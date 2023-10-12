def Convert_TScoordinates_toStandardFormat(topskycoordinates):
    geojsoncoordiantes = []
    for coordinate in topskycoordinates.split("\n"):
        #Degree decimal minutes
        output= []
        coors = re.split(':|\s', coordinate)
        for coor in coors:
            hemesphere = coor[0]
            degrees = int(coor.split(".")[0][1:])
            minutes = coor.split(".")[1]
            seconds = coor.split(".")[2]
            e = dms2dec(f'''{degrees}°{minutes}'{seconds}"{hemesphere}''') # converts to dec N50.00.00 E004.09.43 '''36°44'47.69"N'''
            output.append(e)


        geojsoncoordiantes.append([output[1],output[0]])
    #print(geojsoncoordiantes)

    return geojsoncoordiantes #must be nested list
   
def makegeojsonfile(blocks):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for block in blocks:
        area = IdentifyTS_AreaBlock_AndToStandardFormat(block, categories)

        if all(k in area for k in ("coordinates","category","active")): #Does what we assume is an area have coordinates?
            decimalcoordinates = Convert_TScoordinates_toStandardFormat(area["coordinates"])
            area.pop('coordinates', None) #Remove coordinates from the dictionary since we already have them for the polygon
            feature = {"type":"Feature","properties": area,"geometry":{"type":"Polygon","coordinates": decimalcoordinates}}
            geojson["features"].append(feature)

    return geojson