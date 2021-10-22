#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
#from tqdm import tqdm_notebook as tqdmn
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import pandas as pd
import folium
import time, re
import csv
import os


# In[2]:


#enter path of csv file that contains the list of keywords
user_input = input("Enter path: ")
assert os.path.exists(user_input), "file not at, "+str(user_input)


# In[3]:

#adding such useless comments which aren't even helpful, just plain annoying
fields=[]
rows=[]
with open(user_input) as cf:
    csv_read=csv.reader(cf, delimiter=',')
    fields=next(csv_read)
    for row in csv_read:
        rows.append(row)


# In[4]:


def scrape_info(a,i,done):
    try:
        loc_name.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div:nth-child(1) > h1 > span:nth-child(1)').text)
    except NoSuchElementException:
        loc_name.append(np.nan)
        
    try:
        category.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div.section-hero-header-title-description-container > div > div:nth-child(2) > span.section-rating-term > span:nth-child(1) > button').text)
    except NoSuchElementException:
        category.append(np.nan)
    
    time.sleep(2)
    try:
        address.append(driver.find_element_by_css_selector('button[data-tooltip="Copy address"]').text)
    except NoSuchElementException:
        address.append(np.nan)  
        
    time.sleep(2)
    try:
        element=driver.find_element_by_css_selector('button[data-tooltip="Open website"]')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        ActionChains(driver).move_to_element(element).perform()
        web_link.append(driver.find_element_by_css_selector('button[data-tooltip="Open website"]').text)
    except NoSuchElementException:
        web_link.append(np.nan)
        print("No web address found..")

    time.sleep(2)
    try:
        phone_no.append(driver.find_element_by_css_selector('button[data-tooltip="Copy phone number"]').text)
    except NoSuchElementException:
        phone_no.append(np.nan)

    try:
        rev_no.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.jqnFjrOWMVU__root > div > div.jqnFjrOWMVU__right > div.gm2-display-2').text)
    except NoSuchElementException:
        rev_no.append(np.nan)
    
    try:
        tot_rate.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.jqnFjrOWMVU__root > div > div.jqnFjrOWMVU__right > button').text)
    except NoSuchElementException:  
        tot_rate.append(np.nan)
    input_place.append(start_sear)
    done=True
    return loc_name, web_link, category, phone_no, address, rev_no, tot_rate, done


# In[5]:


def button_click():
    next_click=True
    cli_text=""
    try:
        cli_text=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[1]').text
         
    except (ElementClickInterceptedException, NoSuchElementException):
        next_click= False
    if cli_text=='No results found':
        print("next place")
        next_click=False
    return next_click


# In[ ]:


#declaring empty lists to store scraped values 
input_place=[]
loc_name=[]
web_link=[]
category=[]
phone_no=[]
address=[]
rev_no=[]
tot_rate=[]

#install chromedriver before this step
driver=webdriver.Chrome("C:\\chromedriver.exe")
d=0


fields=[]
rows=[]
with open(user_input) as cf:
    csv_read=csv.reader(cf, delimiter=',')
    fields=next(csv_read)
    for row in csv_read:
        rows.append(row)
        
for esc_room in rows:
    #takes the value from csv file iputted till the last element
    start_sear = str(esc_room)
    #if you want individual results you can declare the "start_search" string such as start_search="required keyword"
    url="https://www.google.com/maps/search/" + start_sear 
    driver.get(url)
    
    time.sleep(5)
    #check_i=False
    #while(check_i!=True):
    try:
            #reads value of number of search results on the first page 
        i=driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.n7lv7yjyC35__root > div > div:nth-child(1) > span > span:nth-child(2)').text
        i=int(i)                        
        #check_i=True                   
    except:
    #        check_i=False
        print("checking i..")
        continue
    print("after conv",i)
    #to subtract later when we click the next triangle button
    r=i
    
    for a in range (0,(i+40)): 
        cli_text=''
        url_ch=''
        ad_find=''
        if (a>i):
            time.sleep(3)
            try:
                print("clicking next button")
                #clicking the next button to check if they have more results
                next_click=driver.find_element_by_css_selector('#n7lv7yjyC35__section-pagination-button-next > span')
                next_click.click()                       
                time.sleep(10)                           
            except (ElementClickInterceptedException, NoSuchElementException, TimeoutException):
                #if the button is not clickable, it could mean there are no more results
                break
            time.sleep(5)
            
            if (button_click()): #function is written above
                print("more searches to scrape")
                time.sleep(5)
                #if the function returns a true value, there are more results on the next page. So we store the last value, of the number of results on next page in d
                time.sleep(3)
                try:
                    d=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/span/span[2]').text
                    d=int(d)
                except:
                    continue
                #we get the url of this page as we have to scrape all the info from here
                
            else:
                break
            #to set the value of i for the loop
            i=d-r
            #resetting a. but i don't think it is working
            a=1
            r=d
            for a in range (1,i+1):
                if(a>i):
                    time.sleep(3)
                    try:
                        print("clicking next button")
                #clicking the next button to check if they have more results
                        driver.find_element_by_css_selector('#n7lv7yjyC35__section-pagination-button-next > span').click()
                        time.sleep(5)
                    except (ElementClickInterceptedException,NoSuchElementException,TimeoutException):
                #if the button is not clickable, it could mean there are no more results
                        break
                    time.sleep(5)
            
                    if (button_click()): #function is written
                        print("more searches to scrape")
                        time.sleep(5)
                #if the function returns a true value, there are more results on the next page. So we store the last value, of the number of results on next page in d
                        try:
                            d=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/span/span[2]').text
                            d=int(d)
                        except:
                            continue
                #we get the url of this page as we have to scrape all the info from here
            
                    else:
                        break
                    #to set the value of i for the loop
                    i=d-r
            #resetting a
                    a=1
                    r=d
                    
                a=(a*2)+1
                try: #waiting for the title element of places after entering our url 
                    WebDriverWait(driver,25).until(EC.visibility_of_element_located((By.CLASS_NAME, "section-result-title")))
                except:
                    pass
                try: #to scrape ads
                    ad_find=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div['+ str(a) +']/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]').text
                except (NoSuchElementException,TimeoutException):
                    pass
                if ad_find=='Ad':
                    print("hi!")                  
                    i+=1
                
                try:
                    print(a)
                    print("clicking on the first search results on new page")
                    time.sleep(5)
                    driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div:nth-child(' + str(a) + ')').click()
                except:                                  
                    print("couldn't click on result")
                    continue
                try: #waiting for the title of the clicked place to appear
                    print("waiting for description block title of clicked search to appear")
                    WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME, "section-hero-header-title-description")))
                except (TimeoutException, NoSuchElementException):
                    print("description block chilled")
                    pass
                done=False
                loc_name, web_link, category, phone_no, address, rev_no, tot_rate, done=scrape_info(a,i,done)
                #scrape_info(a,i,done)   
                while (done!=True):
                    print("waiting...")
                try:
                    driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/button').click()
                    print("after clicking next a",a)
                    print("after clicking next i", i)
                
                except:
                    pass
                    
            continue
        #a calculated according to the division element that we have to click to scrape   
        a=(a*2)+1
        a=str(a)
        try: #waiting for the title element of places after entering our url 
            WebDriverWait(driver,25).until(EC.visibility_of_element_located((By.CLASS_NAME, "section-result-title")))
        except:
            pass
        
        try: #to ignore elements if they are ads
            ad_find=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div['+ a +']/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]').text
            if ad_find=='Ad':
                print("hi!")                  
         #the different search results are in odd numbered divs
                i+=1
        except (NoSuchElementException,TimeoutException):
            pass
        
        
        #clicking on the different places that appeared after searching
        try:                                     
            driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div:nth-child(' + a + ')').click()
        except:
            continue
        try: #waiting for the title of the clicked place to appear
            WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME, "section-hero-header-title-description")))
        except TimeoutException:
            pass
        #appending the lists based on the data we found after scraping
        try:
            loc_name.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div:nth-child(1) > h1 > span:nth-child(1)').text)
        except NoSuchElementException:
            loc_name.append(np.nan)
        
        try:
            category.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div.section-hero-header-title-description-container > div > div:nth-child(2) > span.section-rating-term > span:nth-child(1) > button').text)
        except NoSuchElementException:
            category.append(np.nan)
        
        try:
            address.append(driver.find_element_by_css_selector('button[data-tooltip="Copy address"]').text)
        except NoSuchElementException:
            address.append(np.nan)
        
        time.sleep(2)
        try:
            element=driver.find_element_by_css_selector('button[data-tooltip="Open website"]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            ActionChains(driver).move_to_element(element).perform()
            web_link.append(driver.find_element_by_css_selector('button[data-tooltip="Open website"]').text)
        except NoSuchElementException:
            web_link.append(np.nan)
            print("No web address found..")
                       
        time.sleep(2)
        try:
            phone_no.append(driver.find_element_by_css_selector('button[data-tooltip="Copy phone number"]').text)
        except NoSuchElementException:                           
            phone_no.append(np.nan)      

        try:
            rev_no.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.jqnFjrOWMVU__root > div > div.jqnFjrOWMVU__right > div.gm2-display-2').text)
        except NoSuchElementException:
            rev_no.append(np.nan)
    
        try:
            tot_rate.append(driver.find_element_by_css_selector('#pane > div > div.widget-pane-content.scrollable-y > div > div > div.jqnFjrOWMVU__root > div > div.jqnFjrOWMVU__right > button').text)
        except NoSuchElementException:  
            tot_rate.append(np.nan)
        
        #This appends the keyword that you want to search, so declare it in a start_search variable
        input_place.append(start_sear)
        a=int(a)
        print("final a",a)
        print("final i",i)
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/button').click()
        except (NoSuchElementException,TimeoutException):
            pass
        dict = {'keyword searched for':input_place, 'location_name': loc_name, 'website_link': web_link, 'category': category, 'contact': phone_no, 'address':address, 'no. of reviews': rev_no, 'total_ratings': tot_rate}  
        df_rev = pd.DataFrame(dict) 
        df_rev.to_csv('escape_rooms_final_result.csv') 

driver.close()


