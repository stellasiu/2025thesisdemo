import os
import shutil

# Paths
source_root = "./timit/data/"
target_dir = "./timit_all/"

# Create target directory if it doesn"t exist
os.makedirs(target_dir, exist_ok=True)

# Walk through the source directory
for root, dirs, files in os.walk(source_root):
    for file in files:
        if file.lower().endswith((".wav", ".textgrid")):
            full_path = os.path.join(root, file)
            
            # Extract parts of the path
            relative_path = os.path.relpath(full_path, source_root)
            parts = relative_path.split(os.sep)

            if len(parts) >= 4:
                # parts: [TRAIN or TEST], DRX, SPEAKER, FILENAME
                dataset = parts[0].lower()    # "train" or "test"
                dr = parts[1].lower()          # "dr1-dr8"
                speaker = parts[2]             # speaker folder name
                original_filename = os.path.splitext(parts[3])[0]  # filename without extension
                
                # New filename format
                new_filename = f"{dataset}_{dr}_{speaker}_{original_filename}{os.path.splitext(file)[1]}"
                new_path = os.path.join(target_dir, new_filename)
                
                shutil.copy(full_path, new_path)
                print(f"Copied {full_path} --> {new_path}")
            else:
                print(f"Skipping {full_path}: Path too short.")

print("All files copied and renamed correctly with underscores!")
