from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
from bs4 import BeautifulSoup
import json
import os

# 기본 정보 입력
target_url = 'https://www.instagram.com/'
image_num = 100
username = input("Input ID : ")  # User ID
password = getpass.getpass("Input PW : ")  # User PWD
hashTag = input("Input HashTag # : ")  # Search #

# 해시태그 사용유무 체크
# checkTag = hashTag.find('#')
# if checkTag == -1:
#     hashTag = '#' + hashTag

# 크롬 브라우저 드라이버 로드
driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get(target_url)
time.sleep(3)

# 로그인 링크 찾아 클릭하기
login_elem = driver.find_element_by_link_text('Log in')
login_elem.click()

# # Explicitly wait
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'button.aOOlW.HoLwm'))
#     )
# except Exception as e1:
#     print('대기 오류 발생', e1)
time.sleep(3)

# 로그인 정보 입력하기
element_id = driver.find_element_by_xpath("//input[@name='username']")
element_id.send_keys(username)
element_pw = driver.find_element_by_xpath("//input[@name='password']")
element_pw.send_keys(password)

password = 0 # RESET password

# 로그인 버튼 클릭하기
driver.find_element_by_xpath("//button[contains(.,'Log in')]").click()
driver.implicitly_wait(5)
# 팝업창 "Not Now" 버튼 클릭
driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
driver.implicitly_wait(5)

# 검색 입력창 찾기
searchbox = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='Search']")
    )
)

# 검색할 해시태그 입력 및 검색하기
driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(hashTag)
driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').click()
driver.implicitly_wait(5)

# 해시태그 검색 결과 표시
searchTotalCount = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/header/div[2]/div[2]/span/span').text
print('검색결과  Total : ' + searchTotalCount + ' 건 의 게시물이 검색되었습니다.')

# 이미지 찾아 저장하기
try:
    resultValues = []
    elem = driver.find_element_by_css_selector('body')
    page_images = driver.find_elements_by_css_selector('.eLAPa .KL4Bh')
    current_images = len(page_images)

    while current_images <= image_num:
        
        for image in page_images:
            obj = image.find_element_by_css_selector('img').get_attribute('src')
            resultValues.append(obj)

        elem.send_keys(u'\ue00f')
        time.sleep(5)

        current_images = len(resultValues)

    FINAL = resultValues[:image_num]
    print(FINAL)
    print(len(FINAL))

except Exception as err:
    print('이미지 로드 오류', err)

# 파일로 저장하기


soup = driver.get('https://www.instagram.com/explore/tags/' + hashTag)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')  # BeautifulSoup사용하기
images = soup.select('div > a > div.eLAPa > div.KL4Bh > img')

data = {}
i = 0
for img in images:
    # print(n.get('src'))
    data[i] = img.get('src')
    i += 1

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)

# 브라우저 닫기, 끝내기
driver.close()  # 닫기
driver.quit()  # 끝내기

import sys
sys.exit()  # 프로세스 끝내기
