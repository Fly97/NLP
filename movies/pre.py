import json

def load_data(filename):
    """加载数据
    单条格式：(文本1, 文本2, 标签id)
    """
    D = []
    with open(filename, encoding='utf-8') as f:
        for l in f:
            text, label = l.strip().split('\t')
            D.append((text, label))
    return D

all_data = load_data(r'all_data.txt')
all_class = set(item[1] for item in all_data)
class_id = {value: index for index, value in enumerate(all_class)}
id_class = {value: key for key, value in class_id.items()}

data = []
data.append(class_id)
data.append(id_class)
file = open(r'类别.txt', 'w', encoding='utf-8')
json.dump(data, file, indent=4, ensure_ascii=False)