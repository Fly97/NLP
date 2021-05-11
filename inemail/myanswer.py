# -*- coding: utf-8 -*-
import json
import copy
import ahocorasick
from inemail.similar import SIMI
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher




class Extra:
    wordlist = []
    actree = None
    all_word = []
    all_simi = {}
    graph = Graph('http://localhost:7474', username='neo4j', password='000000')
    matcher = NodeMatcher(graph)
    simi = SIMI()

    def __init__(self):
        pd_data1 = pd.read_excel(r"C:\Users\Administrator\Desktop\系统数据\内网邮件\邮箱用户手册整理.xlsx", header=0, sheet_name='neo')
        pd_data2 = pd.read_excel(r"C:\Users\Administrator\Desktop\系统数据\内网邮件\邮箱用户手册整理.xlsx", header=0, sheet_name='allword')
        pd_data3 = pd.read_excel(r"C:\Users\Administrator\Desktop\系统数据\内网邮件\邮箱用户手册整理.xlsx", header=0, sheet_name='simi')
        self.wordlist = list(set(pd_data1['keyword'].values))
        self.all_word = list(set(pd_data2['word'].values))
        # 建立相似词替换
        for index, item in pd_data3.iterrows():
            for key in item['min'].split('、'):
                self.all_simi[key] = item['main']
        # 建立AC树
        self.actree = ahocorasick.Automaton()
        for index, word in enumerate(self.wordlist):
            self.actree.add_word(word, (index, word))
        self.actree.make_automaton()

    def get_entity(self, question):
        region_wds = []
        for i in self.actree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_wds = list(set(final_wds))
        return final_wds

    def get_data(self, text):
        result = []
        keyword = self.get_entity(text)
        for word in keyword:
            question = None
            source = None
            pro_que = None
            all_solution = None
            # 确定问题
            sql_get_question = r'match (n:Mail_Keyword{name:"' + word + r'"})-[r:link]->(m:Mail_Question)  return m.name,m.source'
            out_question = self.graph.run(sql_get_question).data()
            all_question = []
            all_source = []
            for item in out_question:
                all_question.append(item['m.name'])
                all_source.append(item['m.source'])
            if all_question:
                index_question, pro_que = self.simi.predict_many(text, all_question)
                if pro_que < 0.65:
                    continue
                question = all_question[index_question]
                source = all_source[index_question]
                # 查找步骤
                sql_get_solution = r'match (p:Mail_Keyword{name:"' + word + r'"})-[*]->(n:Mail_Question{name:"' + question + r'"})-[*]->(m)  return m.operate'
                out_solution = self.graph.run(sql_get_solution).data()
                all_solution = []
                for item in out_solution:
                    all_solution.append(item['m.operate'])
            dic = {
                'keyword': word,
                'question': question,
                'question_probability': str(pro_que),
                'question_domain': source,
                'solution': all_solution,
            }
            result.append(dic)
        return result

    def get_neo_data(self, text):
        result = []
        keyword = self.get_entity(text)
        for word in keyword:
            question = None
            source = None
            pro_que = None
            all_solution = None
            # 确定问题
            sql_get_question = r'match (n:Mail_Keyword{name:"' + word + r'"})-[r:link]->(m:Mail_Question)  return m.name,m.source'
            out_question = self.graph.run(sql_get_question).data()
            all_question = []
            all_source = []
            for item in out_question:
                all_question.append(item['m.name'])
                all_source.append(item['m.source'])
            if all_question:
                index_question, pro_que = self.simi.predict_many(text, all_question)
                if pro_que < 0.5:
                    print('最大概率：', pro_que)
                    continue
                question = all_question[index_question]
                source = all_source[index_question]
                # 查找步骤
                sql_get_solution = r'match (p:Mail_Keyword{name:"' + word + r'"})-[*]->(n:Mail_Question{name:"' + question + r'"})-[*]->(m)  return m.operate'
                out_solution = self.graph.run(sql_get_solution).data()
                all_solution = []
                for item in out_solution:
                    all_solution.append(item['m.operate'])
            dic = {
                'keyword': word,
                'question': question,
                'question_probability': str(pro_que),
                'question_domain': source,
                'solution': all_solution,
            }
            result.append(dic)
        if not result:
            line = copy.copy(text)
            if '邮箱' in line:
                line = line.replace('邮箱', '邮件')
                result = self.get_data(line)
            elif '邮件' in line:
                line = line.replace('邮件', '邮箱')
                result = self.get_data(line)
        if not result:
            for word in keyword:
                item = self.get_code_info(word)[0]
                if len(item['relevant']) > 2:
                    max_index_list = self.simi.predict_manyto2(text, item['relevant'])
                    dic = {
                        'word': word,
                        'relevant': [item['relevant'][max_index_list[0]], item['relevant'][max_index_list[1]]]
                    }
                    result.append(dic)
                else:
                    result.append(item)
        return result

    def get_code_info(self, word):
        # 关键字
        sql1 = r'match (n:Mail_Keyword{name:"' + word + r'"})-[r:link]->(m:Mail_Question) return m.name'
        out = self.graph.run(sql1).data()
        result = []
        dic = {
            'word': word,
            'relevant': []
        }
        for item in out:
            dic['relevant'].append(item['m.name'])
        # 界面
        if not out:
            sql1 = r'match (n:Mail_Domain{name:"' + word + r'"})-[r:link]->(m) return m.name'
            out = self.graph.run(sql1).data()
            dic = {
                'word': word,
                'relevant': []
            }
            for item in out:
                dic['relevant'].append(item['m.name'])
        result.append(dic)
        return result

if __name__ == '__main__':
    extra = Extra()
    while 1:
        text = input('输入：')
        # text = '查看发信状态'
        if text in extra.all_word:
            out = extra.get_code_info(text)
        else:
            out = extra.get_neo_data(text)
        print('问题：', text)
        print('结果', json.dumps(out,indent=4, ensure_ascii=False))
        print('*'*100)


