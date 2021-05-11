# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher
import json
from tqdm import tqdm
import pandas as pd


graph = Graph('http://localhost:7474', username='neo4j', password='000000')
matcher = NodeMatcher(graph)



def create_node(_graph, _type, _name):
    node = Node(_type)
    node['name'] = _name
    _graph.create(node)
    return node

soid = 1
def create_node_operate(_graph, _type, _name, operate):
    global soid
    solu_node = matcher.match('Mail_Solution', soid=str(soid)).first()
    while solu_node:
        soid += 1
        solu_node = matcher.match('Mail_Solution', soid=str(soid)).first()
    node = Node(_type)
    node['name'] = _name
    node['soid'] = str(soid)
    node['operate'] = operate
    _graph.create(node)
    soid += 1
    return node

def create_node_question(_graph, _type, _name, source):
    node = Node(_type)
    node['name'] = _name
    node['source'] = source
    _graph.create(node)
    return node


def create_rel(node1, node2, _graph, rel):
    relation = Relationship(node1, rel, node2)
    _graph.create(relation)

'''
System
Mail_Domain
Mail_Keyword
Mail_Question
Mail_Solution
'''

pd_data = pd.read_excel(r"C:\Users\Administrator\Desktop\系统数据\内网邮件\邮箱用户手册整理.xlsx", header=0, sheet_name='neo')

for index, item in tqdm(pd_data.iterrows()):
    system = item['system']
    domain1 = item['first']
    domain2 = item['second']
    keyword = item['keyword']
    question = item['question']
    solution = item['operate']
    all_solu = solution.split('\n')

    # 创建系统
    sys_node = matcher.match('System', name=system).first()
    if not sys_node:
        sys_node = create_node(graph, 'System', system)

    # 创建界面1
    do1_node = matcher.match('Mail_Domain', name=domain1).first()
    if not do1_node:
        do1_node = create_node(graph, 'Mail_Domain', domain1)

    # 创建界面2
    do2_node = matcher.match('Mail_Domain', name=domain2).first()
    if not do2_node:
        do2_node = create_node(graph, 'Mail_Domain', domain2)

    # 创建关键字
    key_node = matcher.match('Mail_Keyword', name=keyword).first()
    if not key_node:
        key_node = create_node(graph, 'Mail_Keyword', keyword)

    # 创建问题
    que_node = matcher.match('Mail_Question', name=question).first()
    if not que_node:
        que_node = create_node_question(graph, 'Mail_Question', question, domain1 + '、' + domain2)

    # 创建解决方案
    solu_node = create_node_operate(graph, 'Mail_Solution', 'OP1', all_solu[0])


    # 创建系统->界面1
    create_rel(sys_node, do1_node, graph, 'link')

    # 创建界面1->界面2
    create_rel(do1_node, do2_node, graph, 'link')

    # 创建界面2->关键字
    create_rel(do2_node, key_node, graph, 'link')

    # 创建关键字->问题
    create_rel(key_node, que_node, graph, 'link')

    # 创建问题->解决方案
    create_rel(que_node, solu_node, graph, 'link')

    count = 2
    if len(all_solu) > 1:
        for solu in all_solu[1:]:
            # 创建下一步操作
            name = 'OP' + str(count)
            next_node = create_node_operate(graph, 'Mail_Solution', name, solu)
            # 创建解决方案->解决方案
            create_rel(solu_node, next_node, graph, 'link')
            solu_node = next_node
            count += 1

