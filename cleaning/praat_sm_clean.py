import pandas as pd

# Load CSV files
height_df = pd.read_csv("./heightcm.csv")
sm_test_df = pd.read_csv("./praat_sm_test.csv")
sm_train_df = pd.read_csv("./praat_sm_train.csv")

# Function to parse the `file` column and extract new fields
def parse_file_info(df):
    parsed = df["file"].str.extract(r"(test|train)_dr(\d)_([FM])([A-Z0-9]+)_(\w+)")
    df["set"] = parsed[0]
    df["dr"] = parsed[1].astype(int)
    df["speaker_id"] = parsed[3]
    df["file_part"] = parsed[4]
    return df

# Apply parsing
sm_test_df = parse_file_info(sm_test_df)
sm_train_df = parse_file_info(sm_train_df)

# Merge with height data
sm_test_df = sm_test_df.merge(height_df, left_on="speaker_id", right_on="ID", how="left")
sm_train_df = sm_train_df.merge(height_df, left_on="speaker_id", right_on="ID", how="left")

# Drop extra ID column
sm_test_df.drop(columns=["ID"], inplace=True)
sm_train_df.drop(columns=["ID"], inplace=True)

# Define final column order and rename
final_columns = ["set", "dr", "speaker_id", "file_part", "height_cm", "phoneme", "M1", "M2", "M3", "M4"]
sm_test_df = sm_test_df[final_columns]
sm_train_df = sm_train_df[final_columns]


# Save to new CSVs if needed
sm_test_df.to_csv("processed_sm_test.csv", index=False)
sm_train_df.to_csv("processed_sm_train.csv", index=False)
