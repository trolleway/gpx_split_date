import sys
import re
from datetime import datetime, timedelta
import os

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_dates.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    
    resultdir='split'
    
    unique_dates = extract_dates(filename)
    print("Unique dates found:")

    for date in sorted(unique_dates):
        print(date)
        
    for date_string in sorted(unique_dates):
        date_object = datetime.strptime(date_string, "%Y-%m-%d")  # Convert string to datetime object
        start_date_string = date_object.strftime("%Y%m%d%H%M%S")
        new_date = date_object + timedelta(days=1)  # Add one day
        end_date_string = new_date.strftime("%Y%m%d%H%M%S")  # Convert back to string
        cmd = f'''gpsbabel -i gpx -f {filename} -o gpx  -x "track,start={start_date_string},stop={end_date_string}"  -F {resultdir}/{date_string[:10]}.gpx '''
        
        print(cmd)
        os.system(cmd)
        
        #gpsbabel -i gpx -f merge.gpx -o gpx -x track,start=202505090000,stop=20250510000000 -F 2025-05-09.gpx


