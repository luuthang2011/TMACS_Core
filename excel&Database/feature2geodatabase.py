import arcpy

class Lyr2DB:
    def __init__(self, lyr, db):
        arcpy.FeatureClassToGeodatabase_conversion(lyr, db)

if __name__ == '__main__':
    unitest = Lyr2DB(r'F:\Code\Arcpy\TMACS\data_processing\mediate\unitest_01_xlsx_Sheet1.lyr',
                     r'F:\Code\Arcpy\TMACS\service_processing\connect_information\wh_connection.sde')
    print type(unitest)