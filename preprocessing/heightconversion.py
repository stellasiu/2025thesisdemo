import re
import csv

def height_to_cm(height_str):
    match = re.match(r"(\d+)'(\d+)", height_str)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        total_inches = feet * 12 + inches
        cm = round(total_inches * 2.54, 2) # Round off to 2 decimal places
        return cm
    return None

input_file = "./timit/SPKRINFO.TXT"
output_file = "./height_cm.csv"

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["ID", "Height_cm"])
    
    for line in infile:
        if line.strip().startswith(";") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 7:
            speaker_id = parts[0]
            height_str = parts[6]
            height_cm = height_to_cm(height_str)
            if height_cm:
                writer.writerow([speaker_id, height_cm])
