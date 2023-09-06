#THIS FILE IS KIND OF USELESS NOW, BUT I'm keeping it because I spent the time to make it.
#Right now you need to have already added the YTM playlist to SPT and have the URIs for Spotify for those songs
import json
import datetime

# Let's assume you have your data loaded as json strings

with open("spt_playlist.json", "r") as file:
    spt_data = json.load(file)

with open("ytm_playlist.json", "r") as file:
    ytm_data = json.load(file)


merged = []
id_dupe = []
index_dupe = []
cleaned = []
# Convert the json strings into lists
#longer_data = json.loads(longer_json)
#shorter_data = json.loads(shorter_json)


# Update the shorter list with the publishedAt value where ids match
for item in spt_data:
    merged.append(item)

for item in ytm_data:
    merged.append(item)

def parse_date(date_str):
    try:
        # First, attempt to parse with time
        return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        # If that fails, attempt to parse without time
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
date_test = False
for item in merged:
    date_test = True if "publishedAt" in item else False

if date_test: 
    sorted = sorted(merged, key=lambda x: parse_date(x["publishedAt"]), reverse=True)
    for item in sorted:
        if "spotify_uri" in item:
            uri = item['spotify_uri']
        elif 'uri' in item:
            uri = item['uri']
        else:
            uri = ""
        if uri not in id_dupe:
            if uri != "": id_dupe.append(uri)
            cleaned.append({'uri':uri,'date':item['publishedAt']})
else:
    for item in merged:
        if "spotify_uri" in item:
            uri = item['spotify_uri']
        elif 'uri' in item:
            uri = item['uri']
        else:
            uri = ""
        if uri not in id_dupe:
            if uri != "": id_dupe.append(uri)
            cleaned.append({'uri':uri})

# Convert the shorter list back to a json string if needed


with open("all_sorted_uris.json","w") as file:
    json.dump(cleaned, file, indent=4)
#%%