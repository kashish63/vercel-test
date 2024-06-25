from flask import Flask, render_template, request, jsonify, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sendMail
import chromedriver_autoinstaller
import os
import requests
import subprocess
import zipfile
app = Flask(__name__)



def bot_setup():
    options = Options()
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-notifications')
    # options.add_argument('--incognito')
    # options.add_argument('--disable-logging')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--no-sandbox")  # Bypass OS security model, WARNING: NOT RECOMMENDED FOR PRODUCTION
    # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    # options.add_argument("--remote-debugging-port=9222") 

    # service = Service(ChromeDriverManager())  
    # chrome_driver_path = chromedriver_autoinstaller.install()

    # Initialize the Chrome driver with the service object
    driver = webdriver.Chrome(options=options)
    # chromedriver_autoinstaller.install()
    # driver = webdriver.Chrome(options=options) 
    driver.implicitly_wait(10)
    return driver

def scrap_data(driver, url, input1, input2 ):
    try: 
        wait = WebDriverWait(driver, 10)

        driver.get(url)
                
        code_input_field = wait.until(EC.presence_of_element_located((By.ID, 'txtPrefix')))
        print("line 44")
        tracking_input_field = wait.until(EC.presence_of_element_located((By.ID, 'TextBoxAWBno')))
        print("line 46")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ButtonGO"]')))
        print("line 48")
        code_input_field.send_keys(input1)
        tracking_input_field.send_keys(input2)
        submit_button.click()
        data={}
        print("done")  # This will now print after actions are successful
        try: 
            # wait.until(EC.presence_of_element_located(By.ID, 'contentarea_tracking'))
            element = driver.find_element(By.ID,"contentarea_tracking")
            time.sleep(10) 
            print("Line 58")  
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tableTitle = soup.find_all("tr",{"class":"titlecolr"})
            print("two tables", len(tableTitle))
            if len(tableTitle)>0:
                tablehead = driver.find_elements(By.XPATH, "//*[@id='gvBkAcInfo']/tbody/tr[1]/th")
                for i in range(0, len(tablehead)):
                    print(tablehead[i].text)
                    data[tablehead[i].text]=tablehead[i].text

                row = soup.find_all("tr", {"class": "newstyle-tr"})
                # col = soup.find_all("td", {"xpath":"//*[@id='gvBkAcInfo']/tbody/tr[2]/td"})
                col = driver.find_elements(By.XPATH, "//*[@id='gvBkAcInfo']/tbody/tr[2]/td")

                print("col= ",len(col), " row=", len(row))
                # for i in range(1, len(elements)+1):
                    # time.sleep(3)
                    # wait.until(EC.presence_of_element_located(By.XPATH, f'//*[@id="cargotracker"]/div[2]/app-cargo-track-history/div/div/div[2]/div[2]/div/ul/li[{i}]/p[1]'))

                    # data1 = driver.find_element(By.XPATH, f'//*[@id="cargotracker"]/div[2]/app-cargo-track-history/div/div/div[2]/div[2]/div/ul/li[{i}]/p[1]').text
                    # data2 = driver.find_element(By.XPATH, f'//*[@id="cargotracker"]/div[2]/app-cargo-track-history/div/div/div[2]/div[2]/div/ul/li[{i}]/p[2]').text

                #     print (data1," :", data2)
                return data
            else:
                print("No data for this number")
                return {"massege": "No data for this number"}
        except TimeoutError as e:
            driver.quit()
            return {"Error":e} 
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        driver.quit()
        return {{'error': 'Failed to automate web form.', 'exception': str(e)}} 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json
    input1 = data['input1']
    input2 = data['input2']

    url="https://6ecargo.goindigo.in/FrmAWBTracking.aspx"
    driver = bot_setup()
    data= scrap_data(driver, url, input1, input2)
    try: 
        sendMail.send_mail(data)
    except Exception as e:
        print("Error in sending mail ", e)
    current_url = driver.current_url
    driver.quit()
    print("Redirecting to Google.")
    return jsonify({'redirect_url': current_url })

if __name__ == '__main__':
    app.run(debug=True)
