"""Synthetic ArcGIS Pro checks; these do not reproduce issue #49's dataset."""
import importlib.util
import os

import pytest


arcpy = pytest.importorskip("arcpy")
tool_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "tools", "_14a_XSPoints_Classify.py")
spec = importlib.util.spec_from_file_location("xs_classify_arcpy", tool_path)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


@pytest.fixture
def workspace(tmp_path):
    gdb = arcpy.management.CreateFileGDB(str(tmp_path), "test.gdb")[0]
    sr = arcpy.SpatialReference(3857)
    dataset = arcpy.management.CreateFeatureDataset(gdb, "features", sr)[0]
    with arcpy.EnvManager(
            workspace=gdb, scratchWorkspace=gdb, overwriteOutput=True):
        yield dataset, sr
        if arcpy.Exists("xs_points"):
            arcpy.management.Delete("xs_points")
    arcpy.management.ClearWorkspaceCache()


def polygon(workspace, name, coordinates):
    dataset, sr = workspace
    fc = arcpy.management.CreateFeatureclass(
        dataset, name, "POLYGON", spatial_reference=sr)[0]
    with arcpy.da.InsertCursor(fc, ["SHAPE@"]) as cursor:
        shape = None if coordinates is None else arcpy.Polygon(
            arcpy.Array([arcpy.Point(x, y) for x, y in coordinates]), sr)
        cursor.insertRow([shape])
    return fc


def snapshot(fc):
    with arcpy.da.SearchCursor(fc, ["OID@", "SHAPE@JSON"]) as cursor:
        return list(cursor)


def test_valid_polygons_classify_points_and_preserve_sources(workspace):
    dataset, sr = workspace
    channel = polygon(
        workspace, "channel", [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)])
    floodplain = polygon(
        workspace, "floodplain",
        [(-5, -5), (-5, 15), (15, 15), (15, -5), (-5, -5)])
    before = snapshot(channel), snapshot(floodplain)
    points = arcpy.management.CreateFeatureclass(
        dataset, "points", "POINT", spatial_reference=sr)[0]
    with arcpy.da.InsertCursor(points, ["SHAPE@XY"]) as cursor:
        for xy in [(5, 5), (12, 12), (30, 30)]:
            cursor.insertRow([xy])
    tool.XSPointsClassify(dataset, points, channel, floodplain, "1 Meters")
    with arcpy.da.SearchCursor(points, ["channel", "floodplain"]) as cursor:
        assert list(cursor) == [(1, 1), (0, 1), (0, 0)]
    assert (snapshot(channel), snapshot(floodplain)) == before


def test_null_geometry_fails_without_changing_source_or_points(workspace):
    dataset, sr = workspace
    channel = polygon(
        workspace, "channel", [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)])
    floodplain = polygon(workspace, "null_floodplain", None)
    before = snapshot(floodplain)
    points = arcpy.management.CreateFeatureclass(
        dataset, "points", "POINT", spatial_reference=sr)[0]
    arcpy.management.AddField(points, "channel", "SHORT")
    arcpy.management.AddField(points, "floodplain", "SHORT")
    with arcpy.da.InsertCursor(
            points, ["SHAPE@XY", "channel", "floodplain"]) as cursor:
        cursor.insertRow([(5, 5), 7, 8])
    with pytest.raises(RuntimeError, match="still has"):
        tool.XSPointsClassify(dataset, points, channel, floodplain, "1 Meters")
    assert snapshot(floodplain) == before
    with arcpy.da.SearchCursor(points, ["channel", "floodplain"]) as cursor:
        assert list(cursor) == [(7, 8)]
