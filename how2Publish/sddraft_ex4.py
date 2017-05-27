# disables KmlServer
# convert mxd file to sddraft file

import arcpy
import xml.dom.minidom as DOM


class Sddraft:
    def __init__(self, workspaceinput, serviceinput):

        global mapDoc, service, sddraft, workspace
        workspace = workspaceinput
        service = serviceinput

        # Reference map document for CreateSDDraft function.
        mapDoc = arcpy.mapping.MapDocument(workspace + '\\' + service + '_topublish.mxd')
        # Create service and sddraft variables for CreateSDDraft function.
        sddraft = workspace + '\\' + service + '.sddraft'

    def create(self):
        # Create sddraft.
        arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER')

    def createwithKmlDisable(self):
        self.create()
        # The Server Object Extension (SOE) to disable.
        soe = 'KmlServer'

        # Read the sddraft xml.
        doc = DOM.parse(sddraft)
        # Find all elements named TypeName. This is where the server object extension (SOE) names are defined.
        typeNames = doc.getElementsByTagName('TypeName')
        for typeName in typeNames:
            # Get the TypeName we want to disable.
            if typeName.firstChild.data == soe:
                extension = typeName.parentNode
                for extElement in extension.childNodes:
                    # Disabled SOE.
                    if extElement.tagName == 'Enabled':
                        extElement.firstChild.data = 'false'

        # Output to a new sddraft.
        # outXml = 'F:\Fimo\Luan_van\odoe\\' + service + 'ForWeb.sddraft'
        f = open(sddraft, 'w')
        doc.writexml(f)
        f.close()

    def analyze(self):
        # Analyze the new sddraft for errors.
        analysis = arcpy.mapping.AnalyzeForSD(sddraft)
        for key in ('messages', 'warnings', 'errors'):
            print "----" + key.upper() + "---"
            vars = analysis[key]
            for ((message, code), layerlist) in vars.iteritems():
                print "    ", message, " (CODE %i)" % code
                print "       applies to:",
                for layer in layerlist:
                    print layer.name,
                print

if __name__ == '__main__':
    print "abc"
    unitest = Sddraft(r'F:\Code\Arcpy\TMACS\service_processing\mediate', "cayxang_xls_aab")
    unitest.createwithKmlDisable()
    unitest.analyze()
