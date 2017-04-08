# create file connect to publish server as a ags file

import arcpy

outdir = 'F:\Fimo\Luan_van\connect_information'
out_folder_path = outdir
out_name = 'ArcgisPublishServer.ags'
server_url = 'http://118.70.72.13:6390/arcgis/admin/'
use_arcgis_desktop_staging_folder = False
staging_folder_path = outdir
username = 'siteadmin'
password = '1234'

#excute
arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                            out_folder_path,
                                            out_name,
                                            server_url,
                                            "ARCGIS_SERVER",
                                            use_arcgis_desktop_staging_folder,
                                            staging_folder_path,
                                            username,
                                            password,
                                            "SAVE_USERNAME")