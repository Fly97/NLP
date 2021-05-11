import csv
import json
import random


def is_all_chinese(chars: str) -> bool:
    return all('\u4e00' <= c <= '\u9fa5' or c.isdigit() for c in chars)


all_movie = []
with open(r"C:\Users\Administrator\Desktop\系统数据\影视圈\csv\movie.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 5 or row[0] == 'mid':
            continue
        mid, title, introduction, rating, releasedate = row
        if is_all_chinese(title):
            all_movie.append(title)

all_person = []
with open(r"C:\Users\Administrator\Desktop\系统数据\影视圈\csv\person.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 6 or row[0] == 'pid':
            continue
        pid, birth, death, name, biography, birthplace = row
        if is_all_chinese(name):
            all_person.append(name)


file = open(r'mytype.txt', 'r', encoding='utf-8')
mytype = json.load(file)
print(mytype)

file_w = open(r'all_data.txt', 'w', encoding='utf-8')
for movie in all_movie:
    # 评分
    for pf in mytype['评分']:
        line = str(pf).replace('nm', movie)
        file_w.write(line + '\t' + '评分' + '\n')


    for pf in mytype['上映']:
        line = str(pf).replace('nm', movie)
        file_w.write(line + '\t' + '上映' + '\n')


    for pf in mytype['风格']:
        line = str(pf).replace('nm', movie)
        file_w.write(line + '\t' + '风格' + '\n')


    for pf in mytype['剧情']:
        line = str(pf).replace('nm', movie)
        file_w.write(line + '\t' + '介绍' + '\n')


    for pf in mytype['参与']:
        line = str(pf).replace('nm', movie)
        file_w.write(line + '\t' + '参与' + '\n')


for person in all_person:
    for pf in mytype['简介']:
        line = str(pf).replace('nnt', person)
        file_w.write(line + '\t' + '介绍' + '\n')


    for pf in mytype['出生']:
        line = str(pf).replace('nnt', person)
        file_w.write(line + '\t' + '出生' + '\n')


    for pf in mytype['出演']:
        line = str(pf).replace('nnt', person)
        file_w.write(line + '\t' + '出演' + '\n')

    for pf in mytype['总数']:
        line = str(pf).replace('nnt', person)
        file_w.write(line + '\t' + '总数' + '\n')
        print(line)

    for pf in mytype['合作']:
        line = str(pf).replace('nnt', person)
        other_person = random.choice(all_person)
        line = str(line).replace('nnr', other_person)
        file_w.write(line + '\t' + '合作' + '\n')
        print(line)



# file = open(r'mytype.txt', 'r', encoding='utf-8')
# mytype = json.load(file)
# # print(mytype)
#
# file_w = open(r'other_data.txt', 'w', encoding='utf-8')
#
# for key, item in mytype.items():
#     if key == '剧情':
#         key = '简介'
#     for line in item:
#         line = str(line).replace('nnt', '')
#         line = str(line).replace('nm', '')
#         file_w.write(line + '\t' + key + '\n')