from geopy import geocoders #this will turn city names into geographic points
import pandas as pd
import requests
from bs4 import BeautifulSoup

import pandas as pd
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

# for table in tables:

northamericayears
print(df)
