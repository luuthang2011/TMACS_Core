# MakeXYLayer.py
# Description: Creates an XY layer and exports it to a layer file

# import system modules
import arcpy, os, time


class Excel2xy:
    def __init__(self, pool_input):
        # Set environment settings
        arcpy.env.workspace = pool_input + "\\mediate"


    def convert(self, data, reference):
        try:
            # Set the local variables
            in_Table = data
            x_coords = "long"
            y_coords = "lat"
            # z_coords = "POINT_Z"
            out_Layer = data.replace(".dbf", "")
            saved_Layer = data.replace(".dbf", ".lyr")

            # Set the spatial reference
            spRef = arcpy.env.workspace + "\\reference\\" + reference
            print "Using reference " + reference + " with " + out_Layer

            if os.path.exists(arcpy.env.workspace + "\\" + saved_Layer):
                print "Lyr file already exists, delete it and renew"
                os.remove(arcpy.env.workspace + "\\" + saved_Layer)

            # Make the XY event layer...
            arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)

            # Print the total rows
            print "Total rows converted: "
            print(arcpy.GetCount_management(out_Layer))

            # Save to a layer file
            arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
            return saved_Layer

        except Exception as err:
            print(err.args[0])

if __name__ == '__main__':
    unitest = Excel2xy(r'F:\Code\Arcpy\TMACS\data_processing')
    print unitest.convert("unitest_xls_aaaa.dbf", "WGS 1984.prj")
    # same file .lock ~ die
    # print unitest.convert("unitest_xls_aaaa.dbf", "WGS 1984.prj")
    print unitest.convert("unitest_xls_Sheet1.dbf", "WGS 1984.prj")

