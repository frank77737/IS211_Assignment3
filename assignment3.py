import argparse
import urllib.request
import logging
import datetime
import sys
import csv
import re
from datetime import datetime


#function to dowload the csv file 

def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"File downloaded successfully")
        return True
    except Exception as e:
        print(f"ERROR: cannot download file: {e}")
        return False

#function to count the images in the csv file
def count_images(filename):
    #regex to find pics 
    image_tags = r'\.(png|jpg|gif)\b'
    image_hits = 0
    file_lines = 0
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                file_lines += 1
                #find all images in row 0
                image_hits += len(re.findall(image_tags, row[0], re.IGNORECASE))
    except Exception as e:
        print(f"ERROR: cannot read file: {e}")
    return f"Image requests account for {(image_hits / file_lines) * 100:.2f}% of all requests"

#function to count the browsers in the csv file 
def count_browsers(filename):
    browsers = r'\b(Firefox|Chrome|MSIE)\b'
    browsers_dict = {
        'firefox': 0,
        'chrome': 0,
        'msie': 0,
        'safari': 0
    }
    file_lines = 0
    browser_sums = 0
    the_date = ""
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                file_lines += 1
                matches = re.findall(browsers, row[2], re.IGNORECASE)
                for match in matches:
                    browsers_dict[match.lower()] += 1
                    browser_sums += 1
                    time_column = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                    the_date = time_column.strftime("%Y-%m-%d")
        safaris = file_lines - browser_sums
        browsers_dict['safari'] = safaris
        most_popular_browser = max(browsers_dict, key=browsers_dict.get)
        most_popular_browser_hits = max(browsers_dict.values())
    except Exception as e:
        print(f"ERROR: cannot read file: {e}")
    return f"The most popular browser is {most_popular_browser} accounting for {(most_popular_browser_hits / file_lines) * 100:.2f}% of all requests on {the_date}"

#function to count the hours in the csv file
def count_hours(filename):
    hours_dict = {f'{i:02d}': 0 for i in range(24)}
    file_lines = 0
    hour_sums = 0
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                file_lines += 1
                #datetime module to find time
                time_column = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                hour = time_column.strftime("%H") #isolating the hours
                hours_dict[hour] += 1
                hour_sums += 1
        #get most popular via max
        most_popular_hour = max(hours_dict, key=hours_dict.get)
                
    except Exception as e:
        print(f"Error reading file: {e}")
    #go thru dict, print hour with highest num of hits, discard, get new hour with highest num of hits, discard, rinse and repeat
    while hours_dict:
        most_popular_hour = max(hours_dict, key=hours_dict.get)
        print(f"Hour {most_popular_hour} has {hours_dict[most_popular_hour]} hits")
        del hours_dict[most_popular_hour]
    return "for all 24 hours of the day."


def main(url):
    print(f"Running main with URL = {url}...")
    filename = "weblog.csv"
    if download_file(url, filename):
        print(count_images(filename))
        print(count_browsers(filename))
        print(count_hours(filename))

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
