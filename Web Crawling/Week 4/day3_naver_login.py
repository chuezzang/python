from selenium import webdriver
import time

url = "https://nid.naver.com/nidlogin.login"

browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get(url)

id = browser.find_element_by_css_selector("#id").send_keys("naver_id")
pw = browser.find_element_by_xpath('//*[@id="pw"]').send_keys("navee_pw")

time.sleep(2)
browser.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()

time.sleep(10)
browser.quit()