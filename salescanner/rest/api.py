import flask
from flask import request, jsonify
from flask import json

from salescanner.services.ad_item_service import AdItemService


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg': 'Hello to SaleScanner!'})

@app.route('/api/ads/list', methods=['PUT'])
def get_ads():
    query = request.json.get('query', '')
    order_by = request.args.get('order_by')

    page = request.args.get('page')
    if page is not None:
        page = int(page)
    size = request.args.get('page_size')
    if size is not None:
        size = int(size)

    ads = AdItemService.list_ads(query, order_by, page, size)
    return jsonify(ads)

@app.route('/api/ads/count', methods=['GET'])
def count_ads():
    count = AdItemService.count_ads()
    return jsonify({'count': count})


if __name__ == '__main__':
    app.run()
