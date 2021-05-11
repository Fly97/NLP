
@[TOC](构建影视圈知识图谱与问答系统)
# 1 影视圈数据梳理
原数据形式：
1.电影类型
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021050715304812.png)
2.演员介绍
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210507153518930.png)
3.电影介绍
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210507153629693.png)

## 1.1 数据导入neo4j知识图谱中

```python
# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher
import json
from tqdm import tqdm
import pandas as pd
import csv


graph = Graph('http://localhost:7474', username='******', password='******')
matcher = NodeMatcher(graph)


def create_node(_graph, _type, _name):
    node = Node(_type)
    node['name'] = _name
    _graph.create(node)
    return node


def create_node_all(_graph, _type, _name, operation):
    node = Node(_type)
    node['name'] = _name
    node['operation'] = operation
    _graph.create(node)
    return node


def create_rel(node1, node2, _graph, rel):
    relation = Relationship(node1, rel, node2)
    _graph.create(relation)



# 建立Genre
with open(r"C:\Users\Administrator\Desktop\csv\csv\genre.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2 or row[0] == 'gid':
            continue
        gid, gname = row
        print(int(gid), gname)

        node = Node('Genre')
        node['name'] = gname
        node['gid'] = str(gid)
        graph.create(node)


# 建立movie
with open(r"C:\Users\Administrator\Desktop\csv\csv\movie.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 5 or row[0] == 'mid':
            continue
        mid, title, introduction, rating, releasedate = row
        print(int(mid), title, introduction, rating, releasedate)

        node = Node('Movie')
        node['name'] = title
        node['mid'] = str(mid)
        node['introduction'] = introduction
        node['rating'] = str(rating)
        node['releasedate'] = str(releasedate)
        graph.create(node)


# 建立person
with open(r"C:\Users\Administrator\Desktop\csv\csv\person.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 6 or row[0] == 'pid':
            continue
        pid, birth, death, name, biography, birthplace = row
        print(int(pid), birth, death, name, biography, birthplace)
        node = Node('Person')
        node['name'] = name
        node['pid'] = str(pid)
        node['birth'] = str(birth)
        node['death'] = str(death)
        node['biography'] = biography
        node['birthplace'] = birthplace
        graph.create(node)

# 建立movie_to_genre
with open(r"C:\Users\Administrator\Desktop\csv\csv\movie_to_genre.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2 or row[0] == 'mid':
            continue
        mid, gid = row
        mid = str(int(mid))
        gid = str(int(gid))
        print(mid, gid)
        genre = matcher.match('Genre', gid=gid).first()
        movie = matcher.match('Movie', mid=mid).first()
        if genre and movie:
            create_rel(movie, genre, graph, 'belong')

# 建立person_to_movie
with open(r"C:\Users\Administrator\Desktop\csv\csv\person_to_movie.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2 or row[0] == 'pid':
            continue
        pid, mid = row
        pid = str(int(pid))
        mid = str(int(mid))
        print(pid, mid)
        person = matcher.match('Person', pid=pid).first()
        movie = matcher.match('Movie', mid=mid).first()
        if person and movie:
            create_rel(person, movie, graph, 'play')

```
图数据库展示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210507164952251.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxMzU5ODE3,size_16,color_FFFFFF,t_70)


## 1.2 构建数据类型
对影视圈的数进行分类，一共分类9类，如下：

```python
[
    {
        "参与": 0,
        "评分": 1,
        "出生": 2,
        "风格": 3,
        "上映": 4,
        "出演": 5,
        "总数": 6,
        "介绍": 7,
        "合作": 8
    },
    {
        "0": "参与",
        "1": "评分",
        "2": "出生",
        "3": "风格",
        "4": "上映",
        "5": "出演",
        "6": "总数",
        "7": "介绍",
        "8": "合作"
    }
]
```
每种类别都设计了对应的问题类型，如下：

```python
{
    "评分": [
        "nm得了多少分",
        "nm的评分有多少",
        "nm电影分数是多少",
        "nm评分",
        "nm的分数是多少"
    ],
    "上映": [
        "nm什么时候上映",
        "nm时间",
        "nm上映时间",
        "nm什么时候首映",
        "什么时候可以在影院看到nm",
        "nm什么时候首播"
    ],
    "风格": [
        "nm的风格是什么",
        "nm是什么风格的电影",
        "nm是什么类型的电影",
        "nm是什么类型的"
    ],
    "剧情": [
        "﻿nm的剧情是什么",
        "nm主要讲什么内容",
        "nm的剧情简介",
        "nm的主要情节",
        "nm的情节梗概",
        "nm简介"
    ],
    "参与": [
        "nm有哪些演员出演",
        "谁参与了nm",
        "nm有哪些演员出演",
        "nm都有谁参与",
        "nm是由哪些人演的",
        "nm这部电影的演员都有哪些"
    ],
    "简介": [
        "nnt",
        "nnt是",
        "nnt是谁",
        "nnt的简介",
        "谁是nnt",
        "nnt的信息"
    ],
    "出生": [
        "nnt的出生日期",
        "nnt的生日",
        "nnt的出生是什么时候",
        "nnt生日是什么时候",
        "nnt出生于哪一天",
        "nnt在哪出生"
    ],
    "出演": [
        "nnt演过什么电影",
        "nnt演过哪些电影",
        "nnt出演的电影",
        "nnt的作品",
        "nnt参与过电影",
        "nnt有哪些电影"
    ],
    "总数": [
        "nnt一共参演过多少电影",
        "nnt演过多少部电影",
        "nnt参演的电影有多少"
    ],
    "合作": [
        "nnt和nnr合作的电影有哪些",
        "nnt和nnr一起演过哪些电影",
        "nnt和nnr一起演过什么电影",
        "nnt、nnr一起演过哪些电影",
        "nnt和nnr合作了哪些电影",
        "nnt和nnr合拍过哪些电影"
    ]
}
# 其中nm-->电影
# 其中nnt-->演员
# 其中nnr-->演员
```
## 1.3 构建训练集、验证集
按照上述的模板生成数据集如下格式（总共67000条数据）：

```python
英雄得了多少分	评分
英雄什么时候上映	上映
英雄的风格是什么	风格
英雄简介	介绍
英雄有哪些演员出演	参与
英雄这部电影的演员都有哪些	参与
谁是古巨基	介绍
古巨基的出生日期	出生
古巨基演过什么电影	出演
古巨基一共参演过多少电影	总数
古巨基和陈建斌合作的电影有哪些	合作
```
*其实也可以直接训练问题模板，然后再意图识别（问题分类）的时候将实体去除*

# 2 意图识别
这对于影视问答的类型有限，使用本次使用的意图识别模型是文本分类模型
## 2.1 模型介绍
借鉴了[苏神（苏剑林）的bert4keras](https://github.com/bojone/bert4keras/)，使用bert预训练模型，尾部添加一个softmax分类器就ok了
## 2.2 模型搭建与训练
模型代码：

```python
# 加载预训练模型
bert = build_transformer_model(
    config_path=config_path,
    checkpoint_path=checkpoint_path,
    with_pool=True,
    return_keras_model=False,
)

output = Dropout(rate=0.1)(bert.model.output)
output = Dense(
    units=10, activation='softmax', kernel_initializer=bert.initializer
)(output)

model = keras.models.Model(bert.model.input, output)
model.summary()

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=Adam(2e-5),  # 用足够小的学习率
    metrics=['accuracy'],
)

model.fit(
        train_generator.forfit(),
        steps_per_epoch=len(train_generator),
        epochs=10,
        callbacks=[evaluator]
    )
```

# 3 问答系统
使用flask部署模型，将模型与neo4j联系起来构成问答系统
## 3.1 查询语句

```python
iftype == '风格':
	for word inkeyword:
	    sql = r'match (n:Movie{name:"' + word + r'"})-[r:belong]->(m)  return m.name'
	    out_data = self.graph.run(sql).data()
elif type == '上映':
    for word in keyword:
        sql = r'match (n:Movie{name:"' + word + r'"})  return n.releasedate'
        out_data = self.graph.run(sql).data()
elif type == '出演':
    for word in keyword:
        sql = r'match (n:Person{name:"' + word + r'"})-[r:play]->(m)  return m.name'
        out_data = self.graph.run(sql).data()
......
....
```
## 3.2 问答实例
直接看效果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210507160104504.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxMzU5ODE3,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210507160131367.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxMzU5ODE3,size_16,color_FFFFFF,t_70)

> 本项目（影视圈问答系统git库）链接：[https://github.com/Fly97/NLP/tree/main/movies](https://github.com/Fly97/movies)
> @misc{bert4keras,
  title={bert4keras},
  author={Jianlin Su},
  year={2020},
  howpublished={\url{https://bert4keras.spaces.ac.cn}},
}