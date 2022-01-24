import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json


base_url = 'https://understat.com/match/'
matchnum = list(range(16376, 16380))
print(matchnum)
#matches 16376->16607

firsturl = 'https://understat.com/match/16376'

r1 = requests.get(firsturl)
soup1 = bs(r1.content, 'html.parser')
scripts1 = soup1.find_all('script')

rosters_json_string1 = ''

for each in scripts1:
    if 'rostersData' in each.text:
        rosters_json_string1 = each.text.strip()

urls = []
for each in matchnum:
    urls.append(base_url+str(each)+'/')

def jsonreader(exstring):
    ind_s = exstring.index("(")+2
    ind_e = exstring.index(")")
    json_data = exstring[ind_s:ind_e]
    return json.loads(json_data.encode('utf8'.decode('unicode_escape')))

seasonrosterdata = []

for url in urls:
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    scripts = soup.find_all('script')
    rosters_json_string = ''

    for each in scripts:
        if 'rostersData' in each.text:
            rosters_json_string = each.text.strip()

    json_dict = jsonreader(rosters_json_string)



playerids =list(json_dict['h'].keys())

# column and values names for an individual player
firstplayer = json_dict['h']['475172']
columns = list(firstplayer.keys())
values = list(firstplayer.values())
# print(playerids)

# print(rosters_cleaned['h'])

brears_data = []
for row in json_dict['h']:
    brears_data.append(list(json_dict['h'][row].values()))
    
for row in json_dict['a']:
    brears_data.append(list(json_dict['a'][row].values()))

# print(bre_data)

brears_df = pd.DataFrame(brears_data,columns=columns)