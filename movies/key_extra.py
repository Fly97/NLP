# -*- coding: utf-8 -*-
import ahocorasick
import csv
from py2neo import Graph, Node, Relationship, NodeMatcher



def is_all_chinese(chars: str) -> bool:
    return all('\u4e00' <= c <= '\u9fa5' or c.isdigit() for c in chars)

class Extra:
    wordlist = []
    actree = None
    graph = Graph('http://localhost:7474', username='neo4j', password='000000')
    matcher = NodeMatcher(graph)

    def __init__(self):
        with open(r"C:\Users\Administrator\Desktop\系统数据\影视圈\csv\movie.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 5 or row[0] == 'mid':
                    continue
                mid, title, introduction, rating, releasedate = row
                if is_all_chinese(title):
                    self.wordlist.append(title)

        with open(r"C:\Users\Administrator\Desktop\系统数据\影视圈\csv\person.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 6 or row[0] == 'pid':
                    continue
                pid, birth, death, name, biography, birthplace = row
                if is_all_chinese(name):
                    self.wordlist.append(name)
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

    def get_neo_data(self, keyword, type, probability):
        result = []
        if probability < 0.65:
            return result
        if type == '风格':
            for word in keyword:
                sql = r'match (n:Movie{name:"' + word + r'"})-[r:belong]->(m)  return m.name'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['m.name'])
                    result.append(all_data)

        elif type == '上映':
            for word in keyword:
                sql = r'match (n:Movie{name:"' + word + r'"})  return n.releasedate'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['n.releasedate'])
                    result.append(all_data)

        elif type == '出演':
            for word in keyword:
                sql = r'match (n:Person{name:"' + word + r'"})-[r:play]->(m)  return m.name'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['m.name'])
                    result.append(all_data)

        elif type == '评分':
            for word in keyword:
                sql = r'match (n:Movie{name:"' + word + r'"})  return n.rating'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['n.rating'])
                    result.append(all_data)

        elif type == '参与':
            for word in keyword:
                sql = r'match (p:Person)-[r:play]->(m:Movie{name:"' + word + r'"}) return p.name'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['p.name'])
                    result.append(all_data)

        elif type == '出生':
            for word in keyword:
                sql = r'match (p:Person{name:"' + word + r'"}) return p.birthplace, p.birth'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['p.birth'])
                        all_data['answer'].append(out['p.birthplace'])
                    result.append(all_data)

        elif type == '总数':
            for word in keyword:
                sql = r'match (n:Person{name:"' + word + r'"})-[r:play]->(m)  return m.name'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    all_data['answer'].append(len(out_data))
                    result.append(all_data)

        elif type == '合作':
            if len(keyword) == 2:
                sql = r'match(n:Person{name:"' + keyword[0] + r'"})-[r:play]->(m)<-[d:play]-(p:Person{name:"' + keyword[1] + r'"}) return m.name'
                out_data = self.graph.run(sql).data()
                if out_data:
                    all_data = {}
                    all_data['key'] = '、'.join(keyword)
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data:
                        all_data['answer'].append(out['m.name'])
                    result.append(all_data)

        elif type == '介绍':
            for word in keyword:
                sql1 = r'match (p:Person{name:"' + word + r'"}) return p.biography'
                sql2 = r'match (m:Movie{name:"' + word + r'"}) return m.introduction'
                out_data1 = self.graph.run(sql1).data()
                out_data2 = self.graph.run(sql2).data()
                if out_data1:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data1:
                        all_data['answer'].append(out['p.biography'])
                    result.append(all_data)
                elif out_data2:
                    all_data = {}
                    all_data['key'] = word
                    all_data['question_type'] = type
                    all_data['probability'] = probability
                    all_data['answer'] = []
                    for out in out_data2:
                        all_data['answer'].append(out['m.introduction'])
                    result.append(all_data)
        return result

if __name__ == '__main__':
    text = '司马燕的生日'
    extra = Extra()
    # keyword = extra.get_entity(text)
    # print(keyword)

    result = extra.get_neo_data(['成龙', '吴辰君'], '总数', 0.8)
    print(result)






