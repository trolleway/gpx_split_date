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
    
def count_substring_in_file(filename:str, substring:str):
    try:
        with open(filename, "r") as file:
            content = file.read()
            count = content.count(substring)
            return count
            
    except FileNotFoundError:
        return -1  # Or handle the error as needed
    return 0
    
def split_gpx_by_dates(filename:str,resultdir:str,unique_dates:list, timezone_text:str=''):

    from pathlib import Path
    Path(resultdir).mkdir(parents=True, exist_ok=True)

    for date_string in sorted(unique_dates):
        date_object = datetime.strptime(date_string, "%Y-%m-%d")  # Convert string to datetime object
        
        date_object = date_object - parse_timedelta(timezone_text)
        
        start_date_string = date_object.strftime("%Y%m%d%H%M%S")
        new_date = date_object + timedelta(days=1)  # Add one day
        end_date_string = new_date.strftime("%Y%m%d%H%M%S")  # Convert back to string
        track_filename=f'{resultdir}/{date_string[:10]}.gpx'
        cmd = f'''gpsbabel -i gpx -f {filename} -o gpx  -x "track,start={start_date_string},stop={end_date_string},title="%Y%m%d""  -F {track_filename} '''
        
        print(cmd)
        os.system(cmd)
        
        # check if result gpx has any trkpoints
        if (count_substring_in_file(track_filename,'trkpt') > 1) == False:
            os.remove(track_filename)
        
        #gpsbabel -i gpx -f merge.gpx -o gpx -x track,start=202505090000,stop=20250510000000 -F 2025-05-09.gpx
        
        '''
        gpsbabel -i gpx -f split/2025-05-17.gpx -o unicsv   -F split/2025-05-17.txt
        '''

def parse_arguments():
    parser = argparse.ArgumentParser(description="Split GPX tracks by day and store in a directory.")

    parser.add_argument("gpx", type=str, help="Path to the input GPX file.")
    parser.add_argument(
        "--timezone",
        type=str,
        default="0:00:00",
        help="Optional timezone offset in the format 'H:M:S', representing a Python timedelta string."
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
        
    split_gpx_by_dates(filename=filename,resultdir=resultdir,unique_dates=unique_dates, timezone_text=timezone_text)
    
    


