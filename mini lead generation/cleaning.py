import pandas as pd

# Read the CSV file generated by your scraping script
scraped_data = pd.read_csv('linkedin.csv')

# Organize companies with the same industry into one separate file
for industry, group in scraped_data.groupby('Industry'):
    filename = f'{industry}_companies.xlsx'
    group.to_excel(filename, index=False)
