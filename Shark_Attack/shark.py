import pandas as pd
from geopy.geocoders import Nominatim
import re
import folium
import random
from math import floor


df = pd.read_csv('attacks.csv',encoding_errors='ignore')

print("Making the map...")

df2 = df.loc[((df['Country'] == 'USA') & (df['Fatal (Y/N)'] == 'Y') & (df['Year'] > 1999)), ['Year','Area','Location','Fatal (Y/N)','Name','Age']]
df2.to_csv('shark_file.csv')

us_sharks = pd.read_csv('shark_file.csv')


geolocator = Nominatim(user_agent="HLC")

center = [39.443256,-98.95734]
map_us = folium.Map(location=center, zoom_start = 4)

long_list = []

for index, row in us_sharks.iterrows():
    text_location = (row['Location'] + ',' + row['Area'])
    rev_text = text_location[::-1]
    chunks = re.split(',+', rev_text)

    victim_age = row['Age']
    if str(victim_age) == 'nan':
        victim_age = "Unknown"
    else:
        victim_age = floor(victim_age)
    
    first_part = chunks[0]
    second_part = chunks[1]

    if text_location.count(',') > 2:
        third_part = chunks[2]
        combined = first_part + ', ' + second_part + ' ' + third_part
    else:
        combined = first_part +', ' + second_part
    
    
    switch_back = combined[::-1]
    
    try:
        new_location = geolocator.geocode(switch_back)
        location = [new_location.latitude,new_location.longitude]
        
        folium.Marker(location,popup = f"""<div style="font-family: courier new; font-size: 2.1em; color: blue">Identity:<span style="color:black;"> {row["Name"]}</span>\nAge:<span style="color:black;"> {victim_age}</span> </div>"""
                      ).add_to(map_us)        
        
    except:
        continue

map_us.save('fol_map.html')


    


