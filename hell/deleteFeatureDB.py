import arcpy
arcpy.env.workspace = "C:/data"

print arcpy.Exists(r"F:\Code\Arcpy\TMACS\service_processing\connect_information\wh_connection.sde\wh.sde.unitest_01_xlsx_sheet1")
print arcpy.Delete_management(r"F:\Code\Arcpy\TMACS\service_processing\connect_information\wh_connection.sde\wh.sde.unitest_01_xlsx_sheet1")

# 1 table 1 record sde_table_registry 1 sde_layers 1 geomatry_columns n columns_registry