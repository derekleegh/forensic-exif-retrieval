import argparse
import subprocess
import os

from geopy.geocoders import Nominatim
from exif import Image
from prettytable import PrettyTable


def setup_table(requiredInfo):
    table=PrettyTable()

    if requiredInfo == "exif":
        table.field_names=["fileName", "has EXIF data", 'model', 'make', 'datetime', "GPS Coordinates", "Address"]
    
    return table

def recover_dd(fileName) :
    #run subprocess to extract the dd via foremost
    print ("Performing dd extract")
    result = subprocess.run(["foremost", fileName, "-o", "recover"], capture_output=True, text=True)
    print(f"Result: {result.stdout}")

    if (result.stdout is None): 
        print("EXtraction succesful")

def process_files(requiredInfo, table):
    dir="recover"
    folders=os.listdir(dir)

    for folder in folders:
        if folder == "audit.txt":
            continue
        
        files=os.listdir(f"{dir}/{folder}")
        for file in files:
            print(f"Processing file: ({file}) from {folder} folder")
            file_dir=f"{dir}/{folder}/{file}"
            
            if requiredInfo == "exif":
                extract_exif(file_dir, file, requiredInfo, table)
    
def extract_exif(fileDir,fileName,requiredInfo,table):
    try:
        with open(fileDir, "rb") as f:
            img=Image(fileDir)
            has_exif=img.has_exif
            if has_exif:
                print(f"{fileName} contains exif data")
                
                # Extract coordinates
                coords = (decimal_coords(img.gps_latitude,
                                    img.gps_latitude_ref),
                                    decimal_coords(img.gps_longitude,
                                                    img.gps_longitude_ref))
                # Get Address from the coordinates       
                geoLoc = Nominatim(user_agent="GetLoc")
                locname = geoLoc.reverse(coords)
                table.add_row([fileName, "true", img.get('make'), img.get('model'), img.get("datetime_original"), coords, locname.address])
                return table
            else:
                table.add_row([fileName, "false","", "", "", "", ""])
    except Exception as e:
        print(f"Error: {e}")
        print(f"Ignoring {fileName} as it is not the target required Info: ({requiredInfo})")
        table.add_row([fileName, "false", "", "", "", "", ""])

def decimal_coords(coords, ref):
 decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
 if ref == "S" or ref == "W":
     decimal_degrees = -decimal_degrees
 return decimal_degrees

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="File Name with paths")
    parser.add_argument("--requiredInfo", help="Required type info to extract")
    args = parser.parse_args()

    

    table=setup_table(args.requiredInfo)
    recover_dd(args.filename)
    process_files(args.requiredInfo, table)
    print(table)
    with open(f"{args.filename}_results.csv", "w", newline="") as output:
        output.write(table.get_csv_string())

