# http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/deletemapservice.htm

import json
import urllib
import urllib2

class pig:

    def gentoken(seft, url, username, password, expiration=60):
        query_dict = {'username': username,
                      'password': password,
                      'expiration': str(expiration),
                      'client': 'requestip'}
        query_string = urllib.urlencode(query_dict)
        return json.loads(urllib.urlopen(url + "?f=json", query_string).read())['token']


    def deleteservice(seft, server, servicename, username, password, token=None, port=6080):
        if token is None:
            token_url = "http://{}:{}/arcgis/admin/generateToken".format(server, port)
            token = seft.gentoken(token_url, username, password, )
        delete_service_url = "http://{}:{}/arcgis/admin/services/{}/delete?token={}".format(server, port, servicename,
                                                                                            token)
        urllib2.urlopen(delete_service_url, ' ').read()  # The ' ' forces POST

if __name__ == '__main__':
    TrangPH = pig()
    TrangPH.deleteservice("118.70.72.13", "SampleWorldCities.MapServer", "siteadmin", "1234", token=None, port=6390)

    # # if you need a token, execute this line:
    # deleteservice("<server>", "<service>.MapServer", "<admin username>", "<admin password>")
    #
    # # if you already have a token, execute this line:
    # deleteservice("<server>", "<service>.MapServer", None, None, token='<token string>')