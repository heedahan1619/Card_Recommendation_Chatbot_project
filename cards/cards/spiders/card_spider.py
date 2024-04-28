import scrapy
import requests
import re

class CardGorillaSpider(scrapy.Spider):
    """카드고릴라 사이트 spider"""
    name = "card" # spider name
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    page_request = 10

    home_url = "https://www.card-gorilla.com/home"
    json_url = "https://api.card-gorilla.com:8080/v1/"

    company_dict = {} # 카드사 딕셔너리 - {카드사명:[카드사 인덱스, 카드사 로고 이미지 url]}
    brand_dict = {} # 카드 브랜드 딕셔너리 - {카드 브랜드 코드:[카드 브랜드명, 카드 브랜드 인덱스, 카드 브랜드 로고 이미지 url]}

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
            
            for page in range(1, self.page_request+1):
                yield scrapy.Request(
                    url=f"{self.json_url}cards/search?p={page}&perPage=30&corp={company_idx}"
                    ,headers=self.headers
                    ,callback=self.parse_card_data
                )

    def parse_card_data(self, response):
        """카드 json 데이터 로드"""

        res = requests.get(response.url, headers=self.headers)
        data = res.json()['data']

        if data != []:
            for i in range(len(data)):

                annual_fee_basic = data[i]['annual_fee_basic'] # 연회비 기본
                annual_fee_basic = annual_fee_basic.replace('[', '').replace(']', '')
                
                card_type = data[i]['c_type_txt'] # 카드 타입
                
                card_img_url = data[i]['card_img']['url'] # 카드 이미지 url
                
                card_cate = f"{data[i]['cate_txt']}카드" # 카드 종류
                
                card_idx = data[i]['cid'] # 카드 인덱스
                
                corp_idx = data[i]['corp_idx'] # 카드사 인덱스
                
                corp_name = data[i]['corp_txt'] # 카드사명
                
                card_name = data[i]['name'] # 카드명
                
                only_online = data[i]['only_online'] # 온라인발급 전용 카드
                if only_online == True:
                    only_online = "온라인발급 전용 카드"
                else:
                    only_online = ""
                
                pre_month_money = str(data[i]['pre_month_money']) # 전월실적
                if len(pre_month_money) == 6:
                    pre_month_money = f"전월실적 {pre_month_money[:2]}만원 이상"
                elif len(pre_month_money) == 7:
                    pre_month_money = f"전월실적 {pre_month_money[:3]}만원 이상"
                else:
                    pre_month_money = "전월실적 없음"
                
                is_discon = data[i]['is_discon'] # 발급 중단 카드 
                if is_discon == True:
                    is_discon = "신규발급이 중단된 카드입니다."
                else:
                    is_discon = ""

                global search_benefit_dict
                search_benefit_dict = {} # 검색 혜택 딕셔너리 - {검색 혜택 타이틀:[검색 혜택 라벨]}
                search_benefit_title_list = [] # 검색 혜택 타이틀 리스트
                for search_benefit in data[i]['search_benefit']: 
                    search_benefit_title = search_benefit['title'] # 검색 혜택 타이틀
                    search_benefit_title_list.append(search_benefit_title)
                    search_benefit_label_list = [] # 검색 혜택 라벨 리스트
                    for search_benefit_options in search_benefit['options']:
                        search_benefit_label = search_benefit_options['label'] # 검색 혜택 라벨
                        search_benefit_label_list.append(search_benefit_label)
                    search_benefit_dict[search_benefit_title] = search_benefit_label_list
                
                global top_benefit_dict
                top_benefit_dict = {} # 상위 혜택 딕셔너리 - {상위 혜택 태그:[상위 혜택 로고 이미지 url, 상위 혜택 타이틀]}
                top_benefit_title_list = [] # 상위 혜택 타이틀 리스트
                top_benefit_tags_list = [] # 상위 혜택 태그 리스트
                for top_benefit in data[i]['top_benefit']:
                    top_benefit_title = top_benefit['title'] # 상위 혜택 타이틀
                    top_benefit_title_list.append(top_benefit_title)
                    top_benefit_tags = f"{top_benefit['tags'][0]} {top_benefit['tags'][1]} {top_benefit['tags'][2]}" # 상위 혜택 태그
                    top_benefit_tags_list.append(top_benefit_tags)
                    top_benefit_logo_img_url = top_benefit['logo_img']['url']
                    top_benefit_dict[top_benefit_tags] = [top_benefit_logo_img_url, top_benefit_title]

                yield scrapy.Request(
                    url=f"{self.json_url}cards/{card_idx}"
                    ,headers=self.headers
                    ,callback=self.parse_add_card_data
                )

    def parse_add_card_data(self, response):
        """추가적인 카드 json 데이터 로드"""

        print(f"\n{response.url}")

        res = requests.get(response.url, headers=self.headers)
        data = res.json()

        annual_fee_detail = data['annual_fee_detail'] # 연회비 상세안내
        annual_fee_detail = re.sub(r'\<p(\s(\S)+)+\>|\<\S+\>', '', annual_fee_detail).replace('<br>', '\n').replace('&nbsp;', ' ').replace('&lsquo;', '‘').replace('&rsquo;;', '’').replace('&amp;', '&').strip()

        awards_list = [] # 수상 내역 리스트
        for awards in data['awards']:
            awards_title = awards['title'] # 수상 타이틀
            awards_contents = awards['contents'] # 수상 내역
            awards_contents = re.sub(r'\<\S+ class="title"\>', '\n', awards_contents)
            awards_contents = re.sub(r'\<(\/)?\S+(\s\S+)?\>|\<\S+((\s\S+)+)?\>', '', awards_contents).strip()
            if awards_contents != '':
                awards_list.append(awards_contents)

        if awards_list != []:
            for award in awards_list:
                print(award)
        