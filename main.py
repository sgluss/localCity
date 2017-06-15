# Created by Sam Gluss 6/1/2017

# Externals
from flask import Flask, request
from flask_cors import CORS
from flask_compress import Compress

import urllib.request
import os
import zipfile
import redis

from dbUtils import *

app = Flask(__name__)
Compress(app)
CORS(app)

downloadWorkingDir = "download/"
unzipOutput = "data/"
dataZipURL = "http://download.geonames.org/export/dump/cities1000.zip"
downloadedZipLastModded = ""

@app.route("/getcities", methods=['POST'])
def getCities():
    data = json.loads(request.data)

    cityIds = redisDB.execute_command('GEORADIUS', "redisGEO", data["lng"], data["lat"], data["radius"], "km")

    if len(cityIds) == 0:
        return "[]"

    return json.dumps(redisDB.hmget("cityData", cityIds))

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

    app.run()