# http://stackoverflow.com/questions/13598958/import-modules-from-different-folders

import sys, arcpy, sys, getopt, datetime
sys.path.append(r'F:\Code\Arcpy\TMACS\excel&Database')
sys.path.append(r'F:\Code\Arcpy\TMACS\how2Publish')
sys.path.append(r'F:\Code\Arcpy\TMACS\hell')
import connectSDE, excel2table, table2XYlayer, makeMXDFromSde, sddraft_ex4, upload_server, deleteMapService

def main(argv):
    sysInput = {'excel': 'cayxang.xls',
           'database': 'wh',
           'reference': 'WGS 1984.prj',
           'replace': 0}
    try:
        opts, args = getopt.getopt(argv, "he:d:p:r:", ["exfile=", "db=", "replace=", "ref="])
        # he:d:p:r:  has special first
    except getopt.GetoptError:
        print 'main.py -e <excel> -d <database>\nEx: main.py -e cayxang.xls -d wh'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print '-e<excel> : Ex:cayxang.xls\n-d<database> : Ex:wh\n-r<datareference> : Ex:WGS 1984.prj\n-p<replace> : 1 or 0'
            sys.exit()
        elif opt in ("-e", "--exfile"):
            sysInput['excel'] = arg
        elif opt in ("-d", "--db"):
            sysInput['database'] = arg
        elif opt in ("-r", "--ref"):
            sysInput['reference'] = arg
        elif opt in ("-p", "--replace"):
            sysInput['replace'] = arg
    return sysInput

if __name__ == '__main__':

    sysInput = main(sys.argv[1:])
    now = datetime.datetime.now()

    # set variables
    database = sysInput['database']
    servicepool = r'F:\Code\Arcpy\TMACS\service_processing'
    datapool = r'F:\Code\Arcpy\TMACS\data_processing'
    dataselection = sysInput['excel']
    reference = sysInput['reference']
    replace = (sysInput['replace'])
    template = servicepool + "\\template\\empty.mxd"
    workspace = servicepool + "\\mediate"
    dbconnection = servicepool + "\\connect_information"
    mapserverconnection = servicepool + "\\connect_information\\ArcgisPublishServer.ags"
    mapserver = "118.70.72.13"
    mapserverUser = "siteadmin"
    mapserverPass = "1234"
    mapserverPort = 6390

    print 'Input file is', sysInput['excel']
    print 'Output database is', sysInput['database']
    print 'Reference is', sysInput['reference']
    print 'Replace is', sysInput['replace']

    # TMACS's workflow
    print "--------------------Welcome to TMACS--------------------"
    connect = connectSDE.ConnectDatabase(dbconnection)
    try:
        if connect.create(database) == True:
            read_excel = excel2table.Excel2table(datapool, dataselection)
            listdbf = read_excel.importallsheets()
            print listdbf
            print connect.conneting

            for dbf in listdbf:
                makeXYlayer = table2XYlayer.Excel2xy(datapool)
                print "dbf is processing: " + dbf
                lyr = makeXYlayer.convert(dbf, reference)
                # print type(lyr)
                print "lyr is processing: " + lyr
                service = lyr.replace(".lyr", "")
                if arcpy.Exists(connect.conneting + "\\" + service) == True:
                    print "Data layer already exists in Database! Do you want replace it? Default: No"
                    # deleteMapService
                    if replace == '1':
                        print ">>>>Important<<<<\nYou choose YES then " + service + " is renewed!"
                        delService = deleteMapService.pig()
                        delService.deleteservice(mapserver, service + ".MapServer", mapserverUser, mapserverPass, token=None, port=mapserverPort)
                        # delete geodatabase
                        arcpy.Delete_management(connect.conneting + "\\" + service)
                    else:
                        print ">>>>Important<<<<\nYou choose No then " + service + " is skipped!"
                        continue
                print "Import datalayer to DB: " + service
                arcpy.FeatureClassToGeodatabase_conversion(lyr, connect.conneting)

                makemxd = makeMXDFromSde.MakeMXD(template, workspace, service)
                makemxd.create(connect.conneting, database)

                makesddraft = sddraft_ex4.Sddraft(workspace, service)
                makesddraft.createwithKmlDisable()
                makesddraft.analyze()

                publish = upload_server.publish(workspace, service, mapserverconnection)
                publish.publish()
    except Exception as err:
        print "!!!!! Something went wrong when TMACS system excited !!!!!"
        print(err.args[0])

    print "\n--------------------TMACS's finish!--------------------\n\t POWER BY FIMO CENTER COPYRIGHT", now.year