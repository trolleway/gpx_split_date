import sys
import re
from datetime import datetime, timedelta, timezone
import os
import argparse

def extract_dates(filename):
    # This pattern matches <time> followed by any characters (at least 10), but we only need the first 10.
    # It captures exactly the first 10 characters after <time>
    pattern = re.compile(r"<time>(.{10})")
    dates = set()

    with open(filename, "r", encoding="utf-8") as file:
        # read the file line by line to handle huge files efficiently
        for line in file:
            # find all occurrences in the current line
            matches = pattern.findall(line)
            for date in matches:
                dates.add(date)
    return dates

def parse_timedelta(time_str):
    sign = -1 if time_str.startswith('-') else 1
    hours, minutes = map(int, time_str[1:].split(':'))
    return timedelta(hours=hours * sign, minutes=minutes * sign)
    
def split_gpx_by_datesfilename(filename:str,resultdir:str,unique_dates:list, timezone_text:str=''):

    for date_string in sorted(unique_dates):
        date_object = datetime.strptime(date_string, "%Y-%m-%d")  # Convert string to datetime object
        
        date_object = date_object + parse_timedelta(timezone_text)
        
        start_date_string = date_object.strftime("%Y%m%d%H%M%S")
        new_date = date_object + timedelta(days=1)  # Add one day
        end_date_string = new_date.strftime("%Y%m%d%H%M%S")  # Convert back to string
        cmd = f'''gpsbabel -i gpx -f {filename} -o gpx  -x "track,start={start_date_string},stop={end_date_string}"  -F {resultdir}/{date_string[:10]}.gpx '''
        
        print(cmd)
        os.system(cmd)
        
        #gpsbabel -i gpx -f merge.gpx -o gpx -x track,start=202505090000,stop=20250510000000 -F 2025-05-09.gpx

def parse_arguments():
    parser = argparse.ArgumentParser(description="Split GPX tracks by day and store in a directory.")

    parser.add_argument("gpx", type=str, help="Path to the input GPX file.")
    parser.add_argument(
        "--timezone",
        type=str,
        default="0:00:00",
        help="Optional timezone offset in the format 'H:M:S', representing a Python timedelta string."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="output",
        help="Directory where the split GPX tracks will be stored."
    )

    return parser.parse_args()
    

if __name__ == "__main__":
    args = parse_arguments()

    filename = args.gpx
    
    resultdir='split'
    
    timezone_text=args.timezone
    
    unique_dates = extract_dates(filename)
    print("Unique dates found:")

    for date in sorted(unique_dates):
        print(date)
        
    split_gpx_by_dates(filename=filename,resultdir=resultdir,unique_dates=unique_gates, timezone_text=timezone_text)
    
    


