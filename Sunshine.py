import geopy #this will turn city names into geographic points
from geopy import *
import pandas as pd
import requests
import bs4
import folium #this is for plotting the actual location

wikiurl = 'https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration'
tables = pd.read_html(wikiurl)



#make tables into variables (except europe)
africa = tables[0]
asia = tables[1]
northamerica = tables[3]
southamerica = tables[4]
oceania = tables[5]


#europe is a special case
europeurl = 'https://en.wikipedia.org/wiki/List_of_cities_in_Europe_by_sunshine_duration'
europe = pd.read_html(europeurl)

data = europe

# for table in tables:

#northamericayears
print(europe)

europe_geolocator = Nominatim(user_agent="europe_geocoder")

def geocode_address(row):
    location = europe_geolocator.geocode(f"{row['Country']}, {row['City']}")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

data['Latitude'], data['Longitude'] = zip(*data.apply(geocode_address, axis=1))

#calculate mean of coordinates for map center
map_center = [data['Latitude'].mean(), data['Longitude'].mean()]

#make map with folium
mymap = folium.Map(location=map_center, zoom_start=4) #adjust as needed

#add markers
for index, row in data.iterrows():
    if row['Latitude'] and row['Longitude']:
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['City']).add_to(mymap)

#save

mymap.save("geocoded_map.html")
