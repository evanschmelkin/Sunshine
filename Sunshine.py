import geopy  # this will turn city names into geographic points
from geopy import *
import pandas as pd
import requests
import bs4
import folium  # this is for plotting the actual location
import branca.colormap as cm  # add this import for colormap

#wikiurl = 'https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration'
#tables = pd.read_html(wikiurl)

# make tables into variables (except europe)
#africa = tables[0]
#asia = tables[1]
#northamerica = tables[3]
#southamerica = tables[4]
#oceania = tables[5]

# europe is a special case
#europeurl = 'https://en.wikipedia.org/wiki/List_of_cities_in_Europe_by_sunshine_duration'
#europe = pd.read_html(europeurl)

# by initializing europe[0] the .apply error goes away!
#data = europe[0]

#read from excel
data = pd.read_excel("sunshineexcel.xlsx")
print(data.columns)


europe_geolocator = Nominatim(user_agent="europe_geocoder")

def geocode_address(row):
    location = europe_geolocator.geocode(f"{row['Country']}, {row['City']}", timeout=10)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

data['Latitude'], data['Longitude'] = zip(*data.apply(geocode_address, axis=1))

# this line is relevant because currently the "sunshine hours" are under the column year
# for the later iterations which will allow diff months we will use the months as the variable
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

# remove rows with missing coordinates or sunshine data
data = data.dropna(subset=['Latitude', 'Longitude', 'Year'])

# map center coordinates are good for now
map_center = [data['Latitude'].mean(), data['Longitude'].mean()]

# automatic color scale
colormap = cm.linear.YlOrRd_09.scale(data['Year'].min(), data['Year'].max())
colormap.caption = 'Sunshine Hours'

# folium map creation
mymap = folium.Map(location=map_center, zoom_start=4)

# add colored circle markers with popup showing city and sunshine hours
for _, row in data.iterrows():
    color = colormap(row['Year'])
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=9,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.85,
        popup=f"{row['City']}: {row['Year']} hours"
    ).add_to(mymap)

#add to colormap
colormap.add_to(mymap)

mymap.save("geocoded_map.html")
