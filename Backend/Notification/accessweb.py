import requests
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText

# Function to generate URL based on current date for Landsat 8 and 9
def generate_url(satellite_type, date):
    year = date.strftime("%Y")
    month = date.strftime("%b")  # Abbreviated month, e.g., "Oct"
    day = date.strftime("%d")    # Day of the month with zero-padding
    formatted_date = f"{month}-{day}-{year}"
    
    # Generate the URL for Landsat 8 or 9
    url = f"https://landsat.usgs.gov/landsat/all_in_one_pending_acquisition/{satellite_type}/Pend_Acq/y{year}/{month}/{formatted_date}.txt"
    return url

# Function to fetch satellite data
def fetch_satellite_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Example usage to generate URLs for Landsat 8 and Landsat 9
today = datetime.now()
landsat8_url = generate_url("L8", today)
landsat9_url = generate_url("L9", today)

# Fetch data
landsat8_data = fetch_satellite_data(landsat8_url)
landsat9_data = fetch_satellite_data(landsat9_url)
