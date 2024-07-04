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
import srilankanskychain, unitconversio 
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def bot_setup():
    options = Options()
    options.add_argument("--no-sandbox") 
    options.add_argument('--headless')
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
                
        code_input_field = wait.until(EC.presence_of_element_located((By.ID, 'txtPrefix')))
        print("line 44")
        tracking_input_field = wait.until(EC.presence_of_element_located((By.ID, 'TextBoxAWBno')))
        print("line 46")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ButtonGO"]')))
        print("line 48")
        code_input_field.send_keys(input1)
        tracking_input_field.send_keys(input2)
        submit_button.click()
        data=[]
        print("done")  # This will now print after actions are successful
        logging.info("Clicked on track button")
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
                # for i in range(0, len(tablehead)):
                #     print(tablehead[i].text)
                #     data[tablehead[i].text]=tablehead[i].text
                
                # table one
                row = driver.find_elements(By.XPATH, "//*[@id='gvBkAcInfo']/tbody/tr")
                col = driver.find_elements(By.XPATH, "//*[@id='gvBkAcInfo']/tbody/tr[2]/td")

                print("col= ",len(col), " row=", len(row))
                for i in range(2, len(row)+1):
                    # time.sleep(3)
                    values={}
                    for j in range(1, len(col)+1):
                        # wait.until(EC.presence_of_element_located(By.XPATH, f'//*[@id="GridViewAwbTracking"]/tbody/tr[2]/td'))
                        key = driver.find_element(By.XPATH, f'//*[@id="gvBkAcInfo"]/tbody/tr[1]/th[{j}]').text
                        value = driver.find_element(By.XPATH, f'//*[@id="gvBkAcInfo"]/tbody/tr[{i}]/td[{j}]').text
                        # print (key," :", value)
                        values[key]=value
                    data.append({'status': f"{values['Status']} at {values['Station']}, Flight#: {values['Flight#']}, pcs: {values['Pcs']}, Weight: {values['Weight']}, Dest: {values['Dest']}",
                                 'date': values['Event Date-Time'],
                                 'location': values['Station']})

                # table two    
                row = driver.find_elements(By.XPATH, "//*[@id='GridViewAwbTracking']/tbody/tr")
                col = driver.find_elements(By.XPATH, "//*[@id='GridViewAwbTracking']/tbody/tr[2]/td")

                print("col= ",len(col), " row=", len(row))
                for i in range(2, len(row)+1):
                    # time.sleep(3)
                    values={}
                    for j in range(1, len(col)+1):
                        # wait.until(EC.presence_of_element_located(By.XPATH, f'//*[@id="GridViewAwbTracking"]/tbody/tr[2]/td'))
                        key = driver.find_element(By.XPATH, f'//*[@id="GridViewAwbTracking"]/tbody/tr[1]/th[{j}]').text
                        value = driver.find_element(By.XPATH, f'//*[@id="GridViewAwbTracking"]/tbody/tr[{i}]/td[{j}]').text
                        # print (key," :", value)
                        values[key]=value
                    data.append({'status': f"{values['Milestone']} at {values['Station']}, Flight#: {values['Flight#']}{values['Flight Date']}, pcs: {values['Pcs']}, Weight: {values['Weight']}, Dest: {values['Dest']}, ULD: {values['ULD']}",
                                 'date': values['Event Date-Time'],
                                 'location': values['Station']})
                print(data)
                # return data
                return {"success": True, "message": "Successfully Scrap data from web","result":data, "length":len(data)} 
            else:
                print("No data for this number")
                return {"success": False, "message": "No data for this number","result":[], "length":0} 
                # return {"massege": "No data for this number"}
        except TimeoutError as e:
            driver.quit()
            return {"success": False, "message": "An Error occured","result":[{"Error":str(e)}]} 
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        driver.quit()
        return {"success": False, "message": "Failed to automate web form.","result":[{"Error": str(e)}]}  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currency', methods=['GET'])
def currency():
    url = "https://instantforex.icicibank.com/instantforex/forms/MicroCardRateView.aspx"
    driver = bot_setup()
    data = unitconversio.get_currency(url, driver)
    driver.quit()
    return jsonify(data)

@app.route('/scrap_data', methods=['POST'])
def save_data():
    
    data = request.json
    if 'prefix' not in data or not data['prefix'] or 'number' not in data or not data['number']:
        return jsonify({"success": False, "message": "Please enter prefix and number","result":[]})
    input1 = data['prefix']
    input2 = data['number']
    if len(input1)!=3 or len(input2)!=8:
        return jsonify({"success": False, "message": "Please enter valid prefix or number","result":[]})
    if input1=="312":
        url="https://6ecargo.goindigo.in/FrmAWBTracking.aspx"
        driver = bot_setup()
        data= scrap_data(driver, url, input1, input2)
    elif input1 =="603":
        url="http://www.srilankanskychain.aero/skychain/app?service=page/nwp:Trackshipmt"
        driver = bot_setup()
        data= srilankanskychain.scrap_data(driver, url, input1, input2)
    # try: 
    #     sendMail.send_mail(data)
    # except Exception as e:
    #     print("Error in sending mail ", e)
    driver.quit()
    print("Redirecting to Google.")
    return jsonify(data)
    


if __name__ == '__main__':
    app.run(debug=True)
