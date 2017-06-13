# Created by Sam Gluss 6/1/2017

# Externals
from flask import Flask

import urllib.request
import os
import zipfile

from dbUtils import *

app = Flask(__name__)

downloadWorkingDir = "download/"
unzipOutput = "data/"
dataZipURL = "http://download.geonames.org/export/dump/cities1000.zip"
downloadedZipLastModded = ""

@app.route("/")
def hello():
    return "Hello World!"

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
    redisDB = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    f = urllib.request.urlopen(dataZipURL)
    lastModified = [s for s in f.headers._headers if 'Last-Modified' in s[0]][0][1]

    if lastModified != downloadedZipLastModded:
        updateCityDataFile()
        updateDBFromData(redisDB)

    # test, cities within 10km of oakland, CA
    retVal = redisDB.execute_command('GEORADIUSBYMEMBER', "redisGEO", "5378538", "10", "km")

    redisDB.hmget("cityData", retVal)

    app.run()