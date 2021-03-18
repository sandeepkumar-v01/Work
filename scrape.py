# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:15:24 2021

@author: Sandeep Kumar
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd



RESPONSE_WAIT_TIME_SEC = 5
letter = [input("Please Enter a Keyword to Search : ")]
#letter = ['ae','bc','cd'] #Input Manually

def load_page():
    driver.get("http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx")
    
    keyword_radio = driver.find_element_by_xpath("//input[@id='optlist_0']")
    keyword_radio.click()
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)

driver = webdriver.Chrome()
load_page()


headers = ['Affiliation Number', 'Name', 'Head/Principal Name', 'Status', 'Affiliated up to', 'Address', 'Phone No.',
           'Email', 'Website']

for i in range(0, len(letter)):
    
    df = pd.DataFrame(columns=headers)
   
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)
    
    driver.find_element_by_id("keytext").send_keys(letter[i])
    
    driver.find_element_by_xpath("//input[@id='search']").click()
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)

    tot_schools = int(driver.find_element_by_xpath("//span[@id='lbltot']").text)
    tot_pages = int(tot_schools / 25) + 1

    for k in range(tot_pages):
      
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        schools = soup.select("table#T1 > tbody > tr > td > table")
        
        for school in schools:
            cols = school.tbody.tr.find_all('td', recursive=False)
            col_1, col_2 = cols[1], cols[2]

            col_1_data = col_1.select("table > tbody > tr")
            col_2_data = col_2.select("table > tbody > tr")
            
            try:
                aff_no = col_1_data[0].select("td")[0].contents[1]
            except IndexError:
                aff_no = ''
            
            try:
                name = col_1_data[1].select("td > a")[0].contents[0]
            except IndexError:
                name = ''
            
            try:
                principal_name = col_1_data[2].select("td")[0].contents[1]
            except IndexError:
                principal_name = ''
            
            try:
                status = col_1_data[3].select("td")[0].contents[1]
            except IndexError:
                status = ''
            
            try:
                aff_upto = col_1_data[4].select("td")[0].contents[1].strip()
            except IndexError:
                aff_upto = ''
            
            try:
                address = ' '.join(col_2_data[0].select("td")[0].contents[1].strip().split())
            except IndexError:
                address = ''
            
            try:
                phone_no = ' '.join(col_2_data[1].select("td")[0].contents[1].strip().split())
            except IndexError:
                phone_no = 0
            
            try:
                e_mail = col_2_data[2].select("td")[0].contents[2].strip()
            except IndexError:
                e_mail = ''
            try:
                website = col_2_data[2].select("td")[0].contents[5].strip()
            except IndexError:
                website = ''

            
            df.loc[len(df)] = ([aff_no, name, principal_name, status, aff_upto, address, phone_no, e_mail, website])
        
        btn_next = driver.find_element_by_xpath("//input[@id='Button1']")
        driver.execute_script("arguments[0].click();", btn_next)
    

    name_sorted_df = df.sort_values(by=['Name'], ascending=True)

    
    csv_name = 'Keyword_'+letter[i]+'.csv'
    csv_loc = "Storage/"+csv_name
    name_sorted_df.to_csv(csv_loc, index=False)
    
    
    load_page()
    
driver.close()
