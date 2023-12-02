import json
import regex as re
import dms2dec
import package_circle_to_polygon as p
from dms2dec.dms_convert import dms2dec

vACC = "BELUX"
with open(f"./output/{vACC}.json", "r") as file:
    lara_config = json.load(file)

def OneTScoorToGEOjson(coor):
    #lat_or_lon like N50.00.00 AND E004.09.43
    geo_coor = []
    for lat_or_lon in coor:
        hemesphere = lat_or_lon[0]
        degrees = int(lat_or_lon.split(".")[0][1:])
        minutes = lat_or_lon.split(".")[1]
        seconds = lat_or_lon.split(".")[2]
        #TopSky To DMS
        DMS = f'''{degrees}°{minutes}'{seconds}"{hemesphere}'''
        #DMS to DEC
        geo_format = round(dms2dec(DMS),5) # converts to dec N50.00.00 E004.09.43 '''36°44'47.69"N'''
        geo_coor.append(geo_format)

    geo_coor.reverse()

    return geo_coor

def ConvertCoordinates(area):
    #Area is a circle
    if type(area["coordinates_TS"]) == dict:
        centre = OneTScoorToGEOjson(area["coordinates_TS"]["centre"])
        radius = area["coordinates_TS"]["radius"]*1852                #In metres

        coors = []
        for coordinate in p.circle_to_polygon(center = centre, radius = radius)["coordinates"][0]:
            lat, lon = coordinate
            lat = round(lat,5)
            lon = round(lon, 5)
            coors.append([lat,lon])

        area["coordinates_GEO"] = [coors]

    
    #Area is a polygon
    elif type(area["coordinates_TS"]) == list:
        GEO_coors = []
        for coor in area["coordinates_TS"]:
            GEO_coors.append(OneTScoorToGEOjson(coor))

        GEO_coors.append(GEO_coors[0]) #the first and last positions in a LinearRing of coordinates must be the same
        area["coordinates_GEO"] =  [GEO_coors]
    else:
        print("No area-coordinates type match for", area)


    return area["coordinates_GEO"]

def ConvertLabel(area):
    area["label_GEO"] = OneTScoorToGEOjson(area["label_TS"])
    area["label_x"], area["label_y"] = OneTScoorToGEOjson(area["label_TS"])
    area.pop("label_TS")
    return area

def RemoveProperties(area):
    area.pop("coordinates_TS")
    area.pop("activation")
    area.pop("coordinates_GEO") #Not part of geo-features but its own coordinate key
    return area

#Init code
geojson = {
        "type": "FeatureCollection",
        "features": []
    }
for i in range(len(lara_config[vACC]["Areas"])):
    area = lara_config[vACC]["Areas"][i]
    
    coordinatesGEO = ConvertCoordinates(area)
    area = ConvertLabel(area)
    area = RemoveProperties(area)
    
    feature = {"type":"Feature","properties": area,"geometry":{"type":"Polygon","coordinates": coordinatesGEO}}
    geojson["features"].append(feature)

with open(f"./output/{vACC}_GEO.geojson", "w") as file:
    file.write(json.dumps(geojson, indent=4))