# LARA-Configurator
Creates vLARA configuration file for use on VATSIM.

The collection of configuration files can be found [here](https://gitlab.com/portugal-vacc/vatlara-configurations).

# Walkthrough
## Set variables
fileDef - Path to the TopskyAreas.txt file !Make sure the TopskyAreas.txt file only contains your vACC's areas when running the file! Invite your neighbors to the project if they haven't already.😎

vacc - Name of vacc

vaccHTTP - Link to the vACC's API for customised and manual activaitons

Area_filter - object - RemoveTheseAreasName and RemoveTheseAreasCategories: List of string - these areas will be filtered out based on the area's name or category. This can be handy when you want to have an area defined in your TopskyArea.txt file but not in the vLARA configuration.
## vaccHTTP
This is a variable that links to your vACC's API. 
It allows the vACC to activate areas in ways we couldn't imagine. 

For example:
Activate area's based on active runways, meteorological conditions, the ab-/presence of a controller position or for example the traffic load. 
It also allows the vACC to manually activate areas and activate or set an area's limit based on the activity and limits of other areas. 

You can customise this fully to your vACC's needs. 
The accepted format is TopSky schedules, check Example/vaccHTTP-contents. 

## Area-attributes.json
For each area you can optionally add the following keys:
- "entry_conditions" - These are the entry conditions for said area. E.g.: Radio Mandatory Zone - Area reserved to participating a/c - Prohibited to all a/c - ...
- "remark" - Any information you wish to share. E.g.: EBCI SOPOK3K, MEDIL3Y unavailable - Sanicole Airshow - ...
- ("owner" - To come at a later date.)

Keep in mind, that these will show every time your area activates! (Unless overwritten by vaccHTTP.)

## Let's run
Been a while, ay? 

- Run Create_LARA-config
- Run Helpful tools/lara-configTStoGEOjson
- (Run Helpful tools/lara-configtoVG)

Kindly check Output/blocks.json and check if the first and last areas area as expected.

## Anomalies.json
Schedule: A found schedule is not conform the TopskSky format. (This is likely an activation method that is not supported by LARA. Use the vaccHTTP function to activate this area.)

Duplicate area names: When an area is found multiple times in the file, you can find it here.

Less than 3 coordinates: When an area has less than three coordinates it can't be drawn. Circles should not show up here.

No activation: these areas are not triggered by NOTAMs, EAUP nor a schedule. This is not an issue if you plan on activating it only through the vaccHTTP.
## Other useful links
  - [vLARA source code](https://gitlab.com/portugal-vacc/vatlara-api)
  - [vLARA API](https://lara.vatsim.pt/api/docs), [landing page](https://lara.vatsim.pt/) and the [maintainer's page]( https://lara.vatsim.pt/admin)



Please also make sure that your file only contains areas of your vACC. Upload the geojson file to github to check quickly!

## Problems
If you encounter problems, please create an issue. 

If the functions from basic_functions ("clean_up" and ...) are missing, make sure you have cloned the whole repository as these functions can be found in LARA-configurator/extra_functions/basic_functions.py



