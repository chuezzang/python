#상품 정보를 담는 클래스
class TourInfo:
    #맴버 변수 (실제 컬럼보다는 작게 세팅했음. 원래는 9가지가 필요)
    title = ''
    price = ''
    area  = ''
    link  = ''
    img   = ''
    #생성자
    def __init__(self, title, price, area, link, img):
        self.title = title
        self.price = price
        self.area  = area
        self.link  = link
        self.img   = img
