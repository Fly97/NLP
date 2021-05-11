from flask import *
from movies.classmovie import TextClass
from movies.key_extra import Extra


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


textclass = TextClass()
extra = Extra()
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/info', methods=['GET'])
def erp():
    # 获取文本
    text = request.args.get("cw_question")
    print(text)
    # 抽取关键字
    keyword = extra.get_entity(text)
    if not keyword:
        return render_template('main.html', result='还未收录此数据！！')
    print(keyword)
    # 问题分类
    type = textclass.predict(text)
    print(type)
    result = extra.get_neo_data(keyword, type[0], type[1])
    print(result)
    return render_template('main.html', type=type, questuon=text, keyword=keyword, result=result)



@app.route('/getdata', methods=['GET', 'POST'])  ##从接口得到数据
def getdata():
    text = request.args.get('question')
    print(text)
    # 抽取关键字
    keyword = extra.get_entity(text)
    print(keyword)
    # 问题分类
    type = textclass.predict(text)
    print(type)
    result = extra.get_neo_data(keyword, type[0], type[1])
    print(result)
    return str(result)

@app.errorhandler(500)
def error(e):
    return '错误，请检查代码！'


if __name__ == '__main__':
    print(app.url_map)
    app.run(port=7777, debug=False, host='0.0.0.0')
    # app.run(port=7777, debug=False)



