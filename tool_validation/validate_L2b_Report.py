import arcpy

class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""

    def __init__(self):
        """Setup arcpy and the list of tool parameters."""
        self.params = arcpy.GetParameterInfo()
    
    def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        # Set the list of regions
        self.params[17].filter.list =   ["Altlantic Plain", 
                                        "Appalachain Highlands", 
                                        "Central and Southern AZ", 
                                        "Eastern - Appalachian Plateau, New England, Valley and Ridge", 
                                        "Eastern - Coastal Plain", 
                                        "Eastern - Piedmont", 
                                        "Eastern AZ/NM", 
                                        "Eastern Highlands", 
                                        "Eastern United States", 
                                        "IL River LTE 120", 
                                        "IL River LTE 300", 
                                        "IL River Panther Creek", 
                                        "Illinois River", 
                                        "IN Central Till Plain", 
                                        "IN Northern Moraine and Lake", 
                                        "IN Southern Hills and Lowlands", 
                                        "Interior Highlands", 
                                        "Interior Plains", 
                                        "Intermontane Plateau", 
                                        "KY Bluegrass",
                                        "Laurentian Upland", 
                                        "Lower Southern Driftless", 
                                        "MA", 
                                        "MD Allegheny Plateau/Valley and Ridge", 
                                        "MD Eastern Coastal Plain", 
                                        "MD Piedmont", 
                                        "MD Western Coastal Plain", 
                                        "ME Coastal and Central", 
                                        "MI Southern Lower Ecoregion", 
                                        "Mid-Atlantic", 
                                        "Minnesota Eastern", 
                                        "Minnesota Western", 
                                        "NC Coastal Plain", 
                                        "NC Mountains", 
                                        "NC Piedmont Rural", 
                                        "NC Piedmont Urban", 
                                        "New England", 
                                        "NH", 
                                        "Northeast - Appalachian Plateau, Coastal Plain, New England, Piedmont, Valley and Ridge", 
                                        "Northeast - Appalachian Plateau, New England, Piedmont, Valley and Ridge", 
                                        "Northern Appalachians", 
                                        "NY Hydrologic Region 1/2", 
                                        "NY Hydrologic Region 3", 
                                        "NY Hydrologic Region 4/4a", 
                                        "NY Hydrologic Region 5", 
                                        "NY Hydrologic Region 6", 
                                        "NY Hydrologic Region 7", 
                                        "OH Region A", 
                                        "OH Region B", 
                                        "ON Southern", 
                                        "PA Carbonate Areas", 
                                        "PA Non-Carbonate Areas", 
                                        "PA Piedmont 1", 
                                        "PA Piedmont 2", 
                                        "Pacific Maritime Mountain", 
                                        "Pacific Mountain System", 
                                        "Pacific Northwest", 
                                        "Rocky Mountain System", 
                                        "San Francisco Bay", 
                                        "Southern Appalachians", 
                                        "Southern Driftless", 
                                        "Upper Green River", 
                                        "Upper Salmon River", 
                                        "USA", 
                                        "VA Piedmont", 
                                        "VA, MD Coastal Plain", 
                                        "VA, MD, WV Valley and Ridge", 
                                        "VT", 
                                        "West Interior Basin and Range", 
                                        "Western Cordillera", 
                                        "WV Appalachian Plateau", 
                                        "WV Eastern Valley and Ridge", 
                                        "WV Western Appalachian Plateau"]

        # Set the default region
        self.params[17].value = "USA"
        return
    
    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
