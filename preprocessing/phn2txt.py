import os

# Root directory of TIMIT dataset
root_dir = "./timit/data"

def convert_phn_to_txt(phn_file_path):
    # Extract base and build new .txt file path
    base_path, phn_filename = os.path.split(phn_file_path)
    base_name = os.path.splitext(phn_filename)[0]
    txt_filename = f"{base_name}_1.txt"
    txt_file_path = os.path.join(base_path, txt_filename)

    # Convert .PHN to .txt (preserving times)
    with open(phn_file_path, "r", encoding="utf-8") as phn_file, open(txt_file_path, "w", encoding="utf-8") as txt_file:
        for line in phn_file:
            parts = line.strip().split()
            if len(parts) == 3:
                start_time, end_time, transcript = parts
                txt_file.write(f"{start_time} {end_time} {transcript}\n")

    print(f"✔️ Created: {txt_file_path}")


# Walk through directory tree and process all .PHN files
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".PHN"):  # Case-sensitive match
            phn_path = os.path.join(dirpath, filename)
            convert_phn_to_txt(phn_path)
