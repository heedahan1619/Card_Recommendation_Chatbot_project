# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CardsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    card_img_url = scrapy.Field() # 카드 이미지 url
    card_name = scrapy.Field() # 카드명
    corp_name = scrapy.Field() # 카드사명
    card_pr = scrapy.Field() # 카드 pr 문구
    top_benefit_list = scrapy.Field() # 상위 혜택 리스트
    is_discon = scrapy.Field() # 신규 발급 중단
    annual_fee_basic = scrapy.Field() # 연회비 기본
    pre_month_money = scrapy.Field() # 전월실적
    brand_list = scrapy.Field() # 카드 브랜드 리스트
    only_online = scrapy.Field() # 온라인 발급 전용
    key_benefit_list = scrapy.Field() # 주요 혜택 리스트
    awards_list = scrapy.Field() # 고릴라 어워즈
    compare_card_list = scrapy.Field() # 많이 비교된 카드 - 최근 1개월
    ranking_dict = scrapy.Field() # 카드사별 인기순위