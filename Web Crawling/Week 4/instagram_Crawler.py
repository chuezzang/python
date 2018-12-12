from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

# 기본 정보 입력
username = input("Input ID : ")  # User ID
password = getpass.getpass("Input PW : ")  # User PWD
hashTag = input("Input HashTag # : ")  # Search #
checkTag = hashTag.find('#')
target_url = 'https://www.instagram.com/'

# 해시태그 사용유무 체크
if checkTag == -1:
    hashTag = '#' + hashTag

# 크롬 브라우저 드라이버 로드
driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get(target_url)

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
element_id.send_keys('username')
element_pw = driver.find_element_by_xpath("//input[@name='password']")
element_pw.send_keys('password')

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

# # 페이지를 스크롤하여 이미지를 최대한 모으기
# SCROLL_PAUSE_TIME = 3
# for scroll in range(1, 10):
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)
#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         # try again (can be removed)
#         driver.execute_script(
#             "window.scrollTo(0, document.body.scrollHeight);")
#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)
#         # Calculate new scroll height and compare with last scroll height
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         # check if the page height has remained the same
#         if new_height == last_height:
#             # if so, you are done
#             break
#         # if not, move on to the next loop
#         else:
#             last_height = new_height
#             continue

# 검색하여 현재 노출된 페이지 안의 사진수 만큼의 빈 배열을 만들어둠
# resultCnt = len(driver.find_elements_by_css_selector('.eLAPa .KL4Bh'))
# resultValues = []

# 사진수 만큼의 index를 가진 빈배열 만들기 끝
# for i in range(resultCnt):
#     resultValues.append('')

# print(resultCnt)
# print(resultValues)


# 이미지 찾아 저장하기
# for item in range(1, 3):
try:
    resultValues = []
    elem = driver.find_element_by_css_selector('body')
    page_images = driver.find_elements_by_css_selector('.eLAPa .KL4Bh')
    current_iamges = len(page_images)

    #자동으로 스크롤 하기
    total_images = 100
    for i in total_images:
        elem.send_keys(u'\ue00f')
        time.sleep(2)
    
        for img in total_images:
            obj = img.find_element_by_css_selector('img').get_attribute('src')
            resultValues.append(obj)
        current_iamges = len(resultValues)
        total_images -= current_iamges
    print(len(resultValues))

except Exception as err:
    print('이미지 로드 오류', err)

# print(tag_img_list, len(tag_img_list))

