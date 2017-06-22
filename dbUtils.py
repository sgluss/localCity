import json

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
def getCityProps(cityString):
    propsList = cityString.split("\t")

    # Short circuit for bad data
    if len(propsList) != 19:
        return None, None

    city = {}
    cityExtra = {}

    city["geonameid"] = int(propsList[0]) if propsList[0] else -1
    cityExtra["geonameid"] = int(propsList[0]) if propsList[0] else -1

    city["name"] = propsList[1]
    cityExtra["asciiname"] = propsList[2]
    cityExtra["alternatenames"] = propsList[3]
    city["latitude"] = float(propsList[4])
    city["longitude"] = float(propsList[5])
    cityExtra["feature class"] = propsList[6]
    cityExtra["feature code"] = propsList[7]
    city["country code"] = propsList[8]
    cityExtra["cc2"] = propsList[9]
    cityExtra["admin1 code"] = propsList[10]
    cityExtra["admin2 code"] = propsList[11]
    cityExtra["admin3 code"] = propsList[12]
    cityExtra["admin4 code"] = propsList[13]
    city["population"] = int(propsList[14]) if propsList[14] else -1
    cityExtra["elevation"] = int(propsList[15]) if propsList[15] else -1
    cityExtra["dem"] = int(propsList[16]) if propsList[16] else -1
    cityExtra["timezone"] = propsList[17]
    cityExtra["modification date"] = propsList[18]

    return city, cityExtra

def addCityToDB(cityData, db):
    city, cityExtra = getCityProps(cityData)

    if city == None:
        return

    # Geo Add
    db.execute_command('GEOADD',
                       "redisGEO",
                       city["longitude"],
                       city["latitude"],
                       city["geonameid"])

    # Add city data
    db.hset("cityData", city["geonameid"], json.dumps(city))

    # Add city extra data
    db.hset("cityExtraData", cityExtra["geonameid"], json.dumps(cityExtra))
