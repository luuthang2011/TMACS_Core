import os, arcpy


class ConnectDatabase:
    def __init__(self, pool_input):
        self.out_folder_path = pool_input

    def create(self, database):
        # fix file exits
        out_name = database + "_connection.sde"

        self.conneting = self.out_folder_path + '\\' + out_name
        print self.conneting
        if os.path.exists(self.conneting):
            # print "SDE Connection file already exists, delete it"
            # os.remove(self.conneting)
            print "SDE Connection file already exists, If it is changer, please contact system admin"
            return True
        else:
            print "continue with creating sde connection file"
            # create connection to database with arcgis ver 10.3+
            # define values

            # out_folder_path = "Database Connections"
            # out_name = "whCode.sde"
            database_platform = "POSTGRESQL"
            # instance = "192.168.0.168,5432"
            instance = "118.70.72.13,6391"
            account_authentication = "DATABASE_AUTH"
            username = "sde"
            password = "sde"
            save_user_pass = "SAVE_USERNAME"
            # database = "wh" input when system call function
            schema = "#"
            version_type = "TRANSACTIONAL"
            version = "#"

            # execute function
            try:
                arcpy.CreateDatabaseConnection_management(self.out_folder_path,
                                                          out_name,
                                                          database_platform,
                                                          instance,
                                                          account_authentication,
                                                          username,
                                                          password,
                                                          save_user_pass,
                                                          database,
                                                          schema,
                                                          version_type,
                                                          version)
                return True
            except arcpy.ExecuteError, ex:
                print "An error occurred in creating SDE Connection file: " + ex[0]
                return False

# unitest
if __name__ == '__main__':
    connect = ConnectDatabase(r'F:\Code\Arcpy\TMACS\service_processing\connect_information')
    print connect.create("wh")
