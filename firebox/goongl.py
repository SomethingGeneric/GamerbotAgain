from selenium import webdriver
from selenium.webdriver.common.by import By

import sys

driver = webdriver.Firefox()


def try_find_weather(query):
    driver.get("https://google.com")

    box = driver.find_element(By.CLASS_NAME, "gLFyf")
    box.send_keys("weather in " + query + "\n")

    try:
        temp = driver.find_element(By.XPATH, '//*[@id="wob_tm"]')
        return str(temp.text)
    except:
        return "FAIL"


cmd = sys.argv[1]
where = sys.argv[2]

if cmd == "weather":
    res = try_find_weather(where)
    print(res)
else:
    print("Empty")
