# Created by Sam Gluss 6/1/2017

# Externals
from flask import Flask
import redis

import urllib.request
import os
import zipfile


app = Flask(__name__)

downloadWorkingDir = "download/"
unzipOutput = "data/"
dataZipURL = "http://download.geonames.org/export/dump/cities1000.zip"
downloadedZipLastModded = ""

@app.route("/")
def hello():
    return "Hello World!"

def getCityProps(cityString):
    print(cityString)

# cityData is a string delimited by \t
# The main 'geoname' table has the following fields :
# ---------------------------------------------------
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
# admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
# admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int)
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
# timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format
def addCityToDB(cityData, db):
    city = getCityProps(cityData)

def updateDBFromData(db):
    fileName = dataZipURL.split('/')[-1][0:-4] + ".txt"
    with open(unzipOutput + fileName, 'r', encoding="utf8") as file:
        sourceData = file.read().split("\n")

        for entry in sourceData:
            addCityToDB(entry, db)

def updateCityDataFile():
    fileName = dataZipURL.split('/')[-1]

    if not os.path.exists(downloadWorkingDir):
        os.makedirs(downloadWorkingDir)

    if not os.path.exists(unzipOutput):
        os.makedirs(unzipOutput)

    urllib.request.urlretrieve(dataZipURL, downloadWorkingDir + fileName)

    # Unzip the downloaded file
    zip_ref = zipfile.ZipFile(downloadWorkingDir + fileName, 'r')
    zip_ref.extractall(unzipOutput)
    zip_ref.close()

if __name__ == "__main__":
    redisDB = redis.StrictRedis(host='localhost', port=6379, db=0)

    f = urllib.request.urlopen(dataZipURL)
    lastModified = [s for s in f.headers._headers if 'Last-Modified' in s[0]][0][1]

    if lastModified != downloadedZipLastModded:
        updateCityDataFile()
        updateDBFromData(redisDB)

    app.run()