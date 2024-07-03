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
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def bot_setup():
    options = Options()
    options.add_argument("--no-sandbox") 
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-notifications')
    # options.add_argument('--incognito')
    # options.add_argument('--disable-logging')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
     # Bypass OS security model, WARNING: NOT RECOMMENDED FOR PRODUCTION
    # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    # options.add_argument("--remote-debugging-port=9222") 

   
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    logging.info("Driver Initilize")
    return driver

def scrap_data(driver, url, input1, input2 ):
    try: 
        wait = WebDriverWait(driver, 10)

        driver.get(url)
        print(driver.current_url)
        logging.info("get url")     
        tracking_input_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div[3]/div/div/div[2]/div/div/form/div[1]/div/div')))
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div[3]/div/div/div[2]/div/div/form/div[2]/button')))
        data = input1+"-"+input2
        tracking_input_field.send_keys(data)
        submit_button.click()
        data=[]
        print("done")  # This will now print after actions are successful
        logging.info("Clicked on track button")
        # try: 
        #     station = driver.find_element(By.XPATH, '//*[@id="trackShiptablerow00"]/td[3]')
        #     elements = driver.find_element(By.XPATH, '//*[@id="trackShiptablerow0"]/td[2]')
        #     details = elements.text
        #     lines = details.strip().split('\n')
        #     for line in lines:
        #         values={}
        #         values["status"]=line
        #         values["location"]=station.text
        #         data.append(values)
        #     return data
        # except TimeoutError as e:
            # driver.quit()
            # return {"Error":e} 
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

    url="https://www.iagcargo.com/en/home/"
    driver = bot_setup()
    data= scrap_data(driver, url, input1, input2)
    # try: 
    #     sendMail.send_mail(data)
    # except Exception as e:
    #     print("Error in sending mail ", e)
    current_url = driver.current_url
    driver.quit()
    print("Redirecting to Google.")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
