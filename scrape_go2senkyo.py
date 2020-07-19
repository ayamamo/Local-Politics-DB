# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://go2senkyo.com/local/jichitai/2409/gikai'

floor = []

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

for table in soup.find_all('table', class_='p_local_senkyo_table m_table'):
    for a in table.find_all('a'):
        floor.append(a.get('href'))

#print (floor)
while len(floor) > 0:
    try:
        r = requests.get(floor[0])
    except:
        print ('except 1')
        pass
    soup = BeautifulSoup(r.text, 'lxml')
    floor.pop(0)
    print (len(floor))

    for table in soup.find_all('table', class_='m_senkyo_data'):
        for td in table.find('td'):
            date = re.sub('年|月|日', '', td)

    for table in soup.find_all('table', class_='m_senkyo_result_table'):
        for tr in table.find_all('tr'):
            party = ''
            result = ''

            # 書き出しファイルの初期化
            f = open("osaka.csv", 'a')
            writer = csv.writer(f, lineterminator='\n')
            csvlist = []

            name = tr.find('a')
            tmp = tr.find('p', class_='m_senkyo_result_data_para').contents[0].text# 年齢と性別が同じ要素に格納されているため
            age, gender = tmp.split('(')
            incumbentRookie = tr.find('p', class_='m_senkyo_result_data_para').contents[1].text
            numberVotes = tr.find('td', class_='right').text
            title = tr.find('p', class_='m_senkyo_result_data_para small').text
            if tr.find('p', class_='m_senkyo_result_data_circle') is not None:# 所属政党の記載がない場合があるため
                party = tr.find('p', class_='m_senkyo_result_data_circle').text
            if tr.find('td', class_='left red') is not None:
                result = tr.find('td', class_='left red').img.get('alt')
            kana = re.search('[ア-ン].*', name.text)
            cChar = re.sub('\t|\n', '', name.next_element)# 姓名の間はスペースが欲しいから
            numberVotes = re.sub('\s', '', numberVotes)
            gender = re.sub('\)', '', gender)
            csvlist.append(numberVotes)
            csvlist.append(date)
            csvlist.append(result)
            csvlist.append(cChar)
            csvlist.append(kana.group())
            csvlist.append(age)
            csvlist.append(gender)
            csvlist.append(party)
            csvlist.append(incumbentRookie)
            csvlist.append(title)
            writer.writerow(csvlist)
            f.close()
