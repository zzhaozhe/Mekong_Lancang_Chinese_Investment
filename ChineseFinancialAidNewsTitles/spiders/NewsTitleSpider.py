import scrapy


class NewsSpider(scrapy.Spider):
    name = 'NewsSpider'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.100 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://opendevelopmentmekong.net/news/page/1/?odm_advanced_nav=1&filter_=1&filter_post_' \
              'type%5B0%5D=news-article&filter_s=China&filter_date_start&filter_date_end#038;filter_=1&filter_post_' \
              'type%5B0%5D=news-article&filter_s=China&filter_date_start&filter_date_end'
        yield scrapy.Request(url, headers = self.header, callback = self.parse_pages)

    def parse(self, response):
        next_url = response.xpath('//article/section[3]/div/div/div/a[@class = "next page-numbers"]/@href').extract()[0]
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback = self.parse_pages)

    def parse_pages(self, response):

        filename = "news.csv"
        f = open(filename, "w")

        headers = "ranking, title, directors, writers, stars\n"
        f.write(headers)

        for i in range(31):
            titles = response.xpath('//article/section[2]/div[3]/div/div/div/div/h5/a/text()').extract()[i]
            sources = response.xpath('//article/section[2]/div[3]/div/div/div/div/div/ul/li[@class = "news-source"]/a/text()').extract()[i]
            dates = response.xpath('//article/section[2]/div[3]/div/div/div/div/div/ul/li[@class = "date"]/text()[2]').extract()[i]
            contents = response.xpath('//article/section[2]/div[3]/div/div/div/div/section/div/p/text()').extract()[i]

            data = titles + "," + sources + "," + dates + "," + contents + "\n"
            f.write(data)

        f.close()



