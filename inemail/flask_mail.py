from flask import *
from inemail.myanswer2 import Extra
from flask_cors import CORS

mail = Blueprint('mail', __name__)
cors = CORS(mail, resources={r"/mail/getdata": {"origins": "*"}})
cors = CORS(mail, resources={r"/mail": {"origins": "*"}})

extra = Extra()
def select(result):
    if not result:
        return '你的问题中不存在所记录的关键字'
    if result[0]['type'] == '1':
        out = '关键字：' + result[0]['keyword'] + '\n'
        out = out + '你是否想问以下问题：' + '\n'
        for que in result[0]['relevant']:
            out = out + que + '\n'
        return out
    if result[0]['type'] == '2':
        out = '界面领域：' + result[0]['keyword'] + '\n'
        out = out + '你是否想查看以下相关的问题：' + '\n'
        for que in result[0]['relevant']:
            out = out + que + '\n'
        return out
    if result[0]['type'] == '3':
        out = ''
        for item in result:
            out = out + '关键词：' + item['keyword'] + '\n'
            out = out + '问题：' + item['question'] + '\n'
            out = out + '问题匹配概率：' + item['question_probability'] + '\n'
            out = out + '问题来源：' + item['question_domain'] + '\n'
            out = out + '解决方案：' + ''.join(item['solution']) + '\n'
            out = out + '\n\n'
        return out
    if result[0]['type'] == '4':
        keywords = []
        questions = []
        for item in result:
            keywords.append(item['keyword'])
            for que in item['relevant']:
                questions.append(que)
        out = '该问题还未记载或者描述不当！你是否想问以下关键词及相关的问题：\n'
        out = out + '关键词：' + '、'.join(keywords) + '\n'
        out = out + '相关问题：' + '、'.join(questions) + '\n'
        return out
    return '你的问题中不存在所记录的关键字'

@mail.route('/')
def index():
    # 获取文本
    text = request.args.get("questuon_mail")
    orig = text
    print(text)
    # 相似词替换
    for key in extra.all_simi.keys():
        if key in text:
            text = text.replace(key, extra.all_simi[key])
            break
    # 关键词搜索
    if text in extra.all_word:
        result = extra.get_code_info(text)
    else:
        result = extra.get_neo_data(text)
    result = select(result)
    print(result)
    result = result.replace('\n', '<br />')
    return render_template('main.html', questuon_mail=orig, result_mail=result)


@mail.route('/getdata', methods=['GET'])
def erp():
    # 获取文本
    text = request.args.get("cw_question")
    orig = text
    print(text)
    # 相似词替换
    for key in extra.all_simi.keys():
        if key in text:
            text = text.replace(key, extra.all_simi[key])
            break
    # 关键词搜索
    if text in extra.all_word:
        result = extra.get_code_info(text)
    else:
        result = extra.get_neo_data(text)
    # print(result)
    result = select(result)
    print(result)
    result = result.replace('\n', '<br />')
    return str(result)

