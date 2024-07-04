from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re

def get_currency(url, driver):
    try: 
        wait = WebDriverWait(driver, 10)

        driver.get(url)
        table = wait.until(EC.presence_of_all_elements_located((By.ID, 'dgMicroRateCard')))     
        row = driver.find_elements(By.XPATH, '//*[@id="dgMicroRateCard"]/tbody/tr')
        print(len(row))
        data=[]
        for i in range(3,len(row)+1):
            text= driver.find_element(By.XPATH, f'//*[@id="dgMicroRateCard"]/tbody/tr[{i}]/td[1]').text
            pattern = r'\((.*?)\)'
            # Extracting currency codes
            currency_codes = re.search(pattern, text).group(1) 
            data.append({
                'currency': currency_codes,
                'buying_rate':driver.find_element(By.XPATH, f'//*[@id="dgMicroRateCard"]/tbody/tr[{i}]/td[2]').text,
                'selling_rate':driver.find_element(By.XPATH, f'//*[@id="dgMicroRateCard"]/tbody/tr[{i}]/td[7]').text,
            })
            
        logging.info("Clicked on track button")
        # print (data)
        return {"success": True, "message": "Successfully Scrap data from web","result":data, "length":len(data)}  
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        driver.quit()
        return {"success": False, "message": "Failed to automate web form.","result":[{"Error": str(e)}]}  

