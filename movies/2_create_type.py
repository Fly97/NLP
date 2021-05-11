import json

all_type = {}
all_type['评分'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【0】评分.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['评分'].append(line)


all_type['上映'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【1】上映.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['上映'].append(line)


all_type['风格'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【2】风格.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['风格'].append(line)

all_type['剧情'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【3】剧情.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['剧情'].append(line)


all_type['参与'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【4】某电影有哪些演员出演.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['参与'].append(line)


all_type['简介'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【5】演员简介.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['简介'].append(line)


all_type['出生'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【13】演员出生日期.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['出生'].append(line)


all_type['出演'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【7】某演员演了什么电影.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['出演'].append(line)


all_type['总数'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【12】某演员一共演过多少电影.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['总数'].append(line)

all_type['合作'] = []
file = open(r'C:\Users\Administrator\Desktop\系统数据\影视圈\template\【11】演员A和演员B合作了哪些电影.txt', 'r', encoding='utf-8')
for line in file.read().split('\n'):
    all_type['合作'].append(line)
print(all_type['总数'])

file = open(r'mytype.txt', 'w', encoding='utf-8')
json.dump(all_type, file, indent=4, ensure_ascii=False)