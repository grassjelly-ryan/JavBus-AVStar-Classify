# -*- coding: UTF8 -*-
import win32clipboard as wc
import win32con
from requests import Session
from bs4 import BeautifulSoup
from requests import utils
import re
import time


def getAllMovieOfActor(actor_info):
    headers = {'User-Agent': 'Mozilla/5.0',}
    cookiesDit = {'existmag': 'all'}
    url_root = 'https://www.seedmm.fun/'
    url = url_root + 'star/' + actor_info['Code'] + '/'
    flag = 1
    result_list = []

    while True:
        request = Session()
        request.proxies = {'https': 'http://127.0.0.1:1080/pac?auth=6sZoXM8Q3lZy eXZMnVP-&t=201909182318551455'}
        res = request.get(url + str(flag), headers=headers, cookies=cookiesDit)
        if res.status_code != 200:
            print(url + str(flag))
            break
        print(url + str(flag))
        res.content.decode('utf8', 'ignore').encode('gbk', 'ignore')
        soup = BeautifulSoup(res.text, 'html.parser')

        block = soup.find_all('a', class_='movie-box')
        for each_block in block:
            cover_title = each_block.find_all('img', src=re.compile('.*'), title=re.compile('.*'))
            cover = re.findall(r'thumb\/([\d|\w]+)\.jpg', str(cover_title[0]))
            title = re.findall(r'title=\"(.+)\"', str(cover_title[0]))
            if len(cover) != 0:
                cover = url_root + '/pics/cover/' + cover[0] + '_b.jpg'
            else:
                cover = 'No Cover Picture!'
            if len(cover) != 0:
                title = title[0]
            else:
                title = 'No Title!'

            num_date = each_block.find_all('date')
            num = str(num_date[0])[6:-7]
            date = str(num_date[1])[6:-7]

            detail_link = re.findall(r'\<a class\=\"movie-box\" href\=\"(.*)\"\>', str(each_block))[0]

            result_list.append({'Number':num, 'Title':title, 'Date':date, 'Cover Link':cover, 'Detail Link':detail_link})

        res.close()
        flag+=1

    with open(actor_info['Name']+'.md', 'w', encoding='utf-8') as f:
        for each_res in result_list:
            f.write('# ' + each_res['Number'] + '  \n')
            f.write('## ' + each_res['Date'] + '  \n')
            f.write(each_res['Title'] + '  \n')
            f.write('<' + each_res['Detail Link'] + '>  \n')
            f.write('<img src="' + each_res['Cover Link'] + '">  \n')

if __name__ == '__main__':
    actor_info_list = [
    {'Name':'松下紗栄子', 'Code':'opq'},
    {'Name':'友田彩也香', 'Code':'2di'}]

    for actor_info in actor_info_list:
        getAllMovieOfActor(actor_info)
        time.sleep(60)
