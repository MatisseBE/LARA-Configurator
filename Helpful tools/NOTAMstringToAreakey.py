import json

#Looks for values (list) in notams(string) and area(returns value's key).
def find_area_for_values_in_NOTAM(dictionary, notam_string):
    found_keys = [key for key, values in dictionary.items() if any(value.lower() in notam_string.lower() for value in values)]
    return found_keys

vACC = "BELUX"
notam_file = "./Helpful tools/notam.txt"
lara_file = f"./Output/{vACC}.json"


with open(notam_file, "r") as file:
    notam_string = file.read()
with open(lara_file, "r") as file:
    lara_json = json.loads(file.read())



tmp_json = {}
for area in lara_json[vACC]["Areas"]:
    if "NOTAM" in area["activation"]:
        tmp_json[area["name"]] = area["activation"]["NOTAM"]
        
print(find_area_for_values_in_NOTAM(tmp_json, notam_string))

