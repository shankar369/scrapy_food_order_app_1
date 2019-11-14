# -*- coding: utf-8 -*-
import scrapy


class HomepageSpider(scrapy.Spider):
    name = 'homepage'
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    #allowed_domains = ['www.zomato.com']
    start_urls = ["https://www.swiggy.com"]
    def __init__(self):
        self.domain = "https://www.swiggy.com"
        self.page_no = 2


    # def restaurent_link(self,response):
    #     main_pages_of_restaurents = response.xpath('//a[@class="_1j_Yo"]/@href').extract()
    #     print(main_pages_of_restaurents)

    def save_restaurent_page(self,response):
        name = response.url.split("https://www.swiggy.com/restaurants/")[1]+'.html'
        file = open(name,'w',encoding="utf-8")
        file.write(response.text)
        file.close()
        #print("************************",response.url,"************************")


    def place_page(self,response):
        pagination = response.xpath('//a[@class="_1FZ7A"]').extract()
        if(pagination):
            main_pages_of_restaurents = response.xpath('//a[@class="_1j_Yo"]/@href').extract()
            for main_page_of_restaurent in main_pages_of_restaurents:
                yield scrapy.http.Request(url = self.domain+main_page_of_restaurent,callback = self.save_restaurent_page)
            #print(main_pages_of_restaurents)
            link = ''
            if("?page=" in response.url):
                link = response.url.split("=")[0]+"="+str(self.page_no)
            else:
                link = response.url+"?page=1"
            self.page_no = self.page_no+1
            yield scrapy.http.Request(url = response.urljoin(link),callback = self.place_page)

    def parse(self, response):
        print("***********************************")
        places = response.xpath('//a[@class="_3TjLz b-Hy9"]/@href').extract()
        #for place in places:
        yield scrapy.http.Request(url = response.urljoin(self.domain+places[0]),callback = self.place_page)
        #print(places)
        pass
