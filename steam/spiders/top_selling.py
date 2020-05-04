import scrapy
from ..items import SteamItem
from scrapy.loader import ItemLoader
 
 
class TopSellingSpider(scrapy.Spider):	
    name = 'top_selling'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']

    def parse(self, response):
        #steam_item = SteamItem()
        games = response.xpath('//div[@id="search_resultsRows"]/a')
        for game in games:
            loader = ItemLoader(item=SteamItem(),selector=game,response=response)
            loader.add_xpath("game_url",'.//@href')
            loader.add_xpath('img_url','.//div[@class="col search_capsule"]/img/@src')
            loader.add_xpath('name','.//span[@class="title"]/text()')
            loader.add_xpath('release_date','.//div[@class="col search_released responsive_secondrow"]/text()')
            loader.add_xpath('platforms','.//span[contains(@class, "platform_img") or @class="vr_supported"]/@class')
            loader.add_xpath('review','.//span[contains(@class,"search_review_summary")]/@data-tooltip-html')
            loader.add_xpath('discount_rate','.//div[contains(@class,"col search_discount")]/span/text()')
            loader.add_xpath('original_price','.//div[contains(@class,"search_price_discount_combined")]')
            loader.add_xpath('discounted_price','.//div[contains(@class," search_price discounted")]/text()')
            
            #steam_item['game_url']      = game.xpath('').get()
            #steam_item['img_url']       = game.xpath('.//div[@class="col search_capsule"]/img/@src').get()
            #steam_item['name']          = game.xpath('.//span[@class="title"]/text()').get()
            #steam_item['release_date']  = game.xpath('.//div[@class="col search_released responsive_secondrow"]/text()').get()
            #steam_item['platforms']     = self.get_platforms(game.xpath('.//span[contains(@class, "platform_img") or @class="vr_supported"]/@class').getall())
            #steam_item['review']        = remove_tags(game.xpath('.//span[contains(@class,"search_review_summary")]/@data-tooltip-html').get())   
            #steam_item['discount_rate'] = self.clean_discount(game.xpath('.//div[contains(@class,"col search_discount")]/span/text()').get())
            #steam_item['original_price']= self.get_original(game.xpath('.//div[contains(@class,"search_price_discount_combined")]'))
            #steam_item['discounted_price'] = game.xpath('normalize-space((.//div[contains(@class," search_price discounted")]/text())[2])').get()
            
            yield loader.load_item()
            #yield steam_item
        next_page = response.xpath('//a[@class="pagebtn" and text()=">"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )