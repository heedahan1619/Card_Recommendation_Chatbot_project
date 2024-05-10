# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CardsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    card_idx = scrapy.Field() # 카드 인덱스
    card_type = scrapy.Field() # 카드 타입
    annual_fee_basic = scrapy.Field() # 연회비 일반
    card_img_url = scrapy.Field() # 카드 이미지 url
    card_cate = scrapy.Field() # 카드 종류
    corp_idx = scrapy.Field() # 카드사 인덱스
    corp_name = scrapy.Field() # 카드사명
    card_name = scrapy.Field() # 카드명
    only_online = scrapy.Field() # 온라인 발급 전용
    pr_container = scrapy.Field() # 카드 pr 문구
    pre_month_money = scrapy.Field() # 전월실적
    is_discon = scrapy.Field() # 신규 발급 중단
    search_benefit_dict = scrapy.Field() # 검색 혜택 딕셔너리
    top_benefit_list = scrapy.Field() # 상위 혜택 리스트
    annual_fee_detail = scrapy.Field() # 연회비 상세
    awards_list = scrapy.Field() # 고릴라 수상 리스트
    brand_list = scrapy.Field() # 카드 브랜드 리스트
    key_benefit_list = scrapy.Field() # 주요 혜택 리스트
    compare_card_list = scrapy.Field() # 많이 비교된 카드 - 최근 1개월
    ranking_dict = scrapy.Field() # 카드사별 인기순위