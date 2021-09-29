#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import time
import json
import re
import os
import time 
import csv

numbers = []
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 600)
action = ActionChains(driver)

def hasxpath(non_business_xpath):
    try: 
        driver.find_element_by_xpath(non_business_xpath)
        return True
    except:
        return False

def scrape():

    i = 0

    # right_side_component 
    groups_people = driver.find_elements_by_xpath("//div[@class='_3m_Xw']")
    groups_people.sort(key=lambda x: int(x.get_attribute('style').split("translateY(")[1].split('px')[0]), reverse=False)

    for p in groups_people:

        p.click()  # open a chat

        header = p.find_element_by_xpath('//*[@id="main"]/header')
        header.click()  # click on the header inside chat
        
        time.sleep(1.5)

        if hasxpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[4]/div[3]/div/div/span/span') == True:
            phone = str(p.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[4]/div[3]/div/div/span/span').text.split("\n"))
        else:
            phone = str(p.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[3]/div[1]/div[2]/span').text.split("\n"))
        
        numbers.append(phone.replace(" ", "")
                            .replace("-", "")
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", ""))
        i += 1
        print(str(i) + "/" + str(len(groups_people)))

    # for p in groups_people:
        
    #     try:
    #         p.click()  # open a chat

    #         header = p.find_element_by_xpath('//*[@id="main"]/header')
    #         header.click()  # click on the header inside chat
            
    #         # time.sleep(1.5)

    #         if hasxpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[4]/div[3]/div/div/span/span') == True:
    #             phone = str(p.find_element_by_xpath(
    #             '/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[4]/div[3]/div/div/span/span').text.split("\n"))
    #         else:
    #             phone = str(p.find_element_by_xpath(
    #             '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[3]/div[1]/div[2]/span').text.split("\n"))
            
    #         numbers.append(phone.replace(" ", "")
    #                             .replace("-", "")
    #                             .replace("[", "")
    #                             .replace("]", "")
    #                             .replace("'", ""))
    #         i += 1
    #         print(str(i) + "/" + str(len(groups_people)))
    #     except exceptions.StaleElementReferenceException:
    #         pass

        

    with open("dirty_contacts.json", "w") as file:
        json.dump(numbers, file)


if __name__ == '__main__':
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)
    x_arg = '//*[@id="pane-side"]/div[1]/div/div/div[1]'
    chats = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    scrape()
print("done")
driver.quit()