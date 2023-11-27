import json
import regex as re

vACC = "BELUX"
with open(f"./output/{vACC}.json", "r") as file:
    lara_config = json.load(file)

def OneTScoorToVG(coor):
    lat , lon = coor
    coor_string = f"{lat} {lon}"
    val = ""

    if re.match(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", coor_string):
        val = re.sub(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "\g<1>\g<2>\g<3>;-\g<5>\g<6>\g<7>\g<8>", coor_string )
    #Degree decimal minutes
    elif re.match(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", coor_string):
        val = re.sub(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "\g<1>\g<2>\g<3>;\g<5>\g<6>\g<7>\g<8>", coor_string )
    
    elif re.match(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", coor_string):
        val = re.sub(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "-\g<1>\g<2>\g<3>;-\g<5>\g<6>\g<7>\g<8>", coor_string )
    
    elif re.match(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?",coor_string):
        val = re.sub(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "-\g<1>\g<2>\g<3>;\g<5>\g<6>\g<7>\g<8>", coor_string )
    else:
        print("No coordinate match found for", coor_string, "Check line 40")
        
    vg_coor = val.replace(" ", "").split(';')
    return vg_coor

def ConvertCoordinates(area):
    #Area is a circle
    if type(area["coordinates_TS"]) == dict:
        area["coordinates_VG"] = area["coordinates_TS"]
        area["coordinates_VG"]["centre"] =  OneTScoorToVG(area["coordinates_TS"]["centre"])
    elif type(area["coordinates_TS"]) == list:
        vg_coors = []
        for coor in area["coordinates_TS"]:
            vg_coors.append(OneTScoorToVG(coor))
        area["coordinates_VG"] =  vg_coors
    else:
        print("No area-coordinates type match for", area)

    area.pop("coordinates_TS")
    return area

def ConvertLabel(area):
    area["label_VG"] = OneTScoorToVG(area["label_TS"])
    area.pop("label_TS")
    return area


#Init code
for i in range(len(lara_config[vACC]["Areas"])):
    area = lara_config[vACC]["Areas"][i]
    
    area = ConvertCoordinates(area)
    area = ConvertLabel(area)
    
    lara_config[vACC]["Areas"][i] = area

with open(f"./output/{vACC}_VG.json", "w") as file:
    file.write(json.dumps(lara_config, indent=4))