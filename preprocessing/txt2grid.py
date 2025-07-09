import os
import csv
import textgrid

# Root directory of TIMIT dataset
root_dir = "./timit/data"

def convert_txt_to_textgrid(txt_file_path):
    base_path, txt_filename = os.path.split(txt_file_path)

    if not txt_filename.endswith("_1.txt"):
        return  # Sanity check

    # Strip "_1" and get base name
    base_name = txt_filename[:-6]  # Removes "_1.txt"
    textgrid_filename = base_name + ".TextGrid"
    textgrid_path = os.path.join(base_path, textgrid_filename)

    # Read the _1.txt file
    with open(txt_file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=" ", fieldnames=["start_time", "end_time", "transcript"])
        data = [row for row in reader]

    # Create TextGrid and tier
    tg = textgrid.TextGrid()
    transcript_tier = textgrid.IntervalTier(name="transcript")

    for row in data:
        try:
            start_time = float(row["start_time"])
            end_time = float(row["end_time"])
            label = row["transcript"]
            transcript_tier.add(start_time, end_time, label)
        except ValueError:
            continue  # Skip malformed lines

    tg.append(transcript_tier)

    # Save .TextGrid
    with open(textgrid_path, "w", encoding="utf-8") as f:
        tg.write(f)

    # Remove the temporary _1.txt file
    os.remove(txt_file_path)

    print(f"✔️ Converted: {txt_filename} → {textgrid_filename} (and deleted {txt_filename})")


# Walk through directory and process all *_1.txt files
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith("_1.txt"):
            txt_path = os.path.join(dirpath, filename)
            convert_txt_to_textgrid(txt_path)
