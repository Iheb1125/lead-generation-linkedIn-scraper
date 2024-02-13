from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url= 'https://www.linkedin.com/search/results/companies/?keywords=consulting&origin=CLUSTER_EXPANSION&sid=!Oe&page={page_number}'

driver = webdriver.Firefox()

driver.implicitly_wait(35)

# Initialize empty lists to store scraped data
industryname = []
locationname = []
linkname = []
companyname = []

# Loop through multiple pages
for page_number in range(1, 11):  # Adjust range as needed
    url1 = url.format(page_number=page_number)
    driver.get(url1)
    time.sleep(5)  # Add a short delay to let the page load

    # Scroll down to load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Add a short delay to let more results load

    # Find and scrape data from each company on the current page
    for i in range(1, 11):  # Assuming there are 10 results per page
        try:
            company_element = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f"li.reusable-search__result-container:nth-child({i})"))
            )
            
            link = company_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            industry_location = company_element.find_element(By.CSS_SELECTOR, f"li.reusable-search__result-container:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)").text
            industry, location = industry_location.split(" • ", 1) 
            company = company_element.find_element(By.CSS_SELECTOR, f"li.reusable-search__result-container:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > a:nth-child(1)").text
            
            industryname.append(industry)
            locationname.append(location)
            companyname.append(company)
            linkname.append(link)
        except Exception as e:
            print(f"Error while processing result {i} on page {page_number}: {str(e)}")

# Create DataFrame
result_df = pd.DataFrame({
    "Company": companyname,
    "Industry": industryname,
    "Location": locationname,
    "Link": linkname
})

# Print the DataFrame

print(result_df)


# Save data to a CSV and xlsx file
result_df.to_csv('linkedin.csv', index=False)
result_df.to_excel('linkedin.xlsx', index=False)
# Close the browser
driver.quit()
