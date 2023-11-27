import json

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