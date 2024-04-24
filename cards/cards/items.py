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
    top_benefit_tags_list = scrapy.Field() # 상위 혜택 태그 리스트
    annual_fee_basic = scrapy.Field() # 연회비 기본
    pre_month_money = scrapy.Field() # 전월실적
    only_online = scrapy.Field() # 온라인 발급 전용