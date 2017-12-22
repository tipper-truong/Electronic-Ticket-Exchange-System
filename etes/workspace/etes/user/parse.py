from geopy.geocoders import Nominatim
import csv 

location_list = []

# Open Countries.csv file, making it a file object, then getting ready to parse file
with open('Countries.csv') as csvDataFile:

    csvReader = csv.reader(csvDataFile) # Return a reader object which will iterate over lines in the given csv file --> csvDataFile
    for row in csvReader: # For every row in the excel sheet
        location = row[0] #location of city or state is located in col 0, row 0 in the excel sheet of Countries.csv
        location_list.append(location) # append the location string to a list data structure

for l in location_list: # for every location in the location_list data structure
    
    geolocator = Nominatim() # Instantiating a geolocator object. For more information about Nominatim --> http://wiki.openstreetmap.org/wiki/Nominatim
        
    # 3 arguments:
    # l = location name (city/state/etc.), 
    # timeout=10 = give it 10 seconds to locate the address of given location
    # language="en" No matter what location is given, return English address format, not foreign address format.
        
    location = geolocator.geocode(l, timeout=10, language="en") 
        
    try:
        # If retrieving location address data is SUCCESSFUL, print address
        # Without substringing, the address looks like this originally: Niort, Deux-S\xe8vres, New Aquitaine, Metropolitan France, 79000, France
        # Split each location string by "comma", now it will be stored in an array like this: [u'Niort', u' Deux-S\xe8vres', u' New Aquitaine', u' Metropolitan France', u' 79000', u' France']
        # Country is located at the last element of the array, do length of array - 1 --> [-1]
        # .strip() to get rid of the whitespace
        print location.address.split(",")[-1].strip()
    except AttributeError: 
        # Attribute errors in Python are generally raised when you try to access or call an attribute that a particular object type doesn’t possess.
        # Due to formatting issues in the excel sheet file for each city/state/etc.,
        # it raises an Attribute Error because geolocator.geocode(...) can't find the location data of the given city/state/etc.
        # which returns NoneType object --> generates AttributeError: 'NoneType' object has no attribute 'address'
        print 'N/A'
            