# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

#Database kısmı:
import psycopg2 as postgre #psycopg2 kütüphanesi postgre olarak import edildi.

class CvePipeline(object):
    
    def __init__(self): #Constructor. Nesne oluştuğu takdirde buradaki fonksiyonlar otomatik olarak çağrılır.
        self.create_connection()
        self.create_table()
        
    def create_connection(self): #Database bağlantısı için oluşturulan fonksiyon
        self.conn = postgre.connect(
                host='localhost',
                user='postgres',
                password='postgreMerve',
                database="cve"
        )
        self.curr = self.conn.cursor() #Veritabanı işlemlerini gerçekleştirebilmek için cursor oluşturuldu.
    
# Tablo veritabanında elle oluşturulduğu için def creatE_table() fonksiyonu kaldırıldı.
    def create_table(self): #Database'de tablo oluşturmak için oluşturulan fonksiyon
        self.curr.execute(""" DROP TABLE IF EXISTS cvetab""")
        self.curr.execute(""" CREATE TABLE cvetab(
                        CVE_ID text,
                        CWE_ID text,
                        VULNERABILITY_TYPE text,
                        PUBLISH_DATE text,
                        UPDATE_DATE text,
                        SCORE text,
                        SUMMARY text,
                        UNIQUE(CVE_ID)
                        )""")
        
    def process_item(self, item, spider): #Verileri database'deki tabloya eklemek için gereken fonksiyon
        self.store_db(item)
        return item
    
    def store_db(self, item): #Verileri tabloya eklemek için gereken SQL sorgusunun bulunduğu fonksiyon
        self.curr.execute("""INSERT INTO cvetab VALUES (%s,%s,%s,%s,%s,%s,%s)""", (
                item['CVE_ID'],
                item['CWE_ID'],
                item['VULNERABILITY_TYPE'],
                item['PUBLISH_DATE'],
                item['UPDATE_DATE'],
                item['SCORE'],
                item['SUMMARY']
        ))
        self.conn.commit() #Girilen verileri işleyebilmek için commit() fonksiyonu kullanıldı.
