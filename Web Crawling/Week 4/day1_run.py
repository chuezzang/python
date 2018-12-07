# 인터파크 투어 사이트에서 여행지를 입력후 검색 -> 잠시 후 -> 결과
# 로그인 시 PC 웹 사이트에서 처리가 어려울 경우 -> 모바일 로그인 진입
# 모듈 가져오기
# pip install selenium
# 사람이 하는 행위와 최대한 유사하게 접근하는 방식

from selenium import webdriver as wd

from selenium.webdriver.common.by import By                         
# 명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# 사전에 필요한 정보를 로드 => DB or Shell, Batch file에서 인자로 받아서 세팅
main_url = 'https://tour.interpark.com/'
keyword  = '로마'

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
for page in range(1, 16):
    try:
        # 자바스크립트 구동하기
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        print("%s 페이지 이동" % page)
    
    except Exception as e1:
        print('오류', e1)

# 브라우저 닫기, 끝내기
# 파이썬 끝내기

#