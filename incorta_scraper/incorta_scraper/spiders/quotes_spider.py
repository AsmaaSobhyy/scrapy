import scrapy
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "incorta"
    start_urls = [
        'https://docs.incorta.com/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'incorta-%s.html' % page
        #-------------------------
        #to add each page to an html file 
        #with open(filename, 'wb') as f:
            #f.write(response.body)
        #------------------------------
        #-------- appending all to 1 file while using beautiful soap------
        txt=response.body
        self.gettext(txt)

        for href in response.css('div ul li div a::attr(href)'):
            yield response.follow(href, callback=self.parse)



    def gettext(self,html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        txt=soup.get_text()
        filename = 'incorta.txt'
        with open(filename, 'a+') as f:
            f.write(txt)










        # next_page = response.css('a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #     f.write(response.body)