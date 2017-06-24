# localCityServer

Requires python 3.X, Flask, and Redis 3.2 or newer installed

The server component for the localCity app.

Once executed, it pulls the city information file from http://download.geonames.org/export/dump/cities1000.zip

This file is unzipped, then parsed into 3 Redis DBs:
    - redisGEO - allows indexing based on latLng, and very fast radius lookups
    - cityData - essential data for map rendering
    - cityExtraData - All the other data

The server responds to HTTP requests. It can currently send back city info within a radius of a point.
It does this by getting the cityIds from the RedisGEO DB, then looks up those ids in the cityData DB.