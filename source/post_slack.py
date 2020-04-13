import requests
import json
from datetime import datetime


def post_slack(dtLastUpdate, data_changed):

    item_chenged = ""

    for i in range(len(data_changed)):
        item_chenged = item_chenged + "\n　・" + data_changed[i]


    post_url = 'Webhook URL'
    requests.post(post_url, data=json.dumps({
        "username": "浜松市オープンデータ更新",
        'text': dtLastUpdate.strftime('%Y-%m-%d %H:%M:%S') + "にcovid19オープンデータ\n" + item_chenged + "\n\nが更新されました"
    }))

#now = datetime.now()
#data_changed = ["検査陽性者の状況", "検査陽性患者の属性","陽性患者数","PCR検査実施人数","相談件数"]
#post_slack(now, data_changed)