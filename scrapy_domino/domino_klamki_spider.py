import scrapy


class DominoSpider(scrapy.Spider):
    name = 'domino'
    start_urls = ['http://www.domino.pl/klamki/produkty/lista/',
                  'http://www.domino.pl/klamki/produkty/lista/2'
                  ]

    def parse(self, response):
        for href in response.xpath('//div/p[@class="product-txt"]/a/@href'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)
        next_page = response.xpath('//ul/li[@class="hidden-xs"]/a/@href').extract()[2]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        try:
            ean = int(response.xpath('//div[@class="col-md-7 col-xs-12"]/table/tr[6]/td[3]/text()').extract_first())
        except TypeError:
            ean = int(response.xpath('//div[@class="col-md-7 col-xs-12"]/table/tr[5]/td[3]/text()').extract_first())
        except ValueError:
            ean = response.xpath('//div[@class="col-md-7 col-xs-12"]/table/tr[5]/td[3]/text()').extract_first()
        name = response.xpath('//div[@class="col-md-7 col-xs-12"]/table/tr[2]/td[3]/text()').extract_first()
        yield {
                'ean': ean,
                'product name': name,
                'Url': response.url,
        }

