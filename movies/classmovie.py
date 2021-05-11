#! -*- coding:utf-8 -*-
# 句子对分类任务，LCQMC数据集
# val_acc: 0.887071, test_acc: 0.870320
import json
import random
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from bert4keras.backend import keras, set_gelu, K
from bert4keras.tokenizers import Tokenizer
from bert4keras.models import build_transformer_model
from bert4keras.snippets import sequence_padding, DataGenerator, to_array
from bert4keras.snippets import open
from keras.layers import Dropout, Dense
from movies.train import data_generator
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

set_gelu('tanh')  # 切换gelu版本


class TextClass:
    maxlen = 128
    batch_size = 50
    config_path = r'E:\chinese_L-12_H-768_A-12\bert_config.json'
    checkpoint_path = r'E:\chinese_L-12_H-768_A-12\bert_model.ckpt'
    dict_path = r'E:\chinese_L-12_H-768_A-12\vocab.txt'
    label_dic = json.load(open(r'类别.txt', 'r', encoding='utf-8'))
    class_id = label_dic[0]
    id_class = label_dic[1]
    graph = tf.get_default_graph()
    model = None
    tokenizer = None

    def __init__(self):
        # 建立分词器
        self.tokenizer = Tokenizer(self.dict_path, do_lower_case=True)

        # 加载预训练模型
        bert = build_transformer_model(
            config_path=self.config_path,
            checkpoint_path=self.checkpoint_path,
            with_pool=True,
            return_keras_model=False,
        )
        output = Dropout(rate=0.1)(bert.model.output)
        output = Dense(
            units=10, activation='softmax', kernel_initializer=bert.initializer
        )(output)
        self.model = keras.models.Model(bert.model.input, output)
        self.model.load_weights(r'my_best_model.weights')
        # self.model.summary()

    def evaluate(self, data):
        total, right = 0., 0.
        for x_true, y_true in data:
            y_pred = self.model.predict(x_true).argmax(axis=1)
            y_true = y_true[:, 0]
            total += len(y_true)
            right += (y_true == y_pred).sum()
        return right / total

    def test(self):
        D = []
        with open(r'all_data.txt', encoding='utf-8') as f:
            for l in f:
                text, label = l.strip().split('\t')
                D.append((text, int(self.class_id[label])))
        # random.shuffle(D)
        # test_data = D[45000:55000]
        test_data = D
        test_generator = data_generator(test_data, self.batch_size)
        print(u'final test acc: %05f\n' % (self.evaluate(test_generator)))

    def predict(self, text):
        token_ids, segment_ids = self.tokenizer.encode(text, maxlen=self.maxlen)
        token_ids, segment_ids = to_array([token_ids], [segment_ids])
        input_data = [token_ids, segment_ids]
        with self.graph.as_default():
            y_pred = self.model.predict(input_data)
        # print('7类所有概率：', y_pred)
        y_index = y_pred.argmax(axis=1)
        key = str(y_index[0])
        # print('类别下标：', key)
        # print('类别：', self.id_class[key])
        return [self.id_class[key], y_pred.max()]


if __name__=='__main__':
    textclass = TextClass()
    textclass.test()
    # while 1:
    #     text = input('请输入：')
    #     out = textclass.predict(text)
    #     print(out)
