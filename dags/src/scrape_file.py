import requests as req
from bs4 import BeautifulSoup as bs
import csv
import datetime
import pytz

tz = pytz.timezone('Asia/Jakarta')        
current_time = datetime.datetime.now(tz)
output_path = '/home/milim/airflow/dags_folder/data_result/'
day = current_time.day
month = current_time.month
year = current_time.year
tgl = f"_{month:02d}_{day:02d}_{year}"

def sc_detik():
    with open(f'{output_path}ress_detik.csv','w')as file:
        wr = csv.writer(file, delimiter='|')
        wr.writerow(['title','released','author','url','content','platform'])

        tgls = f"{month:02d}/{day:02d}/{year}"
        url = f"https://news.detik.com/indeks?date={tgls}"
        ge = req.get(url).text
        sop = bs(ge,'lxml')
        try:
            paging = sop.find_all('div','pagination text-center mgt-16 mgb-16')[0].find_all('a')[-2]
            last_page = paging.text
        except:
            last_page = 1
        for page in range(1,int(last_page)+1):
            try:
                url_ = f'https://news.detik.com/indeks/{page}?date={tgls}'
                ge_ = req.get(url_).text
                sop_ = bs(ge_,'lxml')
                contai = sop_.find_all('div',class_='media__text')
                months = {'jan': '01','feb':'02','mar':'03','apr':'04','mei':'05','jun':'06','jul':'07','agu':'08','sep': '09', 'okt': '10', 'nov': '11', 'des': '12'}
                for x in contai:
                    
                    link = x.find('a')['href']

                    ge_a = req.get(f"{link}?single=1").text
                    sop_a = bs(ge_a,'lxml')
                    try:
                        times = sop_a.find('div',class_='detail__date').text.split()
                        times[2] = months.get(times[2].lower(), times[2])
                        tgl_ = f"{times[1]}/{times[2]}/{times[3]} {times[4]} {times[5]}"
                        author = sop_a.find('div',class_='detail__author').text.split(' - ')
                        title = sop_a.find('h1',class_='detail__title').text.strip()
                        content = sop_a.find_all('div',class_='detail__body-text itp_bodycontent')
                        for i in content:
                            isi = [x.text for x in i.find_all('p')]
                            ress_isi = ''.join(isi).replace('\n', '').replace('ADVERTISEMENT','').replace('SCROLL TO RESUME CONTENT','')
                            try:
                                wr.writerow([title,tgl_,author[0],link,ress_isi,'detik'])
                            except:
                                pass
                    except:pass
            except:pass    


def sc_kompas():
    with open(f'{output_path}ress_kompas.csv','w')as file:
        wr = csv.writer(file, delimiter=',')
        wr.writerow(['title','released','author','url','content','platform'])
        tgls = f"{year}-{month:02d}-{day:02d}"
        url = f"https://indeks.kompas.com/?site=all&date={tgls}"
        ge = req.get(url).text
        sop = bs(ge,'lxml')
        try:
            paging = sop.find_all('div',class_='paging__item')[-2]
            last_page = paging.find('a')['data-ci-pagination-page']
        except:
            last_page = 1
        for page in range(1,int(last_page)+1):
            try:
                url_ = f"https://indeks.kompas.com/?site=all&date={tgls}&page={page}"
                ge_ = req.get(url_).text
                sop_ = bs(ge_,'lxml')
                row = sop_.find_all('div','article__list clearfix')
                for art in row:
                    title = art.find('h3',class_='article__title article__title--medium').text.replace('\n','')
                    link = art.find('a',class_='article__link')['href']
                    art_tgl = art.find('div',class_='article__date').text.replace(',','')

                    ge_a = req.get(f"{link}?page=all").text
                    sop_a = bs(ge_a,'lxml')
                    content = sop_a.find_all('div',class_='read__content')
                    author = sop_a.find('div',{'class': 'read__credit__item', 'id': 'penulis'}).find('a').text
                    
                    for i in content:
                        isi = [x.text for x in i.find_all('p') if x.text.startswith('Baca juga') == False]
                        ress_isi = ''.join(isi)
                        
                        try:
                            wr.writerow([title,art_tgl,author,link,ress_isi,'kompas'])
                        except:
                            pass
            except:pass




