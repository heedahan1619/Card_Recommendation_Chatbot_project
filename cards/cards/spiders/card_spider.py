import scrapy
import requests
import re
from cards.items import CardsItem

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
        """카드사 딕셔너리 생성 함수"""

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
                    url=f"{self.json_url}cards/search?p={page}&perPage=30&corp={company_idx}" # 카드사별 카드 전체보기 url
                    ,headers=self.headers
                    ,callback=self.parse_card_data
                )


    def parse_card_data(self, response):
        """카드 json 데이터 로드 함수"""

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

                pr_container = data[i]['pr_container'] # 카드 이벤트 문구
                if pr_container == None:
                    pr_container = ''
                else:
                    pr_container = re.sub(r"\<(\/)?(p|li|ul)(\s\S+)?\>", "", pr_container)
                print(f"\n{pr_container}")
                
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

                search_benefit_dict = {} # 검색 혜택 딕셔너리 - {검색 혜택 타이틀:[검색 혜택 라벨]}
                for search_benefit in data[i]['search_benefit']: 
                    search_benefit_title = search_benefit['title'] # 검색 혜택 타이틀
                    search_benefit_label_list = [] # 검색 혜택 라벨 리스트
                    for search_benefit_options in search_benefit['options']:
                        search_benefit_label = search_benefit_options['label'] # 검색 혜택 라벨
                        search_benefit_label_list.append(search_benefit_label)
                    search_benefit_dict[search_benefit_title] = search_benefit_label_list
                
                top_benefit_list = [] # 상위 혜택 리스트 생성 - [상위 혜택 고로 이미지 url, 상위 혜택 태그, 상위 혜택 타이틀]
                for top_benefit in data[i]['top_benefit']:
                    top_benefit_title = top_benefit['title'] # 상위 혜택 타이틀
                    top_benefit_tags = f"{top_benefit['tags'][0]} {top_benefit['tags'][1]} {top_benefit['tags'][2]}" # 상위 혜택 태그
                    top_benefit_logo_img_url = top_benefit['logo_img']['url'] # 상위 헤택 로고 이미지 url
                    top_benefit_list.append([top_benefit_logo_img_url, top_benefit_tags, top_benefit_title])

                yield scrapy.Request(
                    url=f"{self.json_url}cards/{card_idx}"
                    ,headers=self.headers
                    ,callback=self.parse_add_card_data
                    ,meta={
                        "card_idx": card_idx
                        ,"card_type": card_type
                        ,"annual_fee_basic": annual_fee_basic
                        ,"card_img_url": card_img_url
                        ,"card_cate": card_cate
                        ,"corp_name": corp_name
                        ,"card_name": card_name
                        ,"only_online": only_online
                        ,"is_discon": is_discon
                        ,"search_benefit_dict": search_benefit_dict
                        ,"top_benefit_list": top_benefit_list
                    }
                )


    def parse_add_card_data(self, response):
        """추가적인 카드 json 데이터 로드 함수"""

        res = requests.get(response.url, headers=self.headers)
        data = res.json()

        annual_fee_detail = data['annual_fee_detail'] # 연회비 상세안내
        annual_fee_detail = re.sub(r'\<p(\s(\S)+)+\>|\<\S+\>', '', annual_fee_detail).replace('<br>', '\n').replace('&nbsp;', ' ').replace('&lsquo;', '‘').replace('&rsquo;;', '’').replace('&amp;', '&').strip()

        awards_list = [] # 수상 리스트 - [수상 내역]
        for awards in data['awards']:
            awards_title = awards['title'] # 수상 타이틀
            awards_contents = awards['contents'] # 수상 내역
            awards_contents = re.sub(r'\<\S+ class="title"\>', '\n', awards_contents)
            awards_contents = re.sub(r'\<(\/)?\S+(\s\S+)?\>|\<\S+((\s\S+)+)?\>', '', awards_contents).strip()
            if awards_contents != '':
                awards_list.append(awards_contents)

        brand_list = [] # 브랜드 리스트 - [브랜드코드, 브랜드 로고 이미지 url]
        for brand in data['brand']:
            brand_idx = brand['idx'] # 브랜드 인덱스
            brand_name = brand['name'] # 브랜드명
            brand_code = brand['code'] # 브랜드코드
            brand_logo_img_url = brand['logo_img']['url'] # 브랜드 로고 이미지 url
            brand_list.append([brand_code, brand_logo_img_url])

        key_benefit_list = [] # 주요혜택 리스트 - [주요혜택 로고 이미지 url, 주요혜택 타이틀, 주요혜택 내용, 주요혜택 상세안내]
        for key_benefit in data['key_benefit']:
            key_benefit_logo_img_url = key_benefit['cate']['logo_img']['url'] # 주요혜택 로고 이미지 url
            key_benefit_title = key_benefit['title'] # 주요혜택 타이틀
            key_benefit_comment = key_benefit['comment'] # 주요혜택 내용
            key_benefit_info = key_benefit['info'] # 주요혜택 상세안내
            key_benefit_info = re.sub(r'\<\/p\>', '\n', key_benefit_info)
            key_benefit_info = re.sub(r'\<(\/)?(p|strong|br)((\s\S+)+)?\>', '', key_benefit_info).replace('&nbsp;', ' ').replace('&amp;', '&').replace('&ndash;', '–').replace('&sup1;', '¹').replace('&sup2;', '²').replace('&sup3;', '³').replace('&trade;', '™').replace('&times;', '×').replace('&lt;', '<').replace('&gt;', '>').replace('&middot;', '·').replace('&bull;', '•').replace("&#39;", "'").replace('&quot;', '"').replace('&lsquo;', '‘').replace('&rsquo;', '’').replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&rarr;', '→')
            key_benefit_list.append([key_benefit_logo_img_url, key_benefit_title, key_benefit_comment, key_benefit_info])
        
        yield scrapy.Request(
            url=f"{self.json_url}cards/compare_top3/{response.meta['card_idx']}" # 많이 비교되는 카드 json 데이터 url
            ,headers=self.headers
            ,callback=self.parse_compare_card_data
            ,meta={
                "card_idx": response.meta['card_idx']
                ,"card_type": response.meta['card_type']
                ,"annual_fee_basic": response.meta['annual_fee_basic']
                ,"card_img_url": response.meta['card_img_url']
                ,"card_cate": response.meta['card_cate']
                ,"corp_name": response.meta['corp_name']
                ,"card_name": response.meta['card_name']
                ,"only_online": response.meta['only_online']
                ,"is_discon": response.meta['is_discon']
                ,"search_benefit_dict": response.meta['search_benefit_dict']
                ,"top_benefit_list": response.meta['top_benefit_list']
                ,"annual_fee_detail": annual_fee_detail
                ,"awards_list": awards_list
                ,"brand_list": brand_list
                ,"key_benefit_list": key_benefit_list
            }
        )


    def parse_compare_card_data(self, response):
        """많이 비교되는 카드 json 데이터 추출 함수"""

        res = requests.get(response.url, headers=self.headers)
        data = res.json()

        compare_card_list = [] # 많이 비교된 카드 리스트 - [많이 비교된 카드 img url, 많이 비교된 카드명, 많이 비교된 카드사명, 많이 비교된 카드 연회비 기본, 많이 비교된 카드 전월실적]
        for compare_card in data:
            compare_card_img = compare_card['card_img']['url'] # 많이 비교된 카드 img url
            compare_card_name = compare_card['name'] # 많이 비교된 카드명
            compare_card_corp_name = compare_card['corp']['name'] # 많이 비교된 카드사명
            compare_card_annual_fee_basic = compare_card['annual_fee_basic'] # 많이 비교된 카드 연회비 기본
            compare_card_pre_month_money = str(compare_card['pre_month_money']) # 많이 비교된 카드 전월실적
            if len(compare_card_pre_month_money) == 6:
                compare_card_pre_month_money = f"전월실적 {compare_card_pre_month_money[:2]}만원 이상"
            elif len(compare_card_pre_month_money) == 7:
                compare_card_pre_month_money = f"전월실적 {compare_card_pre_month_money[:3]}만원 이상"
            else:
                compare_card_pre_month_money = "전월실적 없음"
            compare_card_list.append([compare_card_img, compare_card_name, compare_card_corp_name, compare_card_annual_fee_basic, compare_card_pre_month_money])

        yield scrapy.Request(
            url="http://www.card-gorilla.com/home"
            ,headers=self.headers
            ,callback=self.parse_card_items
            ,meta={
                "card_idx": response.meta['card_idx']
                ,"card_type": response.meta['card_type']
                ,"annual_fee_basic": response.meta['annual_fee_basic']
                ,"card_img_url": response.meta['card_img_url']
                ,"card_cate": response.meta['card_cate']
                ,"corp_name": response.meta['corp_name']
                ,"card_name": response.meta['card_name']
                ,"only_online": response.meta['only_online']
                ,"is_discon": response.meta['is_discon']
                ,"search_benefit_dict": response.meta['search_benefit_dict']
                ,"top_benefit_list": response.meta['top_benefit_list']
                ,"annual_fee_detail": response.meta['annual_fee_detail']
                ,"awards_list": response.meta['awards_list']
                ,"brand_list": response.meta['brand_list']
                ,"key_benefit_list": response.meta['key_benefit_list']
                ,"compare_card_list": compare_card_list
            }
        )


    def parse_card_items(self, response):
        """카드 item 추출 함수"""

        # print(f"\n{response.meta}")