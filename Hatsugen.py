# -*- coding: utf-8 -*-

import os
import re
import json
import csv
import sys
import pandas as pd

file_prev = ''
file_prev_all = ''
file_ing = ''
file_same_name = 1

removePattern = "(（登壇）|─|～|―|─|～|┌|└|┐|│|┤|┘|├|┴|┼|┬|－|―|\"|\t|△)"
addPattern = "^(○|◎|◆|◯|＜)|(：.*。$)|^[0-9]{3}"
startPattern = "午.*(開.*会|開.*議)|(開.*会|開.*議).*午"
endPattern = "午.*時.*分.*(閉会|散会|延会)"
dict = {}
dict = {
    "26100": "京都市",
    "26201": "福知山市",
    "26202": "舞鶴市",
    "26203": "綾部市",
    "26204": "宇治市",
    "26205": "宮津市",
    "26206": "亀岡市",
    "26207": "城陽市",
    "26208": "向日市",
    "26209": "長岡京市",
    "26210": "八幡市",
    "26211": "京田辺市",
    "26212": "京丹後市",
    "26213": "南丹市",
    "26214": "木津川市",
    "27100": "大阪市",
    "27140": "堺市",
    "27202": "岸和田市",
    "27203": "豊中市",
    "27204": "池田市",
    "27205": "吹田市",
    "27206": "泉大津市",
    "27207": "高槻市",
    "27208": "貝塚市",
    "27209": "守口市",
    "27210": "枚方市",
    "27211": "茨木市",
    "27212": "八尾市",
    "27213": "泉佐野市",
    "27214": "富田林市",
    "27215": "寝屋川市",
    "27216": "河内長野市",
    "27217": "松原市",
    "27218": "大東市",
    "27219": "和泉市",
    "27220": "箕面市",
    "27221": "柏原市",
    "27222": "羽曳野市",
    "27223": "門真市",
    "27224": "摂津市",
    "27225": "高石市",
    "27226": "藤井寺市",
    "27227": "東大阪市",
    "27228": "泉南市",
    "27229": "四條畷市",
    "27230": "交野市",
    "27231": "大阪狭山市",
    "27232": "阪南市",
    "28100": "神戸市",
    "28201": "姫路市",
    "28202": "尼崎市",
    "28203": "明石市",
    "28204": "西宮市",
    "28205": "洲本市",
    "28206": "芦屋市",
    "28207": "伊丹市",
    "28208": "相生市",
    "28209": "豊岡市",
    "28210": "加古川市",
    "28212": "赤穂市",
    "28213": "西脇市",
    "28214": "宝塚市",
    "28215": "三木市",
    "28216": "高砂市",
    "28217": "川西市",
    "28218": "小野市",
    "28219": "三田市",
    "28220": "加西市",
    "28221": "篠山市",
    "28222": "養父市",
    "28223": "丹波市",
    "28224": "南あわじ市",
    "28225": "朝来市",
    "28226": "淡路市",
    "28227": "宍粟市",
    "28228": "加東市",
    "28229": "たつの市"
}

def findAllFiles(dir):
    for root, dirs, files in os.walk(dir):
      yield root
      for file in files:
        yield os.path.join(root, file)

def sameLine():
    global line
    global member
    global content
    global addPattern

    if re.search(addPattern, line):
        createCsv()
        # 発言者、役職、発言がそれぞれスペースで区切られており、
        # 発言者、役職と発言を区切るため、rsplit(sth, 1)とした
        if not "　" in line:
            # 発言者と発言が同一行にある自治体であるが、稀に
            # 役職名が長すぎるため、それらが同一行にない場合がある
            member = line
        elif v[1] == "em":
            # 全角スペースはjsonファイルで表現できないため
            member, content = line.rsplit("　", 1)
        else:
            member, content = line.rsplit(v[1], 1)
    else:
        content += line

def diffLine():
    global line
    global member
    global content
    global addPattern

    if re.search(addPattern, line):
        createCsv()
        member = line
    else:
        content += line

def createCsv():
    global member
    global content
    global day_serial

    # 会議idの付与
    global file_prev
    global file_prev_all
    global file_ing
    global file_same_name
    global jis
    kaigi_id = ''
    file_ing = jis.group()[:13]

    file_prev = file_prev if 'file_prev' in globals() else 1
    if file_prev == file_ing and file_prev_all == jis.group():
        kaigi_id = file_ing + str(file_same_name).zfill(2)
    elif file_prev == file_ing:
        file_same_name += 1
        kaigi_id = file_ing + str(file_same_name).zfill(2)
    else:
        kaigi_id = file_ing + '01'
        file_same_name = 1

    file_prev = file_ing
    file_prev_all = jis.group()

    member = re.sub('\s', '', member)
    content = re.sub('\n|\s', '', content)
    city_name = city_name_func()
    result = findGiin()
    member2 = member_name[result] if result is not None else ""# 議員idが抽出できた議員名を議員テーブルの表記へ変換
    id = member_id[result] if result is not None else 0
    member_jis2_append = member_jis2[result] if result is not None else 0
    votes_append = votes_list[result] if result is not None else 0
    kana_append = kana_list[result] if result is not None else 0
    age_append = age_list[result] if result is not None else 0
    gender_append = gender_list[result] if result is not None else 0
    party_name_append = party_name_list[result] if result is not None else 0
    newness_append = newness_list[result] if result is not None else 0
    title_append = title_list[result] if result is not None else 0


    flg = 0
    if not os.path.exists('26/' + kaigi_id + re.sub('\s|\.txt', '', jis.group()[13:]) + '.csv'):
        flg = 1
    else:
        flg = 0

    f = open('26/' + kaigi_id + re.sub('\s|\.txt', '', jis.group()[13:]) + '.csv', 'a', encoding='utf-8_sig')
    #f = open('27/' + jis.group()[8:13] + '.csv', 'a', encoding='utf-8_sig')
    csvlist = []
    writer = csv.writer(f, lineterminator = '\n')

    #csvlist.append(file)
    #csvlist.append(day_serial)
    if flg == 1:
        writer.writerow(['kaigi_id', 'giin_name', 'statement', 'giin_id', 'count', 'date', 'year', 'month', 'day', 'kaigi', 'auto_increment', 'jis', 'jis2', 'city_name', 'votes', 'name', 'name2', 'name3', 'kana', 'age', 'gender_code', 'gender', 'party_code', 'party_name', 'newness', 'title'])
    csvlist.append(str(kaigi_id))
    csvlist.append(member)
    csvlist.append(content)
    csvlist.append(str(id))
    csvlist.append(len(content))
    #csvlist.append(jis.group()[8:13])
    csvlist.append(jis.group()[0:4]+ "-" + jis.group()[4:6] + "-" + jis.group()[6:8])
    csvlist.append(jis.group()[0:4])
    csvlist.append(jis.group()[4:6])
    csvlist.append(jis.group()[6:8])
    csvlist.append(re.sub('\s|\.txt', '', jis.group()[13:]))
    csvlist.append("")# auto_increment
    csvlist.append(jis.group()[8:13])
    csvlist.append(member_jis2_append)
    csvlist.append(city_name)
    csvlist.append(votes_append)
    csvlist.append(member2)
    csvlist.append("")# name2
    csvlist.append("")# name3
    csvlist.append(kana_append)
    csvlist.append(age_append)
    csvlist.append("")# gender_code
    csvlist.append(gender_append)
    csvlist.append("")# party_code
    csvlist.append(party_name_append)
    csvlist.append(newness_append)
    csvlist.append(title_append)
    csvlist.append("")# elected

    writer.writerow(csvlist)
    f.close()

    content = ""
    day_serial += 1

def findGiin():

    # 発言者名が委員会のみ名字表記
    if v[2] == "1":
        if re.search('.*(定例会|臨時会).*', file):
            return fullName()
        else:
            return familyName()
    # 発言者名が定例会/臨時会ともに名字表記
    elif v[2] == "2":
        return familyName()
    else:
        return fullName()

def fullName():
    global member_id
    global member_name

    i = 0
    while i < len(member_name):
        index = member.find(member_name[i])
        if index != -1 and not "議長" in member:
            return i
        i += 1

def familyName():
    global member_id
    global member_name
    global member_name_family

    i = 0
    while i < len(member_name_family):
        index = member.find(member_name_family[i])
        if index != -1 and not "議長" in member:
            return i
        i += 1

def city_name_func():
    global d
    return dict[jis.group()[8:13]]

for file in findAllFiles('C:\\Users\\20160923\\Desktop\\shareBackup\\h30\\01.議事録DL\\26.京都府'):
    if ".txt" in file and re.search('[0-9]{9}', file):

        kv = open('C:\\Users\\20160923\\AppData\\Local\\Programs\\Python\\Python36-32\\workSpace\\hatsugen.json', 'r', encoding="utf-8_sig")
        df = pd.read_excel('C:\\Users\\20160923\\Desktop\\shareBackup\\h30\\02.議員テーブル\\26.京都府.xlsx', Name=None)
        d = json.load(kv)
        jis = re.search('\d{9}.*', file)
        member_id = []
        member_name = []
        member_name_family = []
        member_jis2 = []
        votes_list = []
        kana_list = []
        age_list = []
        gender_list = []
        party_name_list = []
        newness_list = []
        title_list = []

##### 市の中に区があるパターンの処理 start #####
        if jis.group()[8:13] == "26100":
            j = 101
            while j <= 111:
                jis_2 = jis.group()[:10] + str(j)

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    kaigi_date = jis.group(0)[:8]
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)
                    votes = str(rows.votes)
                    kana = str(rows.kana)
                    age = str(rows.age)
                    gender = str(rows.gender)
                    party_name = str(rows.party_name)
                    newness = str(rows.newness)
                    title = str(rows.title)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)
                            member_jis2.append(row[8:13])
                            votes_list.append(votes)
                            kana_list.append(kana)
                            age_list.append(age)
                            gender_list.append(gender)
                            party_name_list.append(party_name)
                            newness_list.append(newness)
                            title_list.append(title)
                j += 1

        if jis.group()[8:13] == "27100":
            j = 102
            while j <= 128:
                jis_2 = jis.group()[:10] + str(j)

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    kaigi_date = jis.group(0)[:8]
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)
                    votes = str(rows.votes)
                    kana = str(rows.kana)
                    age = str(rows.age)
                    gender = str(rows.gender)
                    party_name = str(rows.party_name)
                    newness = str(rows.newness)
                    title = str(rows.title)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)
                            member_jis2.append(row[8:13])
                            votes_list.append(votes)
                            kana_list.append(kana)
                            age_list.append(age)
                            gender_list.append(gender)
                            party_name_list.append(party_name)
                            newness_list.append(newness)
                            title_list.append(title)
                j += 1

        if jis.group()[8:13] == "27140":
            j = 141
            while j <= 147:
                jis_2 = jis.group()[:10] + str(j)

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    kaigi_date = jis.group(0)[:8]
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)
                    votes = str(rows.votes)
                    kana = str(rows.kana)
                    age = str(rows.age)
                    gender = str(rows.gender)
                    party_name = str(rows.party_name)
                    newness = str(rows.newness)
                    title = str(rows.title)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)
                            member_jis2.append(row[8:13])
                            votes_list.append(votes)
                            kana_list.append(kana)
                            age_list.append(age)
                            gender_list.append(gender)
                            party_name_list.append(party_name)
                            newness_list.append(newness)
                            title_list.append(title)
                j += 1

        if jis.group()[8:13] == "28100":
            j = 101
            while j <= 111:
                jis_2 = jis.group()[:10] + str(j)

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    kaigi_date = jis.group(0)[:8]
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)
                    votes = str(rows.votes)
                    kana = str(rows.kana)
                    age = str(rows.age)
                    gender = str(rows.gender)
                    party_name = str(rows.party_name)
                    newness = str(rows.newness)
                    title = str(rows.title)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)
                            member_jis2.append(row[8:13])
                            votes_list.append(votes)
                            kana_list.append(kana)
                            age_list.append(age)
                            gender_list.append(gender)
                            party_name_list.append(party_name)
                            newness_list.append(newness)
                            title_list.append(title)
                j += 1
##### 市の中に区があるパターンの処理 end #####

        # 議員情報を抽出
        for i, rows in df.iterrows():
            row = str(int(rows.id))
            #index = jis.group(0).find(row[6:11])# 大阪仕様 ####################
            index = jis.group(0).find(row[8:13])# 京都・兵庫仕様 ####################
            kaigi_date = jis.group(0)[:8]
            giin_date = row[:6] + "00"# 大阪仕様
            comb_date = int(kaigi_date) - int(giin_date)
            votes = str(rows.votes)
            kana = str(rows.kana)
            age = str(rows.age)
            gender = str(rows.gender)
            party_name = str(rows.party_name)
            newness = str(rows.newness)
            title = str(rows.title)

            # 会議が行われた日付に任期であった議員のみを抽出
            if comb_date > 0 and comb_date < 40000:
                if index != -1:
                    # attendance.pyを参照してください
                    if rows.who != 0:
                        name = re.sub('\s', '', rows.who)
                        if re.search('\s', rows.who):
                            nameFamily, tmp = rows.who.split()
                            member_name_family.append(nameFamily)
                        member_name.append(name)
                        member_id.append(row)
                        member_jis2.append(row[8:13])
                        votes_list.append(votes)
                        kana_list.append(kana)
                        age_list.append(age)
                        gender_list.append(gender)
                        party_name_list.append(party_name)
                        newness_list.append(newness)
                        title_list.append(title)

        for k, v in d.items():
                index = jis.group(0).find(k)
                if index != -1:
                    f = open(file, 'r')
                    member = ""
                    content = ""
                    flag = 0
                    day_serial = 0
                    print (file)

                    for line in f:
                        line = line.replace(",", "、")
                        line = re.sub(removePattern, '', line)
                        line = re.sub('\?$', '', line)

                        # startPatternの後のaddPatternから文字列を抽出するため
                        # flag = 1 と flag += 1 は上の文章を再現するために必要
                        if re.search(startPattern, line): flag = 1
                        if re.search('(' + addPattern + ')' + '.*長', line): flag += 1
                        if re.search('お.*うございます。', line): flag += 1# おはようございますや、あけましておめでとうございますにマッチさせるため
                        if re.search(endPattern, line): flag = 0

                        if flag >= 2:
                            # 発言者と発言が同一行にある場合
                            if v[0] == "1":
                                sameLine()
                            # 定例会・臨時会では発言者と発言が同一行にあるが
                            # 委員会では発言者と発言が同一行にない場合
                            elif v[0] == "2":
                                if re.search('定例会|臨時会', file):
                                    sameLine()
                                else:
                                    diffLine()
                            # 発言者と発言が同一行にない場合
                            else:
                                diffLine()
                    createCsv()
                else:
                    continue
    else:
    	print(file)
