import json

#Removes comments and enters returns a list of possible areas (see Output/blocks.json)
#Removes everything above the first area definition (e.g.: category definitions (not needed))
def cleanup(file):
    textfile = ""

    file = file.readlines()

    #Remove all comment lines
    for line in file:
        if not line.startswith("//") and not line.startswith(";") and line != "":
            textfile += line.strip() + "\n"

    #Create area blocks
    area_block = textfile.split("AREA:") 

    #Splitting removes the delimiter (AREA:), so we add it again.
    areas = []
    for area in area_block:
        areas.append(f"AREA:{area}\n")
   
    #Debug output
    with open("./output/blocks.json", "w") as f:
        f.write(json.dumps(areas[1:], indent=4))
    
    #Everything before the first words AREA: is not an area and can be safely ignored. 
    return areas[1:]

#Warns the user if an area is actively filtered by the user (or has no coordinates/circle)
def Reason_discard(area, area_filter):
    msg = ""
    if not "coordinates" in area:
        msg = f"{area["name"]} has no coordinates"
    elif area["name"] in area_filter["RemoveByName"]:
        msg = f"{area["name"]} is in area_filter (name)"
    elif area["category"] in area_filter["RemoveByCategory"]:
        msg = f"{area["name"]} is in area_filter (category: '{area["category"]}')"
    else:
        msg = f"Issue with {area["name"]} could not be determined\n{area}"
    
    return f"WARN: {msg} -> area discarted"