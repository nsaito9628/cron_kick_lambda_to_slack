# cron_kick_lambda_to_slack
毎分、浜松市のcovid19オープンデータ更新時刻を取得して、データ更新があったらslackに通知するLambda関数
<br>  
**仕様**  
1分毎にオープンデータAIPをたたいて静岡県webサイト上データの最終更新日時を取得し、
あらかじめ取得してDynamoDBに格納してある直前の最終更新日時(%Y-%m-%d %H:%M:%S)と照合して 
データが異なった場合のみslackにメッセージを投稿する
<br>  
**オープンデータの属性(APIリンクあり)**  
　　[検査陽性者の状況](https://opendata.pref.shizuoka.jp/api/package_show?id=a3122ca8-a30b-4f64-ab17-a6fe95d46fba)  
　　[検査陽性患者の属性](https://opendata.pref.shizuoka.jp/api/package_show?id=5ab47071-3651-457c-ae2b-bfb8fdbe1af1)  
　　[陽性患者数](https://opendata.pref.shizuoka.jp/api/package_show?id=92f9ebcd-a3f1-4d5d-899b-d69214294a45)  
　　[PCR検査実施人数](https://opendata.pref.shizuoka.jp/api/package_show?id=d4827176-d887-412a-9344-f84f161786a2)  
　　[相談件数](https://opendata.pref.shizuoka.jp/api/package_show?id=1b57f2c0-081e-4664-ba28-9cce56d0b314)
<br>  
**DynamoDBの設定**  
　　-プライマリパーティションキー：id (数値)  
　　-5つのオープンデータは初期値をダミーで入力(Lambda起動時より未来の日時を%Y-%m-%d %H:%M:%Sで入力)  
　　-lambda初回起動時にオープンデータの最終更新日時を読み込む
<br>  
**Lambdaの設定**  
　　-使用言語：Python　/　ランタイム3.6  
　　-トリガーはCloudWatch Events/EventBridge  
　　-実行間隔は1分毎、設定はrate式

