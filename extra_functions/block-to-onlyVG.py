def makevatglassesfile(blocks):
    vatglass_areas = {}


    for block in blocks:
        area = identify(block, categories)
        print("Testing:",area)

        if all(k in area for k in ("coordinates","category","active")): #Does what we assume is an area have coordinates?
            area["coordinates"] = vatglasses(area["coordinates"])  
            name = area["name"]
            area.pop('name', None)    #remove the name from dic since that will be the key
            vatglass_areas[name] = area

        else:
            print("Not an area")

    return vatglass_areas