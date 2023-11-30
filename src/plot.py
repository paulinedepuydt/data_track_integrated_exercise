import os.path
import pandas as pd
import seaborn as sns

csv_files = [fn for fn in os.listdir("../ts.csv") if fn.endswith("csv")]
ts = pd.read_csv(f"ts.csv/{csv_files[0]}")

sns.barplot(data=ts, x="datetime", y="value")
