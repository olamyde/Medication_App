import pandas as pd

# Read the Excel file
file_path = '/mnt/data/Medication Remedies and Generic Names.xlsx'
df = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
import ace_tools as tools; tools.display_dataframe_to_user(name="Medication Data", dataframe=df)
