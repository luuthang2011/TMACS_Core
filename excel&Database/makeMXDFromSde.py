# Follow procedure's Odoe
# This class want to publish map service from sde with synchronous

import arcpy, os

class MakeMXD:

    def __init__(self, mxdtemplate, workspaceinput, datalayer_input):
        # copy template
        global workspace, datalayer
        workspace = workspaceinput
        datalayer = datalayer_input

        mxd = arcpy.mapping.MapDocument(mxdtemplate)
        mxd.saveACopy(workspace + "\\" + datalayer + "_coding.mxd")
        print mxd.filePath
        # clearer variable
        # del mxd

    def create(self, connection, database):

        # name of data layer ! fucking importance
        print "\\" + database + ".sde." + datalayer
        features = connection + "\\" + database + ".sde." + datalayer
        print features
        feature_Layer = "SDE.ssFeature_Layer"
        lyr_file = workspace + "\\" + datalayer + "_feature.lyr"
        if os.path.exists(lyr_file):
            print "Lyr file already exists, delete it"
            os.remove(lyr_file)

        # use a where clause that works with your data
        where_clause = "'NAME' <> ''"
        arcpy.MakeFeatureLayer_management(features, feature_Layer, where_clause, workspace)
        arcpy.SaveToLayerFile_management(feature_Layer, lyr_file, "ABSOLUTE")

        # add the layer file to your map
        mxd = arcpy.mapping.MapDocument(workspace + "\\" + datalayer + "_coding.mxd")
        print mxd.filePath
        addLayer = arcpy.mapping.Layer(lyr_file)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")
        mxd.saveACopy(workspace + "\\" + datalayer + "_topublish.mxd")
        print "make mxd completed: " + datalayer + "_topublish.mxd"
        del mxd


if __name__ == '__main__':

    # r"..." mean true string in "", don't care special character
    unitest = MakeMXD(r"F:\Code\Arcpy\TMACS\service_processing\template\empty.mxd",
                      r"F:\Code\Arcpy\TMACS\service_processing\mediate",
                      "atm_1")
    unitest.create(r"F:\Code\Arcpy\TMACS\service_processing\connect_information\wh_connection.sde",
                   "wh")
