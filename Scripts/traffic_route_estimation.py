import requests
import pandas as pd
from datetime import datetime



# Define your API key
api_key = api_key

# Function to get latitude and longitude for a place using Nominatim (OpenStreetMap API)
def geocode_place(place_name):
    url = f"https://nominatim.openstreetmap.org/search"
    headers = {
        'User-Agent': 'Nairobi Traffic'  # Replace with your app name and contact info
    }
    params = {
        "q": place_name,
        "format": "json",
        "addressdetails": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return latitude, longitude
    return None, None

# Function to calculate travel time, delay, and length using TomTom Traffic API
def get_traffic_data(source, destination):
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{source}:{destination}/json"
    params = {"key": api_key}

    # Send the request to the TomTom API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        #print(data)  # Debugging: Print the response to understand the structure
        if 'routes' in data and len(data['routes']) > 0:
            route = data['routes'][0]

            # Extracting required fields from the response
            travel_time = route['summary']['travelTimeInSeconds']  # Time in seconds
            delay = route['summary']['trafficDelayInSeconds']  # Delay in seconds
            length_in_meters = route['summary']['lengthInMeters']  # Length in meters
            travel_mode = route['summary']['vehicleRestrictions']['type'] if 'vehicleRestrictions' in route['summary'] else 'Car'

            # Calculating departure and arrival time
            current_time = datetime.now()
            departure_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            arrival_time = (current_time + pd.Timedelta(seconds=travel_time)).strftime('%Y-%m-%d %H:%M:%S')

            return travel_time, delay, length_in_meters, travel_mode, departure_time, arrival_time
    return None, None, None, None, None, None

# List of source and destination places (by name) for Mattu Routes
locations = [
    {"source": "Nairobi CBD", "destination": "Westlands"},
    {"source": "Nairobi CBD", "destination": "Eastleigh"},
    {"source": "Nairobi CBD", "destination": "Kenyatta National Hospital"},
    {"source": "Nairobi CBD", "destination": "Nairobi National Park"},
    {"source": "Nairobi CBD", "destination": "Nairobi Railway Station"},
    {"source": "Nairobi CBD", "destination": "JKIA (Jomo Kenyatta International Airport)"},
    {"source": "Westlands", "destination": "Eastleigh"},
    {"source": "Westlands", "destination": "Kenyatta National Hospital"},
    {"source": "Westlands", "destination": "Nairobi National Park"},
    {"source": "Eastleigh", "destination": "Kenyatta National Hospital"},
    {"source": "Eastleigh", "destination": "Nairobi Railway Station"},
    {"source": "Eastleigh", "destination": "JKIA (Jomo Kenyatta International Airport)"},
    {"source": "Kenyatta National Hospital", "destination": "Nairobi Railway Station"},
    {"source": "Kenyatta National Hospital", "destination": "JKIA (Jomo Kenyatta International Airport)"}
    # Add more routes as necessary
]

# List to store results
results = []

# Iterate through the list of source-destination pairs
for loc in locations:
    source_place = loc['source']
    destination_place = loc['destination']

    # Get latitude and longitude for the source and destination
    source_lat, source_lon = geocode_place(source_place)
    destination_lat, destination_lon = geocode_place(destination_place)

    # If both locations were successfully geocoded
    if source_lat and source_lon and destination_lat and destination_lon:
        # Convert the lat-lon into the format required by the TomTom API
        source_coords = f"{source_lat},{source_lon}"
        destination_coords = f"{destination_lat},{destination_lon}"

        # Get traffic data using TomTom API
        travel_time, delay, length_in_meters, travel_mode, departure_time, arrival_time = get_traffic_data(source_coords, destination_coords)

        # Store the results if the API call was successful
        if travel_time is not None:
            current_date = datetime.now().strftime('%Y-%m-%d')
            results.append({
                "Date": current_date,
                "Source": source_place,
                "Destination": destination_place,
                "Time Taken (seconds)": travel_time,
                "Delay (seconds)": delay,
                "Length (meters)": length_in_meters,
                "Travel Mode": travel_mode,
                "Departure Time": departure_time,
                "Arrival Time": arrival_time
            })

# Create a pandas DataFrame from the results
df = pd.DataFrame(results)

# Print the DataFrame
df.head(10)
