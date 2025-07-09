import os
import librosa
import numpy as np
import pandas as pd
from textgrid import TextGrid

# Parameters
base_dir = "timit_all"
splits = ["train", "test"]
target_phonemes = {
    "iy", "ih", "eh", "ey", "ae", "aa", "aw", "ay", "ah", "ao",
    "oy", "ow", "uh", "uw", "ux", "er", "ax", "ix", "axr", "ax-h"
}
n_mfcc = 13
hop_length = 512  # Default for librosa

def extract_mfccs(audio_path, tg_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, hop_length=hop_length)
    mfcc = mfcc.T  # Shape: (frames, 13)
    duration = librosa.get_duration(y=y, sr=sr)

    tg = TextGrid()
    tg.read(tg_path)
    phoneme_tier = tg[0]  # Only tier named "transcript"

    rows = []
    for interval in phoneme_tier.intervals:
        label = interval.mark.strip().lower()
        if label not in target_phonemes:
            continue
        start, end = interval.minTime, interval.maxTime
        if end > duration:
            continue

        start_idx = int(start * sr / hop_length)
        end_idx = int(end * sr / hop_length)
        mfcc_slice = mfcc[start_idx:end_idx]

        if mfcc_slice.shape[0] == 0:
            continue

        mfcc_avg = mfcc_slice.mean(axis=0)
        row = {
            "wav_file": os.path.basename(audio_path),
            "phoneme": label,
            "start_time": start,
            "end_time": end
        }
        for i in range(n_mfcc):
            row[f"mfcc_{i+1}"] = mfcc_avg[i]  # Use 1-based indexing
        rows.append(row)
    return rows

# Process each split
for split in splits:
    split_dir = os.path.join(base_dir, split)
    all_rows = []

    for root, _, files in os.walk(split_dir):
        wav_files = [f for f in files if f.lower().endswith(".wav")]
        for wav_file in wav_files:
            base = os.path.splitext(wav_file)[0]
            wav_path = os.path.join(root, wav_file)
            tg_path = os.path.join(root, base + ".TextGrid")
            if not os.path.exists(tg_path):
                continue
            rows = extract_mfccs(wav_path, tg_path)
            all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    df.to_csv(f"mfcc_{split}_phoneme_clean_sorted.csv", index=False)
