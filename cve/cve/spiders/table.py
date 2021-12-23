import scrapy #scrapy projeye eklendi.
import math #math modülü projeye eklendi.

#Parsing kısmı:
class TableSpider(scrapy.Spider):
    name = "table"
    start_urls = [
        'https://www.cvedetails.com/vulnerability-list/cvssscoremin-0/cvssscoremax-10/vulnerabilities.html',
    ] #Verileri çekmek için kullanılacak olan site
    
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }    

    def parse(self, response): #Verilerin parse edildiği fonksiyon
        totalNumber = int(response.css('div.paging b::text').get()) #Toplam kayıt sayısını kayıtların bulunduğu tüm sayfalardan çekiyor.
        totalPage = math.ceil(totalNumber/50) # Her sayfada 50 kayıt bulunuyor.
        pageURLs = response.css('div.paging a::attr(href)') #Veri çekilecek sayfaları çekiyor.

        for article in self.getData(response): #Her kayıt için HTTP request atan for döngüsü
            yield article #Her seferinde request döndürülür.
        
        self.getData(response)
        for page in range(1,totalPage): #Verileri çekmek için 1. sayfadan başlayıp sona kadar devam eden for döngüsü
            nextPageURL = 'https://www.cvedetails.com/' + pageURLs[page].get() #Bir sonraki sayfanın URL',
            yield scrapy.Request(nextPageURL, callback=self.getData) #Bir sonraki sayfanın URL'ine request

    def getData(self, response):
        table = response.css('table.searchresults') #Kayıtların bulunduğu kısmın id'si: searchresults
        summaryTD = table.css('td.cvesummarylong::text') #Kayıtların açıklamalarının bulunduğu class: cvesummarylong
        for index,row in enumerate(table.css('tr.srrowns')): #Kayıtların bulunduğu class: srrowns
            yield {
                'CVE_ID': row.css('td:nth-child(2) a:nth-child(1)::text').get(), #CVE_ID verilerinin bulunduğu kısım
                'CWE_ID': row.css('td:nth-child(3) a:nth-child(1)::text').get(), #CWE_ID verilerinin bulunduğu kısım
                'VULNERABILITY_TYPE': row.css('td:nth-child(5)::text').get().strip(), #VULNERABILITY_TYPE verilerinin bulunduğu kısım
                'PUBLISH_DATE': row.css('td:nth-child(6)::text').get(), #PUBLISH_DATE verilerinin bulunduğu kısım
                'UPDATE_DATE': row.css('td:nth-child(7)::text').get(), #UPDATE_DATE verilerinin bulunduğu kısım
                'SCORE': row.css('td:nth-child(8) div.cvssbox:nth-child(1)::text').get(), #SCORE verilerinin bulunduğu kısım
                'SUMMARY': summaryTD[index].get().strip() #SUMMARY verilerinin bulunduğu kısım. Ayrıca strip() metodu kaydı ',' ile ayırıp bir diğer kaydın bilgilerine geçmeyi sağlıyor.
            }