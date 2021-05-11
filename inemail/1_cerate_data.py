import random

import pandas as pd



pd_data = pd.read_excel(r"C:\Users\Administrator\Desktop\系统数据\内网邮件\邮箱用户手册整理.xlsx", sheet_name='neo', header=0)
file_w = open(r'data.txt', 'w', encoding='utf-8')

all_question = {}
all_q = []
for index, item in pd_data.iterrows():
    keyword = item['keyword']
    question = item['question']
    another = item['another'].split('、')
    questions = []
    all_q.append(question)
    if item['keyword'] not in all_question.keys():
        all_question[keyword] = []
    questions.append(question)
    for que in another:
        questions.append(que)
    all_question[keyword].append(questions)

for key, item in all_question.items():
    for i in range(0, len(item)):
        # 相关
        for ii in range(1, len(item[i])):
            file_w.write(item[i][0] + '\t' + item[i][ii] + '\t' + str(1) + '\n')
        # 不相关1
        for j in range(i+1, len(item)):
            for jj in range(0, len(item[j])):
                file_w.write(item[i][0] + '\t' + item[j][jj] + '\t' + str(0) + '\n')

# 不相关2
for index, que in enumerate(all_q):
    another_indexs = random.sample(range(0, len(all_q)), 4)
    if index in another_indexs:
        another_indexs.remove(index)
    for ano in another_indexs:
        file_w.write(all_q[index] + '\t' + all_q[ano] + '\t' + str(0) + '\n')
file_w.close()








