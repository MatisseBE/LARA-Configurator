import requests
from bs4 import BeautifulSoup
import re

def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch HTML. Status code: {response.status_code}")

def extract_notams(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    notam_elements = soup.find_all('pre')

    notams = []
    for n in notam_elements:
        notams.append(n.text)
    return notams

# Example usage:
url = "https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do?reportType=Raw&actionType=notamRetrievalByICAOs&retrieveLocId=EBBU"
html_content = get_html_content(url)
# with open(f"./extra_functions/Defense Internet NOTAM Service.html", "r") as file:
#     html_content = file.read()
notams = extract_notams(html_content)

list_notam = []
for notam in notams:
    tmp = {}
    split = re.split(r"([a-zA-Z])\)", notam)
    tmp["name"] = split[0].strip()
    tmp["info"] = split[2].strip()
    tmp["FIR"] = split[4].strip()
    tmp["start"] = split[6].strip()
    tmp["end"] = split[8].strip()
    tmp["cyclicity"] = split[10].strip()
    #tmp["description"] = split[12].strip()
    #tmp["lower"] = split[14].strip()
    #tmp["upper"] = split[16].strip()


    list_notam.append(tmp)



print(list_notam[:2])
