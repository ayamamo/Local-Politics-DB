# -*- coding: utf-8 -*-

import os
import re
import json
import pandas as pd
import datetime as dt
import csv
import zenhan # mojimojiでない理由は"Microsoft Visual C++ 14.0"をインストールする必要があるため

file_prev = ''
file_ing = ''
file_same_name = 2

# pdのデフォルト値(6)だと議員idが丸められて表示されるため
# 議員idの桁数(16)桁まで表示できるようにする設定。
pd.options.display.precision = 16

def createCsv(x):
    global conf_att_json
    global conf_abu_json
    global attendances
    global abuses

    i = 0
    conf_att_json = 0
    conf_abu_json = 0
    while i <= len(x) -1:

        #file_attendance = open('hyogo3.csv', 'a', encoding='utf-8_sig')
        #csvlist = []
        #writer = csv.writer(file_attendance, lineterminator = '\n')
        file_prev = file_ing

        att_index = attendances.find(x[i])
        abu_index = abuses.find(x[i])
        if att_index != -1:
            conf_att_json += 1
            print ("json出席" + " : " + member_name[i])# れんくんが確認するためのブロック
            # csvへ議員idを出力すると丸められるので、
            # プロンプトに議員idを出力している
            # これが出力後、csvへコピペが必要
            #print (member_id[i])
            #csvlist.append(kaigi_id)
            #csvlist.append(zenhan.z2h(jis.group(0)[13:-4]).replace(" ", ""))
            #csvlist.append(member_id[i])
            #csvlist.append(member_name[i])
            #csvlist.append("1")
            #csvlist.append(file)
        if abu_index != -1:
            conf_abu_json += 1
            print ("json欠席" + " : " + member_name[i])# れんくんが確認するためのブロック
            # csvへ議員idを出力すると丸められるので、
            # プロンプトに議員idを出力している
            # これが出力後、csvへコピペが必要
            #print (member_id[i])
            #csvlist.append(kaigi_id)
            #csvlist.append(zenhan.z2h(jis.group(0)[13:-4]).replace(" ", ""))
            #csvlist.append(member_id[i])
            #csvlist.append(member_name[i])
            #csvlist.append("0")
            #csvlist.append(file)
        i += 1
        # 出力されたファイルから空白行を削除する必要があり
        #writer.writerow(csvlist)
        #file_attendance.close()

def findAllFiles(dir):
    for root, dirs, files in os.walk(dir):
      yield root
      for file in files:
        yield os.path.join(root, file)

for file in findAllFiles('C:\\Users\\20170906c\\AppData\\Local\\Programs\\Python\\Python37-32\\26.京都府\\204.宇治市\\h24'):
    if ".txt" in file and re.search('[0-9]{9}', file):

        kv = open('C:\\Users\\20170906c\\AppData\\Local\\Programs\\Python\\Python37-32\\attendance.json', 'r', encoding="utf-8_sig")
        df = pd.read_excel('C:\\Users\\20170906c\\AppData\\Local\\Programs\\Python\\Python37-32\\26.京都府.xlsx', usecols=[0, 2], Name=None)
        d = json.load(kv)
        jis = re.search('\d{9}.*', file)
        kaigi_date = jis.group(0)[:8]
        member_id = []
        member_name = []
        member_name_family = []

        if jis.group()[8:13] == "28100":
            i = 101
            while i < 111:
                jis_2 = jis.group()[:10] + str(i)
                i += 1

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)

        if jis.group()[8:13] == "26100":
            i = 101
            while i < 111:
                jis_2 = jis.group()[:10] + str(i)
                i += 1

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)

        if jis.group()[8:13] == "27100":
            i = 102
            while i < 128:
                jis_2 = jis.group()[:10] + str(i)
                i += 1

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)

        if jis.group()[8:13] == "27140":
            i = 141
            while i < 147:
                jis_2 = jis.group()[:10] + str(i)
                i += 1

                for i, rows in df.iterrows():
                    row = int(rows.id)
                    row = str(row)
                    index = jis_2.find(row[8:13])
                    giin_date = row[:8]
                    comb_date = int(kaigi_date) - int(giin_date)

                    if index != -1:
                        if comb_date > 0 and comb_date < 40000:
                            # rows.whoとしているのは、nameはpandasの予約語?なのか、
                            # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                            name = re.sub('\s', '', rows.who)
                            member_id.append(row)
                            member_name.append(name)



        print (file)
        for i, rows in df.iterrows():
            row = int(rows.id)
            row = str(row)
            index = jis.group(0).find(row[8:13])
            giin_date = row[:8]
            comb_date = int(kaigi_date) - int(giin_date)

            if index != -1:
                if comb_date > 0 and comb_date < 40000:
                    # rows.whoとしているのは、nameはpandasの予約語?なのか、
                    # 議員名をexcelファイルから抽出することが出来ないのでこうしています。
                    name = re.sub('\s', '', rows.who)
                    if re.search('\s', rows.who):
                        nameFamily, tmp = rows.who.split()
                        member_name_family.append(nameFamily)
                    member_id.append(row)
                    member_name.append(name)

        # 議員情報を抽出
        for k, v in d.items():
            index = jis.group(0).find(k)
            if index != -1:
                f = open(file, 'r')
                attendances = ""
                abuses = ""
                conf_att_txt = ""
                conf_abu_txt = ""
                flag = 0
                for line in f:
                    line = re.sub('\s', '', line)
                    # 取得位置を判定
                    if re.search(v[0], line):
                        flag = 1
                        conf_att_txt = re.search('[0-9０-９]+', line)
                    elif re.search(v[1], line):
                        flag = 2
                        conf_abu_txt = re.search('[0-9０-９]+', line)
                    elif re.search(v[2], line):
                        flag = 0
                    # 会議録に記載の出欠情報を各変数へ追加
                    if flag == 1:
                        attendances += line
                    if flag == 2:
                        abuses += line


                abuse_char = v[3]
                family_name = v[4]
            
        kaigi_id = ''
        file_ing = jis.group(0)[:13]
        file_prev = file_prev if 'file_prev' in globals() else 1
        # 同自治体、同日に会議が行われていた場合の処理
        if file_prev == file_ing:
            kaigi_id = file_ing + str(file_same_name).zfill(2)
            file_same_name += 1
        else:
            kaigi_id = file_ing + '01'
            file_same_name = 1

        if abuse_char != "":
            attendances = re.sub(abuse_char, 'abcd', attendances)
            abuse_char = "abcd"
            test = []
            if jis.group()[8:13] == "26211":
                test = re.split('◯', attendances)
                attendances = ""
                i = 0
                while i <= len(test) -1:
                    test2 = test[i].find(abuse_char)
                    if test2 != -1:
                        abuses += re.search('.*' + abuse_char, test[i]).group()
                        attendances += re.sub('.*' + abuse_char, '', test[i])
                    else:
                        attendances += test[i]
                    i += 1


            test = []
            if jis.group()[8:13] == "28100":
                i = 0
                tmp = []
                while i <= len(member_name) -1:
                    test_index = attendances.find('abcd' + member_name[i])
                    if test_index != -1: tmp.append(member_name[i])
                    if test_index != -1: attendances = attendances.replace('abcd' + member_name[i], '')
                    i += 1

                i = 0
                while i <= len(tmp) -1:
                    abuses += tmp[i]
                    i += 1



        #if abuse_char != "":
        if family_name == "1":
            if re.search('定例会|臨時会', file):
                createCsv(member_name)
            else:
                createCsv(member_name_family)
        else:
            createCsv(member_name)


        # れんくんが確認するためのブロック
        if conf_att_txt:
            conf_att_txt = conf_att_txt.group()
        else:
            conf_att_txt = 0
            if attendances.count("番"):
                conf_att_txt = attendances.count("番")
            elif attendances.count("、"):
                conf_att_txt = attendances.count("、") + 1
            elif attendances.count("議員"):
                conf_att_txt = attendances.count("議員")
        
        if conf_abu_txt:
            conf_abu_txt = conf_abu_txt.group()
        else:
            conf_abu_txt = 0
            if abuses.count("番"):
                conf_abu_txt = abuses.count("番")
            elif abuses.count("議員"):
                conf_abu_txt = abuses.count("議員")
        print ("会議録出席" + " : " + attendances)# れんくんが確認するためのブロック
        print ("会議録欠席" + " : " + abuses)# れんくんが確認するためのブロック
        
        print ("出席計算" + " : " + str(int(conf_att_txt) - int(conf_att_json)))
        print ("欠席計算" + " : " + str(int(conf_abu_txt) - int(conf_abu_json)))
        f.close()
        kv.close()

    else:
        print (file)
