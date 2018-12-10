# 인터파크 투어 사이트에서 여행지를 입력후 검색 -> 잠시 후 -> 결과
# 로그인 시 PC 웹 사이트에서 처리가 어려울 경우 -> 모바일 로그인 진입
# 모듈 가져오기
# pip install selenium
# 사람이 하는 행위와 최대한 유사하게 접근하는 방식

# pip install BeautifulSoup

from selenium import webdriver as wd

from selenium.webdriver.common.by import By               
from bs4 import BeautifulSoup as bs

# 명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from Tour import TourInfo


# 사전에 필요한 정보를 로드 => DB or Shell, Batch file에서 인자로 받아서 세팅
main_url = 'https://tour.interpark.com/'
keyword  = '로마'
# 상품정보를 담는 리스트 (TourInfo 리스트)
tour_list = []

# 드라이버 로드
driver = wd.Chrome(executable_path = './chromedriver')

# 이후 개선 사항 -> 옵션을 부여하여 (프록시, 에이전트 조작, 이미지를 배제)
# 크롤링을 오래 돌리면 -> 임시 파일들이 쌓인다!! -> Temp 파일 삭제 (관리적인 측면)
# 
# 사이트 접속 (get 방식) / 대기도 필요함
driver.get(main_url)
# 검색창을 찾아서 검색어를 입력
# id : SearchGNBText
driver.find_element_by_id('SearchGNBText').send_keys(keyword)
# 수정할 경우 -> 뒤에 내용이 붙어버림 -> 선조치로 .clear() -> .send_keys('내용')
# id, class, 관계 등의 고유한 값을 찾아야 함.

# 검색 버턴을 클릭
driver.find_element_by_css_selector('button.search-btn').click()

# 잠시 대기 => 페이지가 로드됙고 나서 즉각적으로 데이터를 획득하는 행위는 자제 (로딩되는 속도가 천차만별)
# Explicit Waits : 화면과 화면 사이에는 무조건 들어가야 할 대기 코드 (무시 안됨!!)
# 명시적 대기 -> 특정 요소가 로케이트(발견될 때까지) 대기
try:
    element = WebDriverWait(driver, 10).until(
        # 지정한 한개 요소가 올라오면 대기 종료 (더보기 버턴)
        EC.presence_of_element_located((By.CLASS_NAME, 'oTravelBox'))
    )
except Exception as e:
    print('오류 발생', e)

# 대기 방법 : 특정요소가 발견될 때까지 or 특정 시간까지 or 코드적으로 제한 / DDOS 사이트 진입시에는 평균 10초 정도 대기함
# 암묵적 대기 -> DOM이 다 로드될 때까지 대기하고 먼저 로드되면 바로 진행
# 요소를 첮을 특정 시간 동안 (10초) DOM 풀링을 지시 (예를 들어, 10초 이내라도 발견되면 진행)
driver.implicitly_wait(2)
# 절대적 대기 -> time.sleep('second') -> 클라우드 페어(디도스 방어 솔루션)

# 더보기 눌러서 -> 게시판으로 진입
driver.find_element_by_css_selector('.oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click()  # >는 CSS 상에서의 자식 관계 .은 CSS 상에서 element를 정의함

# 게시판에서 데이터를 가져올 때 
# 데이터가 많으면 세션(혹시 로그인을 해서 접근되는 사이트일 경우) 관리
# 특정 단위별로 로그아웃, 로그인 계속 시도
# 특정 게시물이 사라질 경우 -> 팝업 발생 (없는 ....) -> 팝업 처리 검토
# 위 사항들은 운영을 해봐야만 알 수 있는 사항들

# 게시판을 스캔시 -> 임계점을 모름!!!
# 게시판을 스캔 -> 메타 정보 획득 -> loop를 돌려서 일괄적으로 방문 접근

# searchModule.SetCategoryList(1, '') 스크립트 실행
# 16은 임시값, 게시물을 넘어갔을 때 현상을 확인하기 위함. 
for page in range(1, 2): #16):
    try:
        # 자바스크립트 구동하기
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        print("%s 페이지 이동" % page)
        ############################
        # 여러 사이트에서 정보를 수집할 경우 공통 정보를 정의 단계 필요
        # 상품명, 코멘트, 기간1, 기간2, 가격, 평점, 썸네일, 링크(실제 상품 상세정보)
        boxItems = driver.find_elements_by_css_selector('.oTravelBox > .boxList > li')  # ('.oTravelBox > .boxList > .boxItem')
        # 상품 하나하나 접근
        for li in boxItems:
            # 이미지를 링크값을 사용할 것인가?(없어질 수도 있음) 
            # 직접 다운로드해서 우리 서버에 업로드(ftp) 할 것인가? (파일을 받는 방법) 측면도 고민 필요
            print('썸네일', li.find_element_by_css_selector('img').get_attribute('src')) #속성값을 가져올 경우
            print('링크', li.find_element_by_css_selector('a').get_attribute('onclick')) #스캐닝을 하므로 클릭을 해서는 안되므로
            print('상품명', li.find_element_by_css_selector('h5.proTit').text)
            print('코멘트', li.find_element_by_css_selector('.proSub').text)
            print('가격', li.find_element_by_css_selector('.proPrice').text)
            area = ''

            for info in li.find_elements_by_css_selector('.info-row .proInfo'): #4개의 속성값을 가져 옴
                print(info.text)
            print('='*100)
            # 데이터 모음
            # li.find_elements_by_css_selector('.info-row .proInfo')[1].text
            # 데이터가 부족하거나 없을수도 있으므로 직접 인덱스로 표현은 위험성이 있음. 예외처리 필요
            # 최초 뽑을 때부터 4개 속성값을 별도로 신경을 써서 별도로 저장해 두는 게 좋음
            obj = TourInfo(
                li.find_element_by_css_selector('h5.proTit').text,
                li.find_element_by_css_selector('.proPrice').text,
                li.find_elements_by_css_selector('.info-row .proInfo')[1].text, # 리스크가 있는 코드, 정보가 없을 경우 오류 발생 여지 있음
                li.find_element_by_css_selector('a').get_attribute('onclick'),
                li.find_element_by_css_selector('img').get_attribute('src')
            )
            tour_list.append(obj)

    except Exception as e1:
        print('오류', e1)

print (tour_list, len(tour_list)) # 갯수 확인

# 수집한 정보 개수를 루프 -> 페이지 방문 -> 콘텐츠 획득 (상품상세정보) : BeautfulSoup을 사용 -> DB에 입력
for tour in tour_list:
    # tour ->> TourInfo
    print (type(tour)) #내장함수 Type을 통해 확인 가능
    # 스크립트를 바로 실행하면, 새창이 열려 리소스 부족 현상이 발생할 수 있으므로,
    # 동일 탭에서 실행될 수 있도록 설정해야 함.
    # 링크 데이터에서 실 데이터 획득
    # 분해
    arr = tour.link .split(',') # 링크를 2 덩어어리로 분해
    
    if arr:
        # 대체
        link = arr[0].replace('searchModule.OnClickDetail(','') # 이렇게 사용해도 되는 이유는 규칙적으로 반복하기 때문에 가능
        # 슬라이싱 -> 앞에 ', 뒤에 ' 제거
        detail_url = link[1:-1] # 앞뒤로 하나씩 잘라내는 방식임. 
        # 상세 페이지 이동 : URL 값이 완성된 형태인지 확인 (http~~~)
        driver.get(detail_url)
        time.sleep(2)

        # 현재 페이지를 BeautifulSoup의 DOM으로 구성
        soup = bs(driver.page_source, 'html.parser') # 현재페이지의 URL
        # 현재 상세정보 페이지에서 스케쥴 정보를 획득
        data = soup.select('.schedule-all')  # BS4의 CSS Selector
        print(type(data), len(data))

# 브라우저 닫기, 끝내기
driver.close() # 닫기
driver.quit()  # 끝내기

import sys
sys.exit()     # 프로세스 끝내기


