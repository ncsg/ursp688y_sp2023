import requests
import time
from datetime import datetime

def fetch_and_save_json(url):
    try:
        # Fetch the JSON data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses
        data = response.json()
        
        # Generate a filename with the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"cabi_bike_status_{timestamp}.json"
        
        # Save the JSON data to a file
        with open(filename, 'w') as file:
            file.write(response.text)
            
        print(f"Saved JSON to {filename}")
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

def main():
    url = "https://gbfs.lyft.com/gbfs/1.1/dca-cabi/en/free_bike_status.json"  # Replace with your actual URL
    
    try:
        while True:
            fetch_and_save_json(url)
            sleep_minutes = 5
            time.sleep(sleep_minutes * 60)
    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    main()