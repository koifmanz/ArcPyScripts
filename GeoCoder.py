# -*- coding: utf-8 -*-

from arcpy import GetParameterAsText
import pandas as pd
from geopy.geocoders import Nominatim, Here
from geopy.extra.rate_limiter import RateLimiter

UserAgent = GetParameterAsText(0) # string
GeocodingFile = GetParameterAsText(1) # arcpy table / xls
LocColmn = "FullStreet" 
SaveFolder = GetParameterAsText(2) # folder

CleanLocFrame = pd.read_excel(GeocodingFile, sheet_name="sheet1")
# CleanLocFrame = LocationFrame.drop_duplicates()

Geolocator = Nominatim(user_agent=UserAgent)
geocode = RateLimiter(Geolocator.geocode, min_delay_seconds=2)
CleanLocFrame['location'] = CleanLocFrame[LocColmn].apply(geocode)
CleanLocFrame['point'] = CleanLocFrame['location'].apply(lambda loc: tuple(loc.point) if loc else None)

output = SaveFolder + "/output.xlsx"
CleanLocFrame.to_excel(output)
