












































from inspect import indentsize
from textwrap import indent
import json
import regex as re
from dms2dec.dms_convert import dms2dec
from extra_functions.basic_functions import cleanup
import collections
import warnings

warnings.filterwarnings('ignore', category= SyntaxWarning)

#filepath, area categories*
#* Category as defined in the category line like: CATEGORY:REST
#* Category as defined on the area line like: AREA:4:EBBL_CTA, where 4 is the category.
#* Example ["TRA","TSA"] -> must be a list
#* Set [None] if you dont want a category filter -> must be list of None

fileDef = "C:/Users/matis/OneDrive/Documenten/Euroscope/Plugins/Topsky/TopSkyAreas.txt",  [None] 
#fileDef = "C:/Users/matis/Downloads/Trash/TopSkyAreas_PT.txt", [None]
#fileDef = "C:\\Users\\matis\\OneDrive\\Documenten\\Euroscope\\EDGG-Full-Package_20220226132637-220201-0005\\EDGG\\Plugins\\Topsky_Default\\TopSkyAreas.txt", [None]

 
vacc = "BELUX"
vaccHTTP = "www.beluxvacc/extra_areas"
Has_Categories = True #Does your TS file have CATEGORYDEFs? - If True, all areas without a category will be discarted.

#Filters and converts list of possible areas into a definitive dictionary of actual areas. 
def filterTextBlockForAreas(area_txtblocks, categories):
    all_areas = []
    for block in area_txtblocks:
        possible_area = IdentifyTS_AreaBlock_AndToStandardFormat(block, categories)
        
        if (
            (Has_Categories and all(k in possible_area for k in ("coordinates","category")))
            or (not Has_Categories and all(k in possible_area for k in ("coordinates","active")))
        ):
            all_areas.append(possible_area)       

    return all_areas

#Converts TS coordinates into VG coordinates
def Convert_TScoordinates_toVGformat(topskycoordinates):
    vatgl_coordinates = []
    val = ""
    for coordinate in topskycoordinates.split("\n"):
        if re.match(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", coordinate):
            val = re.sub(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "\g<1>\g<2>\g<3>;-\g<5>\g<6>\g<7>\g<8>", coordinate )
        #Degree decimal minutes
        elif re.match(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", coordinate):
            val = re.sub(r"^N0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "\g<1>\g<2>\g<3>;\g<5>\g<6>\g<7>\g<8>", coordinate )
        
        elif re.match(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", coordinate):
            val = re.sub(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)W([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "-\g<1>\g<2>\g<3>;-\g<5>\g<6>\g<7>\g<8>", coordinate )
        
        elif re.match(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?",coordinate):
            val = re.sub(r"^S0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)E([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?", "-\g<1>\g<2>\g<3>;\g<5>\g<6>\g<7>\g<8>", coordinate )
        else:
            print("No coordinate match found for", coordinate, "Check line 40")
        
        coors = val.replace(" ", "").split(';')
        
        vatgl_coordinates.append(coors)

    return vatgl_coordinates

def Convert_TScoordiantes_ToCircle(topskycoordinates):
    circle_split = topskycoordinates.split(":")
    coorLine = " ".join(circle_split[1:3])
    coors = Convert_TScoordinates_toVGformat(coorLine)[0]
    circle_VG = {
        "centre" : coors,
        "radius" : circle_split[3]
    }
    #area["label"] = "" #will be popped line 155
    return circle_VG

def Rewrite_TScoordinates(topskycoordinates):
    if topskycoordinates.startswith("CIRCLE:"):
        circle_split = topskycoordinates.split(":")
        coors = circle_split[1:3]
        circle_coors = {
            "centre" : coors,
            "radius" : float(circle_split[3])
        }
        return circle_coors
    
    joined_coors = topskycoordinates.split("\n")
    split_coors = []
    for coor in joined_coors:
        tmp = coor.split(" ")
        split_coors.append(tmp)

    return split_coors


#Creates dictionary of areas
def IdentifyTS_AreaBlock_AndToStandardFormat(block, categories):
    data = {}
    
    for line in block.split("\n"):
        if line.startswith("CATEGORY"):
            if line.split(":")[1] in categories or None in categories:
                data["category"] =  line.split(":")[1]
              

        elif line.startswith("AREA"):
            if line.split(":")[1] in categories:
                data["category"] =  line.split(":")[1]

        if line.startswith("LABEL"):
            data["label"] = line.split(":")[1:3]
            # lat =line.split(":")[1]
            # lon = line.split(":")[2]
            # data["label"] = f"{lat} {lon}"


        if line.startswith("AREA"):
            values = line.split(":")
            data["name"] = values[2]

        if line.startswith("LIMITS"):
            values = line.split(":")
            data["lower"] = int(values[1])
            data["upper"] = int(values[2])

        if line.startswith("ACTIVE"):
            activations = line.replace("ACTIVE:", "")
            if "active" in data:
                data["active"]  += "\n" + activations 
            else:
                data["active"] = activations

        ##################################

        if line.startswith("CIRCLE"):
            data["coordinates"] = line

            # circle_split = data["coordinates"].split(":")
            # coorLine = " ".join(circle_split[1:3])
            # coors = Convert_TScoordinates_toVGformat(coorLine)[0]
            # circle_VG = {
            #     "centre" : coors,
            #     "radius" : circle_split[3]
            # }

            # data["coordinates"] = circle_VG
                        
        if re.match(r"^(N|S)0?([0-9]{2}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?(:|\s)(E|W)([0-9]{3}).([0-9]{2}).([0-9]{1,2})(.[0-9]{3,})?",line):
            
            line = line.replace(":"," ") #Coordinates can be separated by : or \s but let's standardise with \s

            if "coordinates" in data:
                data["coordinates"]  += "\n" + line 
            else:
                data["coordinates"] = line

    if "active" in data:
        data["active"] = data["active"].split("\n")
    return data

#Creates activation dictionary
def TSAreaActivationToStandardFormat(rules):
    notams = []
    eaup = []
    schedules = []
    controllers = []

    for rule in rules:
        if rule == "1":
            schedules.append("0101:1231::0000:2359:") #always active
        elif rule.startswith("NOTAM"):
            r = rule.replace("NOTAM:","")[5:] #Hide fir and :
            notams.append(r)
        elif rule.startswith("AUP"):
            r = rule.replace("AUP:","")
            eaup.append(r)
        elif rule.startswith("ID"):
            r = rule.replace("ID:","")
            controllers.append(r)

        else:
            schedules.append(rule)

    activation = {
        "NOTAM" : notams,
        "EAUP" : eaup,
        "ControllerID" : controllers,
        "Schedules" : schedules
    }
    return activation

#Finds or creates a TS-label
def FindLabel(area):
    #Poly areas with a label
    if "label" in area:
        return area["label"], area
    
    #Circles (centre)
    elif area["coordinates"].startswith("CIRCLE:"):
        area["label"] = "" #will be popped line 155
        return area["coordinates_TS"]["centre"], area

    #Poly areas without a label
    else:
        print("No label-position found for area:", area["name"], " --- First coordiante will be label position.")
        area["label"] = "" #will be popped line 155
        return area["coordinates_TS"][0], area
    

#LARA-config workflow  
def CreateLARAConfiguration(all_areas, vacc, vaccHTTP):
    Lara_config = {}
    areas = []
    for area in all_areas:
        area["coordinates_TS"] = Rewrite_TScoordinates(area["coordinates"])

        if "active" in area:
            area["activation"] = TSAreaActivationToStandardFormat(area["active"])
            area.pop("active") 
        else:
            area["activation"] = {}
        
        area["label_TS"], area = FindLabel(area)

  
        #All these have been repurposed elsewhere with a different key
        area.pop("coordinates")
        area.pop("label")

        areas.append(area)

    vacc_config = {
        "Areas" : areas,
        "vACC_HTTP_Activation" : vaccHTTP
    }


    Lara_config = {
        vacc : vacc_config
    }
    return Lara_config

#Post - To find possible malconfigurations
def Find_anomalies(lara_config, vacc):
    areas = lara_config[vacc]["Areas"]

    names = []
    anomaly_schedule = []
    anomaly_coordinates = []
    anomaly_activation = []
    

    for area in areas: 
        names.append(area["name"])

        if len(area["activation"]) > 0: #If activation is defined
            schedules = area["activation"]["Schedules"]
            for s in schedules:
                if not re.search(r"(\d{4,6}:\d{4,6}:\d{0,8}:\d{0,4}:\d{0,4}(?::[0-9]{1,6}:[0-9]{1,6})?(?::[\S]+)?)", s):
                    anomaly_schedule.append(s)

        else:
            anomaly_activation.append(area["name"])

            # if len(area["activation"]["NOTAM"]) == 0 and len(area["activation"]["EAUP"]) == 0 and len(area["activation"]["ControllerID"]) == 0 and len(area["activation"]["Schedules"]) == 0:
            #     anomaly_activation.append(area["name"])
        
        # if len(area["coordinates_VG"]) < 3 and type(area["coordinates_VG"]) == list:
        #     anomaly_coordinates.append(area["name"])



    non_unique_names = [item for item, count in collections.Counter(names).items() if count > 1]

    
    anomalies = {
        "Bad_Schedules" : anomaly_schedule,             #Likely areas activated by runways etc. Please activate these using vaccHTTP and remove their schedule in the json.
        "Duplicates_AreaNames" : non_unique_names,      #This area is defined multiple times.
        "<3_coordinates" : anomaly_coordinates,         #This area does not have coordinates defined. At this time, it might also be a circle.
        "no_activation" : anomaly_activation            #This area is not activated automatically. Please activate using vaccHTTP. Or if unused, remove
    }
    return anomalies
        

#Initializer code
file, categories = fileDef
with open(file, "r") as file:
    area_txtblocks = cleanup(file)
    
    all_areas = filterTextBlockForAreas(area_txtblocks, categories)
    lara_config = CreateLARAConfiguration(all_areas, vacc, vaccHTTP)
    #print(lara_config)

anomalies = Find_anomalies(lara_config, vacc)


with open(f"./output/{vacc}.json", "w") as file:
    file.write(json.dumps(lara_config, indent=4))

with open("./output/anomalies.json", "w") as file:
    file.write(json.dumps(anomalies, indent=4))