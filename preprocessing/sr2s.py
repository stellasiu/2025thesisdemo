import os

# Set the base directory
base_dir = "./timit/data"
sample_rate = 16000

# Walk through TRAIN and TEST
def process_phn_files(base_dir):
    for split in ["TRAIN", "TEST"]:
        split_dir = os.path.join(base_dir, split)
        for root, dirs, files in os.walk(split_dir):
            for file in files:
                if file.endswith(".PHN"):
                    file_path = os.path.join(root, file)
                    print(f"Processing: {file_path}")
                    process_single_phn(file_path)

# Process a single .PHN file
def process_single_phn(file_path):
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                start_sample, end_sample, label = parts
                start_sec = float(start_sample) / sample_rate
                end_sec = float(end_sample) / sample_rate
                lines.append(f"{start_sec:.6f}\t{end_sec:.6f}\t{label}")

    # Rewrite the file with headers and new data
    with open(file_path, 'w') as f:
        f.write("start_time\tend_time\ttranscript\n")
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    process_phn_files(base_dir)
    print("All .PHN files have been updated.")
