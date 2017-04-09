import os
import xlrd
import arcpy


class Excel2table:
    def __init__(self, in_pool, in_data):
        global workspace, data
        workspace = in_pool
        data = in_data

    # Import each sheet in a Microsoft Excel file into individual tables in a geodatabase.
    def importallsheets(self):
        # read
        print workspace + "\\rawdata\\" + data
        in_excel = workspace + "\\rawdata\\" + data
        workbook = xlrd.open_workbook(in_excel)
        # scan sheets
        sheets = [sheet.name for sheet in workbook.sheets()]
        print('{} sheets found: {}'.format(len(sheets), ','.join(sheets)))

        # excel2table (-> dbf)
        dbf = []
        try:
            for sheet in sheets:
                # The out_table is based on the input excel file name
                # a underscore (_) separator followed by the sheet name
                out_table = workspace + "\\mediate\\" + data.replace(".", "_") + "_" + sheet + ".gdb"
                print out_table
                if os.path.exists(out_table.replace(".gdb", ".dbf")):
                    print "Out_table file already exists, delete it and renew"
                    os.remove(out_table.replace(".gdb", ".dbf"))

                print('Converting {} to {}'.format(sheet, out_table))
                dbf.append(data.replace(".", "_") + "_" + sheet + ".dbf")

                # Perform the conversion
                arcpy.ExcelToTable_conversion(in_excel, out_table, sheet)
        except Exception as err:
            # print "An error occurred in convert excel to table: " + err.args[0]
            print "An error occurred in convert excel to table! Pls check your data ==> Geodata required lat,long with number format!"
        return dbf


if __name__ == '__main__':
    # in folder ++ "rawdata" || out_table ++ "mediate"
    pool = r'F:\Code\Arcpy\TMACS\data_processing'
    data = "cayxang.xls"

    unitest = Excel2table(pool, data)
    print unitest.importallsheets()
