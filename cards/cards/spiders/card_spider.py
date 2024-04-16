import scrapy
import requests

class CardGorillaSpider(scrapy.Spider):
    """카드고릴라 사이트 spider"""
    name = "card" # spider name
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    home_url = "https://www.card-gorilla.com/home"
    json_url = "https://api.card-gorilla.com:8080/v1/"

    company_dict = {} # 카드사 딕셔너리 - {카드사명:[카드사 인덱스, 카드사 로고 이미지 url]}

    def start_requests(self):
        """크롤러가 시작하면서 실행하는 메소드"""

        print("카드고릴라 접속 완료")

        return [
            scrapy.Request(
                url=self.home_url
                ,headers=self.headers
                ,callback=self.parse_company
            )
        ]
    
    def parse_company(self, response):
        """카드사 json 파일 불러오기"""

        print("카드사 json 파일 로드 완료")

        card_corps = f"{self.json_url}card_corps"

        res = requests.get(card_corps, headers=self.headers)
        data = res.json()

        for i in range(len(data)):
            corps = data[i]
            company_idx = corps['idx'] # 카드사 인덱스
            company_name = corps['name'] # 카드사명
            company_logo_img_url = corps['logo_img']['url'] # 카드사 로고 이미지 url
            
            self.company_dict[company_name] = [company_idx, company_logo_img_url]
            
        print(self.company_dict)

