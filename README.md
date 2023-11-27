# LARA-Configurator
Creates vLARA configuration file for use on VATSIM.

# Walkthrough
## Set variables
fileDef - Path to the TopskyAreas.txt file + list of area categories. !Make sure the TopskyAreas.txt file only contains your vACC's areas when running the file! Invite your neighbors to the project if they haven't already.😎

vacc - Name of vacc

vaccHTTP - Link to the vACC's API for customised and manual activaitons

Has_Categories - Bool - True: categories of fileDef are taken into account - False: Areas without categories are skipped


## Let's run
Been a while, ay? 

- Run Create_LARA-config
- Run Helpful tools/lara-configTStoGEOjson
- Run Helpful tools/lara-configtoVG

## vaccHTTP
This is a variable that links to the vACC's API. 
It allows the vACC to activate areas in ways we couldn't imagine. 

For example:
Activate area's based on active runways, meteorological conditions, the ab-/presence of a controller position or for example the traffic load. 
It also allows the vACC to manually activate areas and activate or set an area's limit based on the activity and limits of other areas. 

You can customise this fully to your vACC's needs. 
The accepted format is TopSky schedules. 

## Extra attributes
For each area you can optionally add the following keys:
- "entry_conditions" - These are the entry conditions for said area. E.g.: Radio Mandatory Zone - Area reserved to participating a/c - Prohibited to all a/c - ...
- "remark" - Any information you wish to share. E.g.: EBCI SOPOK3K, MEDIL3Y unavailable - Sanicole Airshow - ...
Keep in mind, that these will show every time your area activates! (Unless overwritten by vaccHTTP.)

