import scrapy

class CardGorillaSpider(scrapy.Spider):
    """카드고릴라 사이트 spider"""
    name = "card" # spider name
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    home_url = "https://www.card-gorilla.com/home"

    def start_requests(self):
        """크롤러가 시작하면서 실행하는 메소드"""

        print("카드고릴라 접속 완료")

        return [
            scrapy.Request(
                url=self.home_url
                ,headers=self.headers
            )
        ]
    