import requests
import json
from datetime import datetime


def post_slack(dtLastUpdate, data_changed):

    post_url = "URL" #各ワークスペースでWebhook URLを設定
    requests.post(post_url, data=json.dumps({
        "username": "浜松市オープンデータ更新",
        'text': dtLastUpdate.strftime('%Y-%m-%d %H:%M:%S') + "に、covid19オープンデータ「" + data_changed + "」が更新されました"
    }))

#now = datetime.now()
#data_changed = "検査陽性者の状況"
#post_slack(now, data_changed)