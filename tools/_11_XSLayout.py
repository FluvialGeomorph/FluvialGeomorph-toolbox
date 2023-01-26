"""____________________________________________________________________________
Script Name:          _11_XSLayout.py
Description:          Creates cross sections at regular intervals along a 
                      stream centerline. 
Date:                 05/27/2020

Usage:
Creates cross sections of a specified length at regular intervals along a 
stream flowline. 

This script is based on code from:

The `splitline` function is based on code from:
Map Rantala - https://nodedangles.wordpress.com/2011/05/01/quick-dirty-arcpy-
              batch-splitting-polylines-to-a-specific-length/

The `XSLayout` function is based on code from: 
Mateus Ferreira - https://web.archive.org/web/20161229230139/
      http://gis4geomorphology.com/wp-content/uploads/2014/12/Transect-Tool.zip


Parameters:
feature_dataset       -- Path to the feature dataset. 
flowline              -- Path to the flowline feature class.
split_type            -- Method for placing cross sections along the 
                         flowline. "Split at approximate distance" places
                         cross sections along the flowline at the value of 
                         transect_spacing. "Split at vertices" places cross 
                         sections at the nearest existing flowline vertex. 
transect_spacing      -- The distance between cross sections as measured along 
                         the flowline. Uses units of the input flowline.
transect_width        -- The width of the cross section as measured from the 
                         flowline to its furthest outside point. Therefore, a 
                         value of 50 ft for transect_width will result in a 
                         cross section with an overall width of 100 ft (50 ft 
                         on the right descending bank and 50 ft on the left 
                         descending bank).
transect_width_unit   -- The unit of the transect_width.

Outputs:
output_transect -- a new cross section feature class named using the following 
pattern xs_<spacing>_<width>, where <spacing> is the transect_spacing and 
<width> is the transect_width. 
____________________________________________________________________________"""

import os
import arcpy
import math

def splitline(inFC, FCName, alongDist):
    """ 
    
    This function was developed by Map Rantala - 
    https://nodedangles.wordpress.com/2011/05/01/quick-dirty-arcpy-batch-
    splitting-polylines-to-a-specific-length/
    """
    OutDir = arcpy.env.workspace
    outFCName = FCName
    outFC = OutDir + "/" + outFCName
    
    def distPoint(p1, p2):
        calc1 = p1.X - p2.X
        calc2 = p1.Y - p2.Y

        return math.sqrt((calc1**2) + (calc2**2))

    def midpoint(prevpoint,nextpoint,targetDist,totalDist):
        newX = prevpoint.X + ((nextpoint.X - prevpoint.X) * (targetDist/totalDist))
        newY = prevpoint.Y + ((nextpoint.Y - prevpoint.Y) * (targetDist/totalDist))
        return arcpy.Point(newX, newY)

    def splitShape(feat,splitDist):
        # Count the number of points in the current multipart feature
        #
        partcount = feat.partCount
        partnum = 0
        # Enter while loop for each part in the feature (if a singlepart feature
        # this will occur only once)
        #
        lineArray = arcpy.Array()

        while partnum < partcount:
              # Print the part number
              #
              #print "Part " + str(partnum) + ":"
              part = feat.getPart(partnum)
              #print part.count

              totalDist = 0

              pnt = next(part)
              pntcount = 0

              prevpoint = None
              shapelist = []

              # Enter while loop for each vertex
              #
              while pnt:

                    if not (prevpoint is None):
                        thisDist = distPoint(prevpoint,pnt)
                        maxAdditionalDist = splitDist - totalDist

                        print((thisDist, totalDist, maxAdditionalDist))

                        if (totalDist + thisDist) > splitDist:
                              while(totalDist + thisDist) > splitDist:
                                    maxAdditionalDist = splitDist - totalDist
                                    newpoint = midpoint(prevpoint, 
                                                        pnt, 
                                                        maxAdditionalDist, 
                                                        thisDist)
                                    lineArray.add(newpoint)
                                    shapelist.append(lineArray)

                                    lineArray = arcpy.Array()
                                    lineArray.add(newpoint)
                                    prevpoint = newpoint
                                    thisDist = distPoint(prevpoint, pnt)
                                    totalDist = 0

                              lineArray.add(pnt)
                              totalDist += thisDist
                        else:
                              totalDist += thisDist
                              lineArray.add(pnt)
                              #shapelist.append(lineArray)
                    else:
                        lineArray.add(pnt)
                        totalDist = 0

                    prevpoint = pnt                
                    pntcount += 1

                    pnt = next(part)

                    # If pnt is null, either the part is finished or there is an
                    #   interior ring
                    #
                    if not pnt:
                        pnt = next(part)
                        if pnt:
                              print("Interior Ring:")
              partnum += 1

        if (lineArray.count > 1):
              shapelist.append(lineArray)

        return shapelist

    if arcpy.Exists(outFC):
        arcpy.Delete_management(outFC)

    arcpy.Copy_management(inFC,outFC)

    #origDesc = arcpy.Describe(inFC)
    #sR = origDesc.spatialReference

    #revDesc = arcpy.Describe(outFC)
    #revDesc.ShapeFieldName

    deleterows = arcpy.UpdateCursor(outFC)
    for iDRow in deleterows:       
         deleterows.deleteRow(iDRow)

    try:
        del iDRow
        del deleterows
    except:
        pass

    inputRows = arcpy.SearchCursor(inFC)
    outputRows = arcpy.InsertCursor(outFC)
    fields = arcpy.ListFields(inFC)

    numRecords = int(arcpy.GetCount_management(inFC).getOutput(0))
    OnePercentThreshold = numRecords // 100

    #printit(numRecords)

    iCounter = 0
    iCounter2 = 0

    for iInRow in inputRows:
        inGeom = iInRow.shape
        iCounter += 1
        iCounter2 += 1    
        if (iCounter2 > (OnePercentThreshold+0)):
              #printit("Processing Record "+str(iCounter) + " of "+ str(numRecords))
              iCounter2 = 0

        if (inGeom.length > alongDist):
              shapeList = splitShape(iInRow.shape,alongDist)

              for itmp in shapeList:
                    newRow = outputRows.newRow()
                    for ifield in fields:
                        if (ifield.editable):
                              newRow.setValue(ifield.name, 
                                              iInRow.getValue(ifield.name))
                    newRow.shape = itmp
                    outputRows.insertRow(newRow)
        else:
              outputRows.insertRow(iInRow)

    del inputRows
    del outputRows


def XSLayout(feature_dataset, flowline, split_type, transect_spacing, 
             transect_width, transect_width_unit):
        
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.XYResolution = "0.00001 Meters"
    arcpy.env.XYTolerance = "0.0001 Meters"

    # Create "General" file geodatabase
    project_gdb = os.path.dirname(feature_dataset)
    WorkFolder = os.path.dirname(project_gdb)
    General_GDB = WorkFolder + "\General.gdb"
    arcpy.CreateFileGDB_management(WorkFolder, "General", "CURRENT")
    arcpy.env.workspace = General_GDB
    
    # List parameter values
    arcpy.AddMessage("Output Workspace: {}".format(project_gdb))
    arcpy.AddMessage("Workfolder: {}".format(WorkFolder))
    arcpy.AddMessage("Flowline: "
                     "{}".format(arcpy.Describe(flowline).baseName))
    arcpy.AddMessage("Split Type: {}".format(split_type))
    arcpy.AddMessage("XS Spacing: {}".format(transect_spacing))
    arcpy.AddMessage("XS Width: {}".format(transect_width))
    arcpy.AddMessage("XS Width Units: {}".format(transect_width_unit))
    
    #Unsplit Line
    LineDissolve="LineDissolve"
    arcpy.Dissolve_management(flowline, LineDissolve,"", "", "SINGLE_PART")
    LineSplit="LineSplit"

    #Split Line
    if split_type=="Split at approximate distance":
        splitline(LineDissolve, LineSplit, transect_spacing)
    else:
        arcpy.SplitLine_management(LineDissolve, LineSplit)
    
    #Add fields to LineSplit
    FieldsNames=["LineID", "Direction", "Azimuth", "X_mid", "Y_mid", "AziLine_1", "AziLine_2", "Distance"]
    for fn in FieldsNames:
        arcpy.AddField_management(LineSplit, fn, "DOUBLE")
    
    #Calculate Fields
    CodeBlock_Direction="""def GetAzimuthPolyline(shape):
     radian = math.atan((shape.lastpoint.x - shape.firstpoint.x)/(shape.lastpoint.y - shape.firstpoint.y))
     degrees = radian * 180 / math.pi
     return degrees"""
     
    CodeBlock_Azimuth="""def Azimuth(direction):
     if direction < 0:
      azimuth = direction + 360
      return azimuth
     else:
      return direction"""
    CodeBlock_NULLS="""def findNulls(fieldValue):
        if fieldValue is None:
            return 0
        elif fieldValue is not None:
            return fieldValue"""
    arcpy.CalculateField_management(LineSplit, "LineID", "!OBJECTID!", "PYTHON_9.3")
    arcpy.CalculateField_management(LineSplit, "Direction", "GetAzimuthPolyline(!Shape!)", "PYTHON_9.3", CodeBlock_Direction)
    arcpy.CalculateField_management(LineSplit, "Direction", "findNulls(!Direction!)", "PYTHON_9.3", CodeBlock_NULLS)
    arcpy.CalculateField_management(LineSplit, "Azimuth", "Azimuth(!Direction!)", "PYTHON_9.3", CodeBlock_Azimuth)
    arcpy.CalculateField_management(LineSplit, "X_mid", "!Shape!.positionAlongLine(0.5,True).firstPoint.X", "PYTHON_9.3")
    arcpy.CalculateField_management(LineSplit, "Y_mid", "!Shape!.positionAlongLine(0.5,True).firstPoint.Y", "PYTHON_9.3")
    CodeBlock_AziLine1="""def Azline1(azimuth):
     az1 = azimuth + 90
     if az1 > 360:
      az1-=360
      return az1
     else:
      return az1"""
    CodeBlock_AziLine2="""def Azline2(azimuth):
     az2 = azimuth - 90
     if az2 < 0:
      az2+=360
      return az2
     else:
      return az2"""
    arcpy.CalculateField_management(LineSplit, "AziLine_1", "Azline1(!Azimuth!)", "PYTHON_9.3", CodeBlock_AziLine1)
    arcpy.CalculateField_management(LineSplit, "AziLine_2", "Azline2(!Azimuth!)", "PYTHON_9.3", CodeBlock_AziLine2) 
    arcpy.CalculateField_management(LineSplit, "Distance", transect_width, "PYTHON_9.3")
    
    #Generate Azline1 and Azline2
    spatial_reference=arcpy.Describe(flowline).spatialReference
    Azline1="Azline1"
    Azline2="Azline2"
    arcpy.BearingDistanceToLine_management(LineSplit, Azline1, "X_mid", "Y_mid", "Distance", transect_width_unit, "AziLine_1", "DEGREES", "GEODESIC", "LineID", spatial_reference)
    arcpy.BearingDistanceToLine_management(LineSplit, Azline2, "X_mid", "Y_mid", "Distance", transect_width_unit, "AziLine_2", "DEGREES", "GEODESIC", "LineID", spatial_reference)
    
    #Create Azline and append Azline1 and Azline2
    Azline="Azline"
    arcpy.CreateFeatureclass_management(arcpy.env.workspace, "Azline", "POLYLINE", "", "", "", spatial_reference)
    arcpy.AddField_management(Azline, "LineID", "DOUBLE")
    arcpy.Append_management([Azline1, Azline2], Azline, "NO_TEST")
    
    #Dissolve Azline
    Azline_Dissolve="Azline_Dissolve"
    arcpy.Dissolve_management(Azline, Azline_Dissolve,"LineID", "", "SINGLE_PART")
    
    #Add Fields to Azline_Dissolve
    FieldsNames2=["x_start", "y_start", "x_end", "y_end"]
    for fn2 in FieldsNames2:
        arcpy.AddField_management(Azline_Dissolve, fn2, "DOUBLE")
        
    #Calculate Azline_Dissolve fields
    arcpy.CalculateField_management(Azline_Dissolve, "x_start", "!Shape!.positionAlongLine(0,True).firstPoint.X", "PYTHON_9.3") 
    arcpy.CalculateField_management(Azline_Dissolve, "y_start", "!Shape!.positionAlongLine(0,True).firstPoint.Y", "PYTHON_9.3")
    arcpy.CalculateField_management(Azline_Dissolve, "x_end", "!Shape!.positionAlongLine(1,True).firstPoint.X", "PYTHON_9.3")
    arcpy.CalculateField_management(Azline_Dissolve, "y_end", "!Shape!.positionAlongLine(1,True).firstPoint.Y", "PYTHON_9.3")
    
    #Generate output file
    out_transect_name = "xs_{}_{}".format(int(round(transect_spacing)),
                                          int(round(transect_width)))
    output_transect = os.path.join(feature_dataset, out_transect_name)
    arcpy.XYToLine_management(Azline_Dissolve, output_transect,
                              "x_start", "y_start", "x_end","y_end", 
                              "", "", spatial_reference)
    
    # Create `Seq` field
    arcpy.AddField_management(in_table = output_transect, 
                              field_name = "Seq", field_type = "SHORT")
    arcpy.CalculateField_management(in_table = output_transect, 
                                    field = "Seq", 
                                    expression = "!OID!", 
                                    expression_type = "PYTHON_9.3")
    
    # Set the ReachName field
    unique_reaches = set(row[0] for row in arcpy.da.SearchCursor(flowline, 
                                                                 "ReachName"))
    reach_name = list(unique_reaches)[0]
    arcpy.AddField_management(in_table = output_transect, 
                              field_name = "ReachName", field_type = "TEXT")
    arcpy.CalculateField_management(in_table = output_transect, 
                                    field = "ReachName", 
                                    expression = "'" + reach_name + "'", 
                                    expression_type = "PYTHON_9.3")                          
    
    # Return
    arcpy.SetParameter(6, output_transect)
    
    # Cleanup
    arcpy.Delete_management(General_GDB)


def main():
    # Call the ChannelSlope function with command line parameters
    XSLayout(feature_dataset, flowline, split_type, transect_spacing, 
             transect_width, transect_width_unit)

if __name__ == "__main__":
    # Get input parameters
    feature_dataset     = arcpy.GetParameterAsText(0)
    flowline            = arcpy.GetParameterAsText(1)
    split_type          = arcpy.GetParameterAsText(2)
    transect_spacing    = float(arcpy.GetParameterAsText(3))
    transect_width      = float(arcpy.GetParameterAsText(4))
    transect_width_unit = arcpy.GetParameterAsText(5)
    
    main()
