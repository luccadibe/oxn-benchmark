import pandas as pd
import json

# Load the CSV file
input_file = "data.csv"  # Replace with your file path
output_file = "clean.csv"  # Output file for SQLite import

# Read the CSV
df = pd.read_csv(input_file)

# Parse the 'all_alerts' column
def clean_all_alerts(json_str):
    try:
        # Ensure the value is a string before processing
        if isinstance(json_str, str):
            alerts = json.loads(json_str.replace('""', '"'))
            return json.dumps(alerts)  # Return valid JSON as string
        else:
            return None  # Handle non-string values gracefully
    except (json.JSONDecodeError, TypeError):
        return None  # Handle any invalid JSON gracefully

# Apply the cleaning function
if "all_alerts" in df.columns:
    df["all_alerts"] = df["all_alerts"].apply(clean_all_alerts)

# Save the cleaned CSV
df.to_csv(output_file, index=False)
print(f"Cleaned CSV saved to {output_file}")
