import scrapy
from bs4 import BeautifulSoup
import pdfkit

# endcond=0
# alltext=''

class QuotesSpider(scrapy.Spider):
    name = "incorta"
    start_urls = [
        'https://docs.incorta.com/',
    ]

    def parse(self, response):
        # global endcond
        #global alltext
        #endcond=endcond+1
        page = response.url.split("/")[-2]
        filename = 'incorta-%s.html' % page
        #-------------------------
        #to add each page to an html file 
        #with open(filename, 'wb') as f:
            #f.write(response.body)
        #------------------------------
        #-------- appending all to 1 file while using beautiful soap------
        txt=response.body
        txt= self.repair_links(response.url,txt)

        txt=self.get_important_content(txt)

        self.savetext(txt)

        for href in response.css('div ul li div a::attr(href)'):
            yield response.follow(href, callback=self.parse)

        # if(endcond==1):
        #     pdfkit.from_string(str(alltext), 'incorta.pdf'.format(html_doc))



    
    def repair_links(self,page,text):
        soup = BeautifulSoup(text, 'html.parser')
        for i in soup.find_all('a'):
            if(i.attrs['href'][0]=='/'):
                i.attrs['href']=str(page)+str(i.attrs['href'])
        return soup





    def savetext(self,html_doc):
        #soup = BeautifulSoup(html_doc, 'html.parser')

        #txt=html_doc.get_text()
        filename = 'incorta.html'
        with open(filename, 'a+') as f:
            f.write(html_doc)


    def get_important_content(self, html_doc):
        #with open(html_doc) as f:
        #soup = BeautifulSoup(html_doc, 'html.parser')
        important_div = html_doc.findAll("div", {"class": ['col-md-9', 'col-lg-10', 'border-left', 'pl-4']})[0]
        return(str(important_div))
            #pdfkit.from_string(str(important_div), 'incorta.pdf'.format(html_doc))








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