from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape_linkedin():
    url= 'https://www.linkedin.com/search/results/companies/?keywords=consulting&origin=CLUSTER_EXPANSION&sid=!Oe&page={page_number}'
    driver = webdriver.Firefox()
    driver.implicitly_wait(35)

    industryname = []
    locationname = []
    linkname = []
    companyname = []

    for page_number in range(1, 11):
        url1 = url.format(page_number=page_number)
        driver.get(url1)
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        for i in range(1, 11):
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

    result_df = pd.DataFrame({
        "Company": companyname,
        "Industry": industryname,
        "Location": locationname,
        "Link": linkname
    })

    driver.quit()

    return render_template('results.html', data=result_df)

@app.route('/save', methods=['POST'])
def save_data():
    data = request.form['data']
    df = pd.read_html(data)[0]

    save_format = request.form['format']

    # Get the directory of the app.py file
    app_dir = os.path.dirname(os.path.abspath(__file__))

    if save_format == 'csv':
        csv_file = os.path.join(app_dir, 'linkedin.csv')
        df.to_csv(csv_file, index=False)
    elif save_format == 'xlsx':
        excel_file = os.path.join(app_dir, 'linkedin.xlsx')
        df.to_excel(excel_file, index=False)
    elif save_format == 'by_industry':
        for industry, group in df.groupby('Industry'):
            filename = f'{industry}_companies.xlsx'
            file_path = os.path.join(app_dir, filename)
            group.to_excel(file_path, index=False)

    # Re-render the results.html template with the same data
    return render_template('results.html', data=df)

if __name__ == '__main__':
    app.run(debug=True)
