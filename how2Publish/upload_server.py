# run after ssdraft ext4

import arcpy, os
from arcpy import env

class publish:
    def __init__(self, workspace, service, connection):

        global inServiceDefinitionDraft, outServiceDefinition, publishServerInfo

        # Set environment settings
        env.workspace = workspace

        # Set local variables
        inServiceDefinitionDraft = service + ".sddraft"
        outServiceDefinition = service + ".sd"
        global result
        result = service

        # publish map server infomation
        publishServerInfo = connection

    def define(self):
        if os.path.exists(arcpy.env.workspace + '//' + outServiceDefinition):
            print "Sd file already exists, delete it and renew"
            os.remove(arcpy.env.workspace + '//' + outServiceDefinition)
        # Execute StageService
        arcpy.StageService_server(inServiceDefinitionDraft, outServiceDefinition)

    def publish(self):
        try:
            self.define()
            # Execute UploadServiceDefinition
            print "Publish running !!"
            arcpy.UploadServiceDefinition_server(outServiceDefinition, publishServerInfo)
            print ">>>>Important<<<<\nSuccess !!"
            return result
        except Exception, e:
            print e.message

if __name__ == '__main__':
    unitest = publish(r"F:\Code\Arcpy\TMACS\service_processing\mediate",
                      'cayxang_xls_aab',
                      r"F:\Code\Arcpy\TMACS\service_processing\connect_information\ArcgisPublishServer.ags")
    unitest.publish()
