import pandas as pd
from datetime import datetime

# Load the provided Excel file
file_path = 'linki do naczep.xlsx'
df_links = pd.read_excel(file_path)

# Display the column names to identify the correct name
print(df_links.columns.tolist())

# Adjust these names based on the actual column names in your file
numer_column_name = 'Numer'  # Zmień to na faktyczną nazwę kolumny z numerami
link_column_name = 'Link'    # Zmień to na nazwę kolumny, gdzie chcesz umieścić linki

# Define the base URL format
base_url = "https://elcar-online.pl/#/history/{}/{}T00:00:00+02:00/{}T23:59:59+02:00"

# Get the current date in the required format and add one day
current_date = datetime.now().strftime("%Y-%m-%d")

# Function to create links, skipping empty rows
def create_link(numer):
    if pd.isna(numer):
        return ''
    url = base_url.format(numer, current_date, current_date)
    return f'=HYPERLINK("{url}", "link do map")'

# Create the links
df_links[link_column_name] = df_links[numer_column_name].apply(create_link)

# Save the updated DataFrame to a new Excel file
output_file_path_links = 'updated_links_with_buttons.xlsx'
df_links.to_excel(output_file_path_links, index=False, engine='openpyxl')

print("Updated links saved to:", output_file_path_links)
