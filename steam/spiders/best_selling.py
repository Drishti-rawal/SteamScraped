import scrapy
from ..items import SteamItem
 
 
class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']
 
    def get_platforms(self, list_classes):
        platforms = []
        for item in list_classes:
            platform = item.split()[-1]
            if platform == 'win':
                platforms.append('windows')
            if platform == 'mac':
                platforms.append('Mac OS')
            if platform == 'linux':
                platforms.append('Linux')
            if platform == 'vr_supported':
                platforms.append('VR Supported')
        return platforms
 
    def parse(self, response):
        steam_item = SteamItem()
        games = response.xpath('//div[@id="search_resultsRows"]/a')
        for game in games:
            steam_item['game_url'] = game.xpath('.//@href').get()
            steam_item['img_url'] = game.xpath('.//div[@class="col search_capsule"]/img/@src').get()
            steam_item['name'] = game.xpath('.//span[@class="title"]/text()').get()
            steam_item['release_date'] = game.xpath('.//div[@class="col search_released responsive_secondrow"]/text()').get()
            steam_item['platforms'] = self.get_platforms(game.xpath('.//span[contains(@class, "platform_img") or @class="vr_supported"]/@class').getall())
            yield steam_item