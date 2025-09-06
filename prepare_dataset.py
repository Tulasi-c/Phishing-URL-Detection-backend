# prepare_dataset.py
import os, sys, argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--input", default="raw_urls.csv", help="Path to raw CSV (default: raw_urls.csv)")
ap.add_argument("--output", default="urls_labels.csv", help="Path to cleaned output CSV (default: urls_labels.csv)")
args = ap.parse_args()

csv_path = args.input
if not os.path.exists(csv_path):
    print(f"\nERROR: input file not found: {csv_path}\n")
    sys.exit(1)

# Load CSV
df = pd.read_csv(csv_path)
print("Loaded CSV. Columns:", df.columns.tolist())

# Select first and last columns
if df.shape[1] < 2:
    print("ERROR: CSV must have at least two columns (URL and label).")
    sys.exit(1)

cleaned = df.iloc[:, [0, -1]].copy()
cleaned.columns = ['url', 'label']

# Map textual labels to 0/1
def norm_label(x):
    s = str(x).strip().lower()
    if s in ('phishing','malicious','bad','1','true','t','yes','y'):
        return 1
    if s in ('legitimate','legit','safe','benign','0','false','f','no','n'):
        return 0
    # fallback: numeric conversion
    try:
        return int(float(s))
    except:
        return 0

cleaned['label'] = cleaned['label'].apply(norm_label)

# Remove rows with missing URLs
cleaned = cleaned.dropna(subset=['url']).reset_index(drop=True)

# Save cleaned CSV
cleaned.to_csv(args.output, index=False)
print(f"✅ Saved cleaned dataset to {args.output} (rows: {len(cleaned)})")
