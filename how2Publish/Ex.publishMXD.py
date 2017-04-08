# false when trying publish from mxd

import arcpy

# define local variables
wrkspc = 'G:/Fimo/Luan van/mxd/'
mapDoc = arcpy.mapping.MapDocument(wrkspc + 'San bong.mxd')
con = 'G:/Fimo/Luan van/mxd/myLocal.ags'
service = 'San bong'
sddraft = wrkspc + service + '.sddraft'
sd = wrkspc + service + '.sd'
summary = 'test'
tags = 'county, counties'

# create service definition draft
analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER',
                                          con, True, None, summary, tags)
print "analynis done"

# stage and upload the service if the sddraft analysis did not contain errors
if analysis['errors'] == {}:
    # Execute StageService
    arcpy.StageService_server(sddraft, sd)
    # Execute UploadServiceDefinition
    arcpy.UploadServiceDefinition_server(sd, con)
    print 'done'
else:
    # if the sddraft analysis contained errors, display them
    print analysis['errors']