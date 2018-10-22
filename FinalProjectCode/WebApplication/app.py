"""
food_obesity_points: /food_obesity
food: /food
obesity: /obesity
locale_list: /locale
locale_detail: /locale/<string:locale_code>
"""



from flask import Flask, jsonify, abort, make_response, request, url_for, send_from_directory
from flask_cors import CORS
# from WebApplication.dataFetcher import DataFetcher
from dataFetcher import DataFetcher

app = Flask(__name__)
CORS(app)

data_fetcher = DataFetcher()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No Available Data'}), 404)


@app.route('/food_obesity', methods=['GET'])
def get_food_obesity_data():
    try:
        child, adult = data_fetcher.get_abr_obesity()
    except:
        abort(404)
    if len(child) == 0 or len(adult) == 0:
        abort(404)
    return jsonify({'child': child, 'adult': adult}), 200


@app.route('/food', methods=['GET'])
def get_food():
    try:
        abr_data = data_fetcher.get_abr()
    except:
        abort(404)
    if len(abr_data) == 0:
        abort(404)
    return jsonify({'food_count': abr_data}), 200


@app.route('/obesity', methods=['GET'])
def get_obesity():
    try:
        obesity = data_fetcher.get_obesity()
    except:
        abort(404)
    if len(obesity) == 0:
        abort(404)
    return jsonify({'obesity_count':obesity}), 200


@app.route('/locale', methods=['GET'])
def get_locale_list():
    try:
        data_list = data_fetcher.get_locale_list()
    except:
        abort(404)
    if len(data_list) == 0:
        abort(404)
    return jsonify({'locale_list': data_list}), 200


@app.route('/locale/<string:locale_code>/<string:ob>', methods=['GET'])
def get_city(locale_code, ob):
    if ob == 'ob':
        if_obesity = True
    else:
        if_obesity = False
    try:
        data_list = data_fetcher.get_locale_summary(locale_code, if_obesity)
    except:
        abort(404)
    if len(data_list) == 0:
        abort(404)
    return jsonify({locale_code: data_list[0]}), 200


@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('Web', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

"""
curl -i http://localhost:5000/food_obesity
curl -i http://localhost:5000/locale
curl -i http://localhost:5000/locale/20002
curl -i http://localhost:5000/food
curl -i http://localhost:5000/obesity
"""

"""
curl -i http://18.216.214.90:5000/food_obesity
curl -i http://18.216.214.90:5000/locale
curl -i http://18.216.214.90:5000/locale/20002
curl -i http://18.216.214.90:5000/food
curl -i http://18.216.214.90:5000/obesity
"""