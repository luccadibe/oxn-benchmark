import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Connect to the SQLite database
db_path = 'db.db'
conn = sqlite3.connect(db_path)

# Load the data into a Pandas DataFrame
query = """
SELECT fault_name, fault_params, detection_latency, first_alert, 
       latency_threshold, evaluation_window
FROM table_name 
WHERE detected = 1 
  AND fault_name != 'add_security_context' 
  AND first_alert != 'KubernetesContainerOomKiller';
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Convert evaluation_window to numeric values (seconds)
df['evaluation_window'] = df['evaluation_window'].str.replace('s', '').astype(float)

# Extract numeric values from fault_params for package loss percentage or delay
df['fault_param_value'] = df['fault_params'].str.extract(r'(\d+\.?\d*)').astype(float)

# Set up the plot styles
sns.set(style="whitegrid")

# Plot 1: ECDF of Detection Latency for Package Loss Percentages
plt.figure(figsize=(10, 6))
package_lost_df = df[df['fault_name'] == 'package_lost_treatment']

# Plot ECDF for each loss percentage
for loss_pct in [15.0, 20.0]:
    data = package_lost_df[package_lost_df['fault_param_value'] == loss_pct]['detection_latency']
    # Calculate ECDF
    x = np.sort(data)
    y = np.arange(1, len(data) + 1) / len(data)
    plt.plot(x, y, label=f'Loss {loss_pct}%', marker='.')

plt.title('ECDF of Detection Latency by Package Loss Percentage')
plt.xlabel('Detection Latency (s)')
plt.ylabel('Cumulative Probability')
plt.legend(title='Package Loss')
plt.grid(True)
plt.savefig('detection_latency_ecdf.png')
plt.close()

# Plot 2: Detection Latency vs. Latency Threshold
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='latency_threshold', y='detection_latency', hue='fault_name', marker='o')
plt.title('Detection Latency by Latency Threshold')
plt.xlabel('Latency Threshold (ms)')
plt.ylabel('Detection Latency (s)')
plt.legend(title='Fault Type')
plt.savefig('detection_latency_by_threshold.png')
plt.close()

# Plot 3: Detection Latency by Evaluation Window
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='evaluation_window', y='detection_latency', hue='fault_name', ci=None)
plt.title('Detection Latency by Evaluation Window')
plt.xlabel('Evaluation Window (s)')
plt.ylabel('Detection Latency (s)')
plt.legend(title='Fault Type')
plt.savefig('detection_latency_by_eval_window.png')
plt.close()

# Plot 4: Distribution of Detection Latency by First Alert
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='first_alert', y='detection_latency', hue='fault_name')
plt.title('Distribution of Detection Latency by First Alert')
plt.xlabel('First Alert')
plt.ylabel('Detection Latency (s)')
plt.legend(title='Fault Type')
plt.xticks(rotation=45)
plt.savefig('detection_latency_by_first_alert.png')
plt.close()

