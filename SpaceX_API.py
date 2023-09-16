#!/usr/bin/env python
# coding: utf-8

# # SpaceX Falcon 9 first stage Landing Prediction

# ## Lab 1: Collecting the data

# ### Estimated time needed: 45 minutes
# 
# In this capstone, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch. In this lab, you will collect and make sure the data is in the correct format from an API. 

# ## Objectives

# #### In this lab, you will make a get request to the SpaceX API. You will also do some basic data wrangling and formating.
# 
# -Request to the SpaceX API
# 
# -Clean the requested data

# #### Import Libraries and Define Auxiliary Functions

# In[ ]:


# Requests allows us to make HTTP requests which we will use to get data from an API
import requests

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd

# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)

# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)


# Below we will define a series of helper functions that will help us use the API to extract information using identification numbers in the launch data.
# 
# From the rocket column we would like to learn the booster name.

# In[62]:


# Define a function to extract the booster name from the rocket column
def getBoosterVersion(data):
        #Iterate thorough the 'rocket' IDs in the data
    for rocket_id in data['rocket']:
        if rocket_id:
            #Make a new API request to get rocket details based on the Id
            rocket_response = requests.get(f"https://api.spacexdata.com/v4/rockets/{rocket_id}").json()
            
            #Extract the booster version and append it to the list
            if 'name' in rocket_response:
                booster_version = rocket_response['name']
                BoosterVersion.append(booster_version)
                
    return BoosterVersion


# From the launchpad we would like to know the name of the launch site being used, the logitude, and the latitude.

# In[79]:


# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):  
    #Iterate thorugh the 'launchpad' IDs in the data
    for launchpad_id in data['launchpad']:
        if launchpad_id:
            # Make a new API request to get launch site details based on the ID
            response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}").json()
            
            #Extract and append launch site information if avaialable 
            if 'longitude' in response and 'latitude' in response and 'name' in response:
                Longitude.append(response['longitude'])
                Latitude.append(response['latitude'])
                LaunchSite.append(response['name'])
            else:
                # Handle cases where some information is missing in the API response
                Longitude.append(None)
                Latitude.append(None)
                LaunchSite.append(None)

    return Longitude, Latitude, LaunchSite         


# From the payload we would like to learn the mass of the payload and the orbit that it is going to.

# In[80]:


# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    # Iterate through the 'payloads' IDs in the data
    for payload_id in data['payloads']:
        if payload_id:
            # Make a new API request to get payload details based on the ID
            response = requests.get(f"https://api.spacexdata.com/v4/payloads/{payload_id}").json()

            # Extract and append payload information if available
            if 'mass_kg' in response and 'orbit' in response:
                PayloadMass.append(response['mass_kg'])
                Orbit.append(response['orbit'])
            else:
                # Handle cases where some information is missing in the API response
                PayloadMass.append(None)
                Orbit.append(None)

    return PayloadMass, Orbit


# From cores we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, wheter the core is reused, wheter legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core

# In[81]:


def getCoreData(data):
    # Iterate through the 'cores' data in the main dataset
    for core in data['cores']:
        if core and core['core']:
            # Make a new API request to get core details based on the core ID
            response = requests.get(f"https://api.spacexdata.com/v4/cores/{core['core']}").json()

            # Extract and append core information if available
            Block.append(response.get('block', None))
            ReusedCount.append(response.get('reuse_count', None))
            Serial.append(response.get('serial', None))

        else:
            # Handle cases where core information is missing
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)

        # Extract and append other core information from the main dataset
        Outcome.append(str(core.get('landing_success', None)) + ' ' + str(core.get('landing_type', None)))
        Flights.append(core.get('flight', None))
        GridFins.append(core.get('gridfins', None))
        Reused.append(core.get('reused', None))
        Legs.append(core.get('legs', None))
        LandingPad.append(core.get('landpad', None))

    return Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial


# Now lets start requesting rocket launch data from SpaceX API with the following URL:

# In[82]:


# Define the SpaceX API endpoint URL
spacex_url="https://api.spacexdata.com/v4/launches/past"

# Make an HTTP GET request to the API endpoint
response = requests.get(spacex_url)


#print(response.content)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    launch_data = response.json()

    # Now you have the launch data in the 'launch_data' variable
    # You can process and analyze this data as needed for your project

    # Example: Print the first launch's details
    if len(launch_data) > 0:
        first_launch = launch_data[0]
        print("First Launch Details:")
        print("Flight Number:", first_launch.get('flight_number', 'N/A'))
        print("Mission Name:", first_launch.get('name', 'N/A'))
        print("Launch Date:", first_launch.get('date_utc', 'N/A'))
    else:
        print("No launch data available.")

else:
    # Handle the case where the request was not successful
    print("Failed to retrieve launch data. Status code:", response.status_code)


# In[83]:


static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

response = requests.get(static_json_url)

if response.status_code == 200:
    
    data = response.json()
    
    if data:
        
        spacex_df = pd.json_normalize(data)
        
        print('First few Rows of the DataFrame:')
        print(spacex_df.head())
        
    else:
        print('No SpaceX launc data available.')
        
else:
    print("Failed to retrieve SpaceX launch data. Status Code:", repsonse.status_code)


# In[68]:


spacex_df.head()


# In[84]:


# Select a subset of the DataFrame with specific columns
spacex_df = spacex_df[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# Remove rows with multiple cores (Falcon rockets with extra boosters) and multiple payloads in a single rocket
spacex_df  = spacex_df [spacex_df ['cores'].map(len) == 1]
spacex_df  = spacex_df [spacex_df ['payloads'].map(len) == 1]

# Extract the single value in the lists for 'cores' and 'payloads'
spacex_df ['cores'] = spacex_df ['cores'].map(lambda x: x[0])
spacex_df ['payloads'] =spacex_df ['payloads'].map(lambda x: x[0])

# Convert the 'date_utc' column to datetime and extract the date component
spacex_df ['date'] = pd.to_datetime(spacex_df ['date_utc']).dt.date

#Filter data to restrict launches up to November 13, 2020
spacex_df = spacex_df [spacex_df ['date'] <= datetime.date(2020, 11, 13)]


# In[70]:


spacex_df


# In[85]:


#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []


# In[86]:


BoosterVersion


# In[87]:


#Call getBoosterVersion
getBoosterVersion(spacex_df)


# In[88]:


BoosterVersion[0:5]


# In[89]:


#Call getLaunchSite
getLaunchSite(spacex_df)


# In[92]:


# Call getPayloadData
getPayloadData(spacex_df)


# In[93]:


# Call getCoreData
getCoreData(spacex_df)


# In[96]:


launch_dict = {'FlightNumber': list(spacex_df['flight_number']),
'Date': list(spacex_df['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}


# In[98]:


launch_df=pd.DataFrame(launch_dict)


# In[101]:


launch_df


# In[102]:


data_falcon9 = launch_df[launch_df['BoosterVersion']=='Falcon 9'].copy()
data_falcon9.reset_index(drop=True, inplace=True)


# In[103]:


data_falcon9


# In[106]:


# data_falcon9['FlightNumber'] = range(1, len(data_falcon9) + 1)
data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
data_falcon9


# # Data Wrangling

# In[110]:


data_falcon9.isnull().sum()


# In[108]:


# Calculate the mean of the 'PayloadMass' column
payload_mass_mean = data_falcon9['PayloadMass'].mean()

# Replace np.nan values with the calculated mean
data_falcon9['PayloadMass'].replace(np.nan, payload_mass_mean, inplace=True)


# In[114]:


data_falcon9.to_csv('F:/Data Science and Python books/Coursera-Assigments/Datascience Capstone Project/data_falcon9_filtered.csv', index=False)

