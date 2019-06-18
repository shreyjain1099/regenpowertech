from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
chrome_path = r"C:\Users\Lenovo\Desktop\chromedriver.exe"

import datetime
start_date = datetime.date(2018, 10, 22)
end_date   = datetime.date(2019, 6, 14)
date = pd.date_range(start_date, end_date)
y = []
for testdate in date:
    z = datetime.datetime.strptime(str(testdate.date()), '%Y-%m-%d').strftime('%d-%m-%Y')
    y.append(z)

driver = webdriver.Chrome(chrome_path)
driver.get("http://scada.regenpowertech.com/Login.aspx")
time.sleep(1)
inputElement = driver.find_element_by_id("txtregenid")
inputElement.send_keys('ITCBH')
inputElement = driver.find_element_by_id("textpwd")
inputElement.send_keys('ITC@123')
driver.find_element_by_id("iblogin").click()

report = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_RadMenu"]/ul/li[2]/a')
hover = ActionChains(driver).move_to_element(report)
hover.perform()
driver.find_element_by_link_text('Daily').click()

for finaldates in y:
    try:
        dateinput = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder2_ContentPlaceHolder6_ContentPlaceHolder10_rdp_dateInput"]')
        dateinput.send_keys(finaldates)
        #driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder2_ContentPlaceHolder6_ContentPlaceHolder10_IBExport"]').click()
        #export key
        driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder2_ContentPlaceHolder6_ContentPlaceHolder10_IBView"]').click()
        table = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder3_ContentPlaceHolder7_ContentPlaceHolder11_UpdatePanel1"]')
        rows=table.text.split('\n')
        element=[]
        for r in rows:
            element.append([i for i in r.split(' ')])
        df=pd.DataFrame(element)
        df.columns=df.iloc[0]
        df=df.reindex(df.index.drop(0))
        temp = finaldates.replace("/", "_")
        df.to_csv(temp+".csv", index=False)
        ###
        report2 = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder1_RadMenu"]/ul/li[2]/a')
        hover2 = ActionChains(driver).move_to_element(report2)
        hover2.perform()
        driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder1_RadMenu"]/ul/li[2]/div/ul/li[4]/a').click()
    except:
        pass