# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher
import json
from tqdm import tqdm
import pandas as pd
import csv


graph = Graph('http://localhost:7474', username='neo4j', password='000000')
# graph = Graph('http://114.116.247.159:7474', username='neo4j', password='123456')
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



# # 建立Genre
# with open(r"C:\Users\Administrator\Desktop\csv\csv\genre.csv", 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if len(row) != 2 or row[0] == 'gid':
#             continue
#         gid, gname = row
#         print(int(gid), gname)
#
#         node = Node('Genre')
#         node['name'] = gname
#         node['gid'] = str(gid)
#         graph.create(node)


# # 建立movie
# with open(r"C:\Users\Administrator\Desktop\csv\csv\movie.csv", 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if len(row) != 5 or row[0] == 'mid':
#             continue
#         mid, title, introduction, rating, releasedate = row
#         print(int(mid), title, introduction, rating, releasedate)
#
#         node = Node('Movie')
#         node['name'] = title
#         node['mid'] = str(mid)
#         node['introduction'] = introduction
#         node['rating'] = str(rating)
#         node['releasedate'] = str(releasedate)
#         graph.create(node)


# # 建立person
# with open(r"C:\Users\Administrator\Desktop\csv\csv\person.csv", 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if len(row) != 6 or row[0] == 'pid':
#             continue
#         pid, birth, death, name, biography, birthplace = row
#         print(int(pid), birth, death, name, biography, birthplace)
#         node = Node('Person')
#         node['name'] = name
#         node['pid'] = str(pid)
#         node['birth'] = str(birth)
#         node['death'] = str(death)
#         node['biography'] = biography
#         node['birthplace'] = birthplace
#         graph.create(node)

# # 建立movie_to_genre
# with open(r"C:\Users\Administrator\Desktop\csv\csv\movie_to_genre.csv", 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if len(row) != 2 or row[0] == 'mid':
#             continue
#         mid, gid = row
#         mid = str(int(mid))
#         gid = str(int(gid))
#         print(mid, gid)
#         genre = matcher.match('Genre', gid=gid).first()
#         movie = matcher.match('Movie', mid=mid).first()
#         if genre and movie:
#             create_rel(movie, genre, graph, 'belong')

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

