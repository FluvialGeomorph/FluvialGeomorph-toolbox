import importlib.util
import os
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


TOOL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "tools",
    "_14a_XSPoints_Classify.py",
)


class FakeResult:
    def __init__(self, output):
        self.output = output

    def __getitem__(self, index):
        return self.output


def load_tool(monkeypatch, problem_counts, fail_check_for=None,
              feature_counts=None):
    counts = iter(problem_counts)
    feature_counts = iter(feature_counts if feature_counts is not None else [1] * 10)
    execute_error = type("ExecuteError", (Exception,), {})

    def get_count(path):
        values = counts if "_geometry_check_" in path else feature_counts
        return FakeResult(next(values))

    def check_geometry(in_features, _out_table):
        if in_features == fail_check_for:
            raise execute_error("mock Check Geometry failure")

    arcpy = SimpleNamespace(
        env=SimpleNamespace(scratchGDB="scratch.gdb", overwriteOutput=False),
        ExecuteError=execute_error,
        Exists=Mock(return_value=True),
        AddMessage=Mock(),
        AddWarning=Mock(),
        AddError=Mock(),
        Describe=Mock(side_effect=lambda path: SimpleNamespace(
            baseName=os.path.basename(path))),
        GetMessages=Mock(return_value="mock geoprocessing detail"),
        management=SimpleNamespace(
            CheckGeometry=Mock(side_effect=check_geometry),
            GetCount=Mock(side_effect=get_count),
            Delete=Mock(),
            CopyFeatures=Mock(),
            RepairGeometry=Mock(),
            AddField=Mock(),
            CalculateField=Mock(),
            SelectLayerByLocation=Mock(),
            SelectLayerByAttribute=Mock(),
        ),
        analysis=SimpleNamespace(Buffer=Mock()),
        MakeFeatureLayer_management=Mock(),
        ListFields=Mock(return_value=[]),
        SetParameter=Mock(),
    )
    monkeypatch.setitem(sys.modules, "arcpy", arcpy)
    spec = importlib.util.spec_from_file_location("xs_points_classify", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, arcpy


def test_valid_polygon_uses_original(monkeypatch):
    module, arcpy = load_tool(monkeypatch, [0])

    result = module.prepare_polygon_for_buffer("source.gdb/channel", "channel")

    assert result == "source.gdb/channel"
    arcpy.management.CopyFeatures.assert_not_called()
    arcpy.management.RepairGeometry.assert_not_called()


def test_invalid_polygon_is_repaired_in_scratch_copy(monkeypatch):
    module, arcpy = load_tool(monkeypatch, [1, 0])

    result = module.prepare_polygon_for_buffer("source.gdb/channel", "channel")

    arcpy.management.CopyFeatures.assert_called_once_with(
        "source.gdb/channel", result)
    arcpy.management.RepairGeometry.assert_called_once_with(
        result, delete_null="KEEP_NULL")
    assert result.startswith(os.path.join("scratch.gdb", "channel_repaired_"))
    assert arcpy.AddWarning.called


def test_unrepairable_geometry_stops_with_actionable_error(monkeypatch):
    module, arcpy = load_tool(monkeypatch, [1, 2])

    with pytest.raises(RuntimeError, match="still has 2 geometry problem"):
        module.prepare_polygon_for_buffer("source.gdb/channel", "channel")

    arcpy.management.CopyFeatures.assert_called_once()
    arcpy.AddError.assert_called_once()


def test_both_inputs_are_checked_before_xs_points_are_changed(monkeypatch):
    floodplain = "workspace.gdb\\dataset\\floodplain"
    module, arcpy = load_tool(monkeypatch, [0], fail_check_for=floodplain)

    with pytest.raises(arcpy.ExecuteError, match="mock Check Geometry failure"):
        module.XSPointsClassify(
            "workspace.gdb\\dataset",
            "workspace.gdb\\dataset\\xs_points",
            "workspace.gdb\\dataset\\channel",
            floodplain,
            "1 Meters",
        )

    arcpy.management.AddField.assert_not_called()
    arcpy.management.CalculateField.assert_not_called()
    arcpy.AddError.assert_called_once()
    assert arcpy.management.Delete.call_count == 2


def test_empty_polygon_is_rejected(monkeypatch):
    module, arcpy = load_tool(monkeypatch, [], feature_counts=[0])
    with pytest.raises(RuntimeError, match="contains no features"):
        module.prepare_polygon_for_buffer("empty", "channel")
    arcpy.management.RepairGeometry.assert_not_called()


def test_repair_cannot_silently_remove_features(monkeypatch):
    module, arcpy = load_tool(monkeypatch, [1, 0], feature_counts=[1, 0])
    with pytest.raises(RuntimeError, match="feature count from 1 to 0"):
        module.prepare_polygon_for_buffer("channel", "channel")
    arcpy.AddError.assert_called_once()


@pytest.mark.parametrize("failed_buffer", [1, 2])
def test_buffer_failure_leaves_xs_fields_untouched(monkeypatch, failed_buffer):
    module, arcpy = load_tool(monkeypatch, [0, 0])
    failure = arcpy.ExecuteError("mock Buffer failure")
    arcpy.analysis.Buffer.side_effect = (
        [failure] if failed_buffer == 1 else [None, failure])
    with pytest.raises(arcpy.ExecuteError, match="mock Buffer failure"):
        module.XSPointsClassify(
            "workspace.gdb\\dataset", "xs_points", "channel", "floodplain", "1")
    arcpy.management.AddField.assert_not_called()
    arcpy.management.CalculateField.assert_not_called()


def test_cleanup_failure_does_not_hide_check_failure(monkeypatch):
    module, arcpy = load_tool(monkeypatch, [], fail_check_for="channel")
    arcpy.management.Delete.side_effect = arcpy.ExecuteError("cleanup failure")
    with pytest.raises(arcpy.ExecuteError, match="mock Check Geometry failure"):
        module.prepare_polygon_for_buffer("channel", "channel")
    arcpy.AddWarning.assert_called_once()
