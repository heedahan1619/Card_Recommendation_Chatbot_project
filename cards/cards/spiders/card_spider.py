import scrapy
import requests

class CardGorillaSpider(scrapy.Spider):
    """카드고릴라 사이트 spider"""
    name = "card" # spider name
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    page_request = 10

    home_url = "https://www.card-gorilla.com/home"
    json_url = "https://api.card-gorilla.com:8080/v1/"
    card_url = "https://api.card-gorilla.com:8080/v1/cards/search?"

    company_dict = {} # 카드사 딕셔너리 - {카드사명:[카드사 인덱스, 카드사 로고 이미지 url]}

    def start_requests(self):
        """크롤러가 시작하면서 실행하는 메소드"""

        return [
            scrapy.Request(
                url=self.home_url
                ,headers=self.headers
                ,callback=self.parse_company_data
            )
        ]
    
    def parse_company_data(self, response):
        """카드사 딕셔너리 생성"""

        url = f"{self.json_url}card_corps"

        res = requests.get(url, headers=self.headers)
        data = res.json()

        global company_idx_list
        company_idx_list = [] # 카드사 인덱스 리스트 생성
        for i in range(len(data)):
            corps = data[i]
            company_idx = corps['idx'] # 카드사 인덱스
            company_idx_list.append(company_idx)
            company_name = corps['name'] # 카드사명
            company_name_eng = corps['name_eng'] # 영문 카드사명
            if " " in company_name_eng:
                company_name_eng = company_name_eng.split(" ")[0]
            if "Card" in company_name_eng:
                company_name_eng = company_name_eng.replace("Card", "")
            company_name_eng = company_name_eng.lower()
            company_logo_img_url = corps['logo_img']['url'] # 카드사 로고 이미지 url
            
            self.company_dict[company_idx] = [company_name, company_name_eng, company_logo_img_url]

        return [
            scrapy.Request(
                url=f"{self.card_url}p=1&perPage=30&corp={company_idx}"
                ,headers=self.headers
                ,callback=self.parse_card_data
            )
            for company_idx in company_idx_list
        ]

    def parse_card_data(self, response):
        """카드 json 데이터 로드"""

        res = requests.get(response.url, headers=self.headers)
        data = res.json()['data']
        
        print(data)