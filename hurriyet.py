# -*- coding: utf-8 -*-
#hurriyet.py
#2016-03-13
#author = Ahmet Aksoy
#Son güncelleme = 2016-03-13
#Python 3.5.1 ile test edildi
from selenium import webdriver
from urllib.parse import urlparse
from  turlib import *
import turkcemi
from derlem import *
import re
import time, datetime

xharfler= {'ÅŸ':'ş','ÄŸ':'ğ','â€™':"'",'Ä±':'ı','Ã¶':'ö','Ã¼':'ü','Ã§':'ç','Â':' ',
           'Ä°':'İ','Ã‡':'Ç','Ã–':'Ö','Åž':'Ş','Äž':'Ğ','Ãœ':'Ü','â€¦':'...',
           'â€œ':'“','â€':'”','Ã¢':'â','â€':'‘'}

adresler = "http://www.hurriyet.com.tr/index/?p=250"
modname = "hurriyet_py"

sayfasay =0
baslama = int(time.time())

outfilename = "temp/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+modname+".txt"
outfile = open(outfilename,"a",encoding="utf-8")

def get_base_url(url):
    o =urlparse(url)
    base_url=''
    if o.scheme > '':
        base_url += o.scheme+"://"
    base_url += o.netloc
    return base_url

#Varsayılan driver olarak Firefox kullanılacak
def get_driver():
    try:
        driver = webdriver.Firefox()
    except:
        driver = None
    return driver

def sayfa_oku(b,basla):
    sayfa = sayfaOku(b)
    if sayfa == None:
        print("{} Sayfa okunamadı: {}".format(modname,b))
        print("{} Sayfa okunamadı: {}".format(modname,b),file=outfile, flush=True)
        return

    #TODO: link açıklamaları kalkmayacak
    #sayfadan tüm linkleri kaldır
    #for tag in sayfa.findAll('a', href=True):
    #    tag.extract()

    paragraflar = sayfa.find_all('div',attrs={'itemprop' : 'articleBody'})
    if len(paragraflar)==0:
        print("Bu sayfada makale bulunmamaktadır.")
        print("Bu sayfada makale bulunmamaktadır.",file=outfile, flush=True)
        return
    for pr in paragraflar:
        #script bölümlerini temizle
        #[s.extract() for s in pr('script')]

        #http:// ile başlayan ardışık karakterleri sil
        #re.sub('(http.*)\s',' ',pr.text)

        #Başlık ile metin arasında boşluk karakteri olsun
        parag = " ".join(pr.findAll(text=True))
        #Farklı karakterler varsa düzelt
        for i in xharfler.keys():
            parag=re.sub(i,xharfler[i],parag)
        #Başlık ile normal yazı arasına boşluk eklenmesi lazım
        print(parag)
        print(parag,file=outfile,flush=True)
        if (turkcemi.turkcemi(parag, fout=outfile) == True) and (len(parag)>=400):
            print("Bu metin Türkçedir")
            print("Bu metin Türkçedir", file=outfile, flush=True)
            print("{} {:06d} {} {}".format(damgatar(), sayfasay,modname,b), flush=True)
            print("{} {:06d} {} {}".format(damgatar(),sayfasay,modname,b),file=outfile, flush=True)
            txttest = TXTDerlemTRText(parag)
            print("{} {} Toplam çalışma süresi = {} saniye".format(damgatar(),modname,time.perf_counter()-basla),flush=True)
            print("{} {} Toplam çalışma süresi = {} saniye".format(damgatar(),modname,time.perf_counter()-basla),file=outfile,flush=True)
        else:
            print(modname+" Bu metin Türkçe değildir veya yeterli sayıda geçerli Türkçe sözcük barındırmamaktadır.")
            print(modname+" Bu metin Türkçe değildir veya yeterli sayıda geçerli Türkçe sözcük barındırmamaktadır.",file=outfile,flush=True)

def load_arsiv_page(driver,adres):
    global sayfasay
    basla = time.perf_counter()
    if adres[-1]=='/': adres = adres[:-1]
    base_url = get_base_url(adres)
    driver.get(adres)
    elements = driver.find_elements_by_xpath("//h3/a[@href]")
    n=len(elements)
    for a in elements:
        try:
            b = a.get_attribute('href')
        except Exception as e:
            print("{} Exception -1: {}".format(modname,e))
            print("{} Exception -1: {}".format(modname,e),file=outfile, flush=True)
            continue
        if b is None: continue
        if len(b)==0: continue
        if b[-1]=='/': b = b[:-1]
        if b == base_url: continue
        if not b.startswith(base_url): continue
        if b == adres: continue
        if b == base_url+"/index": continue
        sayfasay += 1
        print("\n{} {} {} {:05d} {}".format(damgatar(), modname, gecen_sure(baslama), sayfasay, b))
        print("\n{} {} {} {:05d} {}".format(damgatar(), modname, gecen_sure(baslama), sayfasay, b),file=outfile,flush=True)
        #link başka bir siteye ait olmasın
        if base_url in b:
            sayfa_oku(b,basla)
        else:
             print(modname+" Link başka siteye aittir: {}".format(b))
             print(modname+" Link başka siteye aittir: {}".format(b),file=outfile,flush=True)

def main():
    sene = 2011
    if str(sene) not in GENSOZLUK_DOSYA_ADI:
        print("Rapor yılı derlem.py GENSOZLUK_DOSYA_ADI'nda hatalı tanımlanmış. Lütfen düzeltin!")
        return
    driver = get_driver()
    pagestart = 1
    pageend=11
    if driver != None:
        for pageno in range(pagestart,pageend):
            adres = "http://www.hurriyet.com.tr/index/?p="+"{}&d={}".format(pageno,sene)
            print("\n{} SayfaNo:{:06d} {}".format(damgatar(), pageno,adres), flush=True)
            print("\n{} SayfaNo:{:06d} {}".format(damgatar(), pageno,adres),file=outfile, flush=True)
            load_arsiv_page(driver,adres)
        driver.quit()

    outfile.close()

if __name__ == "__main__":
    gensozluk_oku()
    main()
    """
    b = "http://www.hurriyet.com.tr/basbakan-davutoglundan-onemli-aciklamalar-40067609"
    basla = time.perf_counter()
    sayfa_oku(b,basla)
    """
