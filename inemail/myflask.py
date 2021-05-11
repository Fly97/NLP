from flask import *
from inemail.myanswer import Extra
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

extra = Extra()
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/info', methods=['GET'])
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
    print(result)
    return render_template('main.html', questuon=orig, result=result)

@app.errorhandler(500)
def error(e):
    return '错误，请检查代码！'


if __name__ == '__main__':
    print(app.url_map)
    app.run(port=7777, debug=False, host='0.0.0.0')
    # app.run(port=6969, debug=False)


