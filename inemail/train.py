import random
from bert4keras.backend import keras, set_gelu
from bert4keras.tokenizers import Tokenizer
from bert4keras.models import build_transformer_model
from bert4keras.optimizers import Adam
from bert4keras.snippets import sequence_padding, DataGenerator
from keras.layers import Dropout, Dense


set_gelu('tanh')  # 切换gelu版本

maxlen = 128
batch_size = 20
config_path = r'E:\chinese_L-12_H-768_A-12\bert_config.json'
checkpoint_path = r'E:\chinese_L-12_H-768_A-12\bert_model.ckpt'
dict_path = r'E:\chinese_L-12_H-768_A-12\vocab.txt'


# 读取txt数据，返回数据lists[set(text1, text2, int(label))]
def read_data(input_file):
    """Reads a tab separated value file."""
    file = open(input_file, 'r', encoding='utf-8')
    lines = []
    for line in file.read().split('\n'):
        line = line.split("\t")
        text1, text2, label = line[0], line[1], line[2]
        text1 = text1.strip('\n')
        text2 = text2.strip('\n')
        label = label.strip('\n')
        lines.append((text1, text2, int(label)))
    return lines



# 加载数据集
all_data = read_data(r'E:\workspace\BF\inemail\data.txt')
# random.shuffle(all_data)

train_data = all_data[:15000]
random.shuffle(train_data)
random.shuffle(all_data)
valid_data = all_data[:2500]
test_data = all_data[2500:5000]

# random.shuffle(train_data)

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 数据生成器，迭代一次返回一个batch的数据，[batch_token_ids, batch_segment_ids], batch_labels
class data_generator(DataGenerator):
    """数据生成器
    """
    def __iter__(self, random=False):
        batch_token_ids, batch_segment_ids, batch_labels = [], [], []
        for is_end, (text1, text2, label) in self.sample(random):
            token_ids, segment_ids = tokenizer.encode(
                text1, text2
            )
            batch_token_ids.append(token_ids)
            batch_segment_ids.append(segment_ids)
            batch_labels.append([label])
            if len(batch_token_ids) == self.batch_size or is_end:
                batch_token_ids = sequence_padding(batch_token_ids)
                batch_segment_ids = sequence_padding(batch_segment_ids)
                batch_labels = sequence_padding(batch_labels)
                yield [batch_token_ids, batch_segment_ids], batch_labels
                batch_token_ids, batch_segment_ids, batch_labels = [], [], []


# 加载预训练模型
bert = build_transformer_model(
    config_path=config_path,
    checkpoint_path=checkpoint_path,
    with_pool=True,
    return_keras_model=False
)
# 添加dropout，起到去除过拟合作用
output = Dropout(rate=0.1)(bert.model.output)
# 添加输出层，softmax层，两个单元，分别为0,1的概率
output = Dense(
    units=2, activation='softmax', kernel_initializer=bert.initializer
)(output)

# 搭建模型，输入、输出
model = keras.models.Model(bert.model.input, output)
model.summary()

# 编译
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=Adam(2e-5),
    metrics=['accuracy'],
)


# 转换数据集
train_generator = data_generator(train_data, batch_size)
valid_generator = data_generator(valid_data, batch_size)
test_generator = data_generator(test_data, batch_size)


# 评测函数
def evaluate(data):
    total, right = 0., 0.
    for x_true, y_true in data:
        y_pred = model.predict(x_true).argmax(axis=1)
        y_true = y_true[:, 0]
        total += len(y_true)
        right += (y_true == y_pred).sum()
    return right / total

# 回调类
class Evaluator(keras.callbacks.Callback):
    def __init__(self):
        self.best_val_acc = 0.
    # 每迭代一次，调用一次
    def on_epoch_end(self, epoch, logs=None):
        val_acc = evaluate(valid_generator)
        if val_acc > self.best_val_acc:
            self.best_val_acc = val_acc
            model.save_weights('best_model.weights')
        test_acc = evaluate(test_generator)
        print(
            u'val_acc: %.5f, best_val_acc: %.5f, test_acc: %.5f\n' %
            (val_acc, self.best_val_acc, test_acc)
        )
        # print(
        #     u'val_acc: %.5f, best_val_acc: %.5f\n' %
        #     (val_acc, self.best_val_acc)
        # )

if __name__=='__main__':
    evaluator = Evaluator()
    model.fit_generator(
        train_generator.forfit(),
        steps_per_epoch=len(train_generator),
        epochs=10,
        callbacks=[evaluator]
    )
    model.save_weights('last_model.weights')


