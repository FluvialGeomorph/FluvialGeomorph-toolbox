


arcpy.AddField_management(in_table="Riffle_channel", 
                          field_name="Seq_1", 
                          field_type="LONG", 
                          field_is_nullable="NULLABLE", 
                          field_is_required="NON_REQUIRED")


arcpy.CalculateField_management(in_table="Riffle_channel", 
                                field="Seq_1", 
                                expression="!SEQ!", 
                                expression_type="PYTHON")


arcpy.DeleteField_management(in_table="Riffle_channel", 
                             drop_field="SEQ")

arcpy.AddField_management(in_table="Riffle_channel", 
                          field_name="Seq", 
                          field_type="LONG", 
                          field_alias="Seq", 
                          field_is_nullable="NULLABLE", 
                          field_is_required="NON_REQUIRED")


arcpy.CalculateField_management(in_table="Riffle_channel", 
                                field="Seq", 
                                expression="!Seq_1!", 
                                expression_type="PYTHON")


arcpy.DeleteField_management(in_table="Riffle_channel", 
                             drop_field="Seq_1")