"""____________________________________________________________________________
Script Name:          _11_XSLayout.py
Description:          Creates cross sections at regular intervals along a 
                      stream centerline. 
Date:                 4/19/2018

Usage:
Creates cross sections of a specified length at regular intervals along a 
stream centerline. 

This script is based on code from:

Map Rantala - https://nodedangles.wordpress.com/2011/05/01/quick-dirty-arcpy-
              batch-splitting-polylines-to-a-specific-length/

Mateus Ferreira - http://gis4geomorphology.com/stream-transects-partial/


Parameters:
workspace_folder (str)-- Path to the output workspace folder
centerline (str)      -- Path to the centerline feature class.
split_type (str)      -- Method for placing cross sections along the 
                         centerline. "Split at approximate distance" places
                         cross sections along the centerline at the value of 
                         split_distance. "Split at vertices" places cross 
                         sections at vertices. 
distance_split        -- The distance along the centerline that cross sections
                         will be placed. Uses units of the input centerline.
transect_length       -- The length of the cross section.
transect_length_unit  -- The unit of the transect_length.
output_transect       -- Path to the output cross sections.
reach_name            -- The name of the reach. 

Outputs:
output_transect       -- a new cross section feature class
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

              pnt = part.next()
              pntcount = 0

              prevpoint = None
              shapelist = []

              # Enter while loop for each vertex
              #
              while pnt:

                    if not (prevpoint is None):
                        thisDist = distPoint(prevpoint,pnt)
                        maxAdditionalDist = splitDist - totalDist

                        print thisDist, totalDist, maxAdditionalDist

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

                    pnt = part.next()

                    # If pnt is null, either the part is finished or there is an
                    #   interior ring
                    #
                    if not pnt:
                        pnt = part.next()
                        if pnt:
                              print "Interior Ring:"
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


def XSLayout(workspace, Lines, SplitType, DistanceSplit, TransecLength, TransecLength_Unit, OutputTransect, ReachName):
        
    # Set environment variables 
    arcpy.env.overwriteOutput = True
    arcpy.env.XYResolution = "0.00001 Meters"
    arcpy.env.XYTolerance = "0.0001 Meters"

    # Create "General" file geodatabase
    WorkFolder = workspace
    General_GDB = WorkFolder + "\General.gdb"
    arcpy.CreateFileGDB_management(WorkFolder, "General", "CURRENT")
    arcpy.env.workspace = General_GDB
    
    # List parameter values
    arcpy.AddMessage("Workspace: {}".format(arcpy.env.workspace))
    arcpy.AddMessage("Centerline: "
                     "{}".format(arcpy.Describe(Lines).baseName))
    arcpy.AddMessage("Split Type: {}".format(SplitType))
    arcpy.AddMessage("XS Spacing: {}".format(DistanceSplit))
    arcpy.AddMessage("XS Width: {}".format(TransecLength))
    arcpy.AddMessage("XS Width Units: {}".format(TransecLength_Unit))
    arcpy.AddMessage("Output XS: "
                     "{}".format(os.path.basename(OutputTransect)))
    arcpy.AddMessage("Reach Name: {}".format(ReachName))
                     
    #Unsplit Line
    LineDissolve="LineDissolve"
    arcpy.Dissolve_management(Lines, LineDissolve,"", "", "SINGLE_PART")
    LineSplit="LineSplit"

    #Split Line
    if SplitType=="Split at approximate distance":
        splitline(LineDissolve, LineSplit, DistanceSplit)
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
    arcpy.CalculateField_management(LineSplit, "Distance", TransecLength, "PYTHON_9.3")
    
    #Generate Azline1 and Azline2
    spatial_reference=arcpy.Describe(Lines).spatialReference
    Azline1="Azline1"
    Azline2="Azline2"
    arcpy.BearingDistanceToLine_management(LineSplit, Azline1, "X_mid", "Y_mid", "Distance", TransecLength_Unit, "AziLine_1", "DEGREES", "GEODESIC", "LineID", spatial_reference)
    arcpy.BearingDistanceToLine_management(LineSplit, Azline2, "X_mid", "Y_mid", "Distance", TransecLength_Unit, "AziLine_2", "DEGREES", "GEODESIC", "LineID", spatial_reference)
    
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
    arcpy.XYToLine_management(Azline_Dissolve, OutputTransect,"x_start", "y_start", "x_end","y_end", "", "", spatial_reference)
    
    # Create `Seq` field
    arcpy.AddField_management(in_table = OutputTransect, 
                              field_name = "Seq", field_type = "SHORT")
    arcpy.CalculateField_management(in_table = OutputTransect, 
                                    field = "Seq", 
                                    expression = "!OID!", 
                                    expression_type = "PYTHON_9.3")
    
    # Create ReachName field
    arcpy.AddField_management(in_table = OutputTransect, 
                              field_name = "ReachName", field_type = "TEXT")
    arcpy.CalculateField_management(in_table = OutputTransect, 
                                    field = "ReachName", 
                                    expression = "'" + ReachName + "'", 
                                    expression_type = "PYTHON_9.3")                          
    
    # Cleanup
    arcpy.Delete_management(General_GDB)


def main():
    # Call the ChannelSlope function with command line parameters
    XSLayout(workspace, Lines, SplitType, DistanceSplit, TransecLength, 
             TransecLength_Unit, OutputTransect, ReachName)

if __name__ == "__main__":
    # Get input parameters
    workspace          = arcpy.GetParameterAsText(0)
    Lines              = arcpy.GetParameterAsText(1)
    SplitType          = arcpy.GetParameterAsText(2)
    DistanceSplit      = float(arcpy.GetParameterAsText(3))
    TransecLength      = arcpy.GetParameterAsText(4)
    TransecLength_Unit = arcpy.GetParameterAsText(5)
    OutputTransect     = arcpy.GetParameterAsText(6)
    ReachName          = arcpy.GetParameterAsText(7)
    
    main()
