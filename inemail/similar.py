import heapq
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from bert4keras.backend import keras
from bert4keras.tokenizers import Tokenizer
from bert4keras.models import build_transformer_model
from bert4keras.snippets import sequence_padding, DataGenerator, to_array
from keras.layers import Dropout, Dense
from inemail.train import data_generator
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


class SIMI:
    maxlen = 128
    batch_size = 20
    config_path = r'E:\chinese_L-12_H-768_A-12\bert_config.json'
    checkpoint_path = r'E:\chinese_L-12_H-768_A-12\bert_model.ckpt'
    dict_path = r'E:\chinese_L-12_H-768_A-12\vocab.txt'
    graph = None
    model =None
    # 建立分词器
    tokenizer = None
    def __init__(self):
        self.tokenizer = Tokenizer(self.dict_path, do_lower_case=True)
        self.graph = tf.get_default_graph()
        # 加载预训练模型
        bert = build_transformer_model(
            config_path=self.config_path,
            checkpoint_path=self.checkpoint_path,
            with_pool=True,
            return_keras_model=False,
        )
        # 添加dropout，起到去除过拟合作用
        output = Dropout(rate=0.1)(bert.model.output)
        # 添加输出层，softmax层，两个单元，分别为0,1的概率
        output = Dense(
            units=2, activation='softmax', kernel_initializer=bert.initializer
        )(output)
        # 搭建模型，输入、输出
        self.model = keras.models.Model(bert.model.input, output)
        # model.summary()
        self.model.load_weights(r'E:\workspace\BF\inemail\last_model.weights')

    # 评测函数
    def evaluate(self, data):
        total, right = 0., 0.
        for x_true, y_true in data:
            y_pred = self.model.predict(x_true).argmax(axis=1)
            y_true = y_true[:, 0]
            total += len(y_true)
            right += (y_true == y_pred).sum()
        return right / total

    def test(self):
        file = open(r'E:\workspace\BF\inemail\data.txt', 'r', encoding='utf-8')
        lines = []
        for line in file.read().split('\n'):
            line = line.split("\t")
            text1, text2, label = line[0], line[1], line[2]
            text1 = text1.strip('\n')
            text2 = text2.strip('\n')
            label = label.strip('\n')
            lines.append((text1, text2, int(label)))
        test_data = lines[:5000]
        test_generator = data_generator(test_data, self.batch_size)
        test_acc = self.evaluate(test_generator)
        print(u'test_acc: %.5f\n' %(test_acc))

    def predict_two(self, text1, text2):
        # 两个句子计算相似度
        token_ids, segment_ids = self.tokenizer.encode(text1, text2)
        token_ids, segment_ids = to_array([token_ids], [segment_ids])
        input_data = [token_ids, segment_ids]
        with self.graph.as_default():
            results = self.model.predict(input_data)
        # print(results)
        # print(results.argmax(axis=1))
        return results.argmax(axis=1)

    def predict_many(self, main_text, texts):
        lines = []
        for text in texts:
            lines.append((main_text, text, None))
        # 多个中找最相似的句子
        test_D = data_generator(lines, self.batch_size)
        with self.graph.as_default():
            results = self.model.predict_generator(test_D.__iter__(), steps=len(test_D))
        results = results[:, 1]
        result_index = results.argmax(axis=0)
        # print(results)
        # if results[result_index] > 0.5:
        #     print(main_text)
        #     print('最相似的标准问题是：', texts[result_index])
        return result_index, results[result_index]

    def predict_manyto2(self, main_text, texts):
        lines = []
        for text in texts:
            lines.append((main_text, text, None))
        # 多个中找最相似的句子
        test_D = data_generator(lines, self.batch_size)
        with self.graph.as_default():
            results = self.model.predict_generator(test_D.__iter__(), steps=len(test_D))
        results = list(results[:, 1])
        result_index_list = list(map(results.index, heapq.nlargest(2, results)))
        return result_index_list

    def find_false(self):
        file = open(r'E:\workspace\BF\inemail\data.txt', 'r', encoding='utf-8')
        file_w = open(r'E:\workspace\BF\inemail\wrong_data.txt', 'w', encoding='utf-8')
        for index, line in enumerate(file.read().split('\n')):
            if index > 6650:
                break
            line = line.split("\t")
            text1, text2, label = line[0], line[1], line[2]
            text1 = text1.strip('\n')
            text2 = text2.strip('\n')
            label = label.strip('\n')
            pre_label = self.predict_two(text1, text2)
            if int(label) != int(pre_label[0]):
                print(text1, text2, str(label), str(pre_label[0]))
                file_w.write(text1 + '  ' + text2 + '   ' + str(label) + '  ' + str(pre_label[0]) + '\n')


if __name__ == '__main__':
    simi = SIMI()
    # 测)试单条数据
    out = simi.predict_two('如何扩展客户信息', '附件限制')
    print(out[0])

    # # 测试多条数据
    # main_text = r'添加附件'
    # texts = [r'如何添加普通附件', r'如何添加超大附件', r'附件限制', r'无法上传附件']
    # out2 = simi.predict_many(main_text, texts)
    # print(out2)

    # simi.find_false()



