import boto3
from boto3.dynamodb.conditions import Key
import sys
sys.dont_write_bytecode = True
import os
import os.path
import requests
import io
import json
import pytz
from datetime import date, datetime
from post_slack2 import post_slack
import logging

dynamo = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

data_type = ("検査陽性者の状況", "検査陽性患者の属性","陽性患者数","PCR検査実施人数","相談件数")

apiID = ("a3122ca8-a30b-4f64-ab17-a6fe95d46fba", "5ab47071-3651-457c-ae2b-bfb8fdbe1af1", "92f9ebcd-a3f1-4d5d-899b-d69214294a45", "d4827176-d887-412a-9344-f84f161786a2", "1b57f2c0-081e-4664-ba28-9cce56d0b314")

def lambda_handler(event, context):
    try: 

        lastUpdate_table = dynamo.Table("covid19_opendata_lastupdate_log")
        lastUpdate_dynamo =  lastUpdate_table.query(
            KeyConditionExpression = Key('id').eq(0)
        )

        lastUpdate = lastUpdate_dynamo['Items'][0]
       
        for keys, date in lastUpdate.items():
            if keys == "id": continue

            for i in range(len(data_type)):
                if keys == data_type[i]:

                    dtUpdated = getCSVData("https://opendata.pref.shizuoka.jp/api/package_show?id=" + apiID[i])
                    if dtUpdated is None: 
                        lastUpdate[keys] = date
                        logger.info("Data change going on")
                        continue

                    else:                        
                        dt_delta_tmp = (dtUpdated - datetime.strptime(date,"%Y-%m-%d %H:%M:%S")).total_seconds()
                        
                        if dt_delta_tmp < 0 :
                            lastUpdate[keys] = str(dtUpdated)

                        elif dt_delta_tmp > 0:
                            post_slack(dtUpdated, keys)
                            lastUpdate[keys] = str(dtUpdated)

                        else:
                            lastUpdate[keys] = str(dtUpdated)
                            logger.info("No change of opendata")
        
        lastUpdate["id"] = 0
        date_updated = list(lastUpdate.values())
        key_updated = list(lastUpdate.keys())

        lastUpdate_table.put_item(
            Item = {
                key_updated[0] : date_updated[0],
                key_updated[1] : date_updated[1],
                key_updated[2] : date_updated[2],
                key_updated[3] : date_updated[3],
                key_updated[4] : date_updated[4],
                key_updated[5] : date_updated[5]
            }
        )

        return {
            "statusCode": 200,
            "body": "Successfully completed"
        }

    except Exception as e:
        logger.exception(e)
        return {
            "statusCode": 500,
            "body": "error"
        }

def getCSVData(apiAddress):
    try:
        Response = requests.get(apiAddress)
        #リクエストのリターンが正常通信で終わらなかったらFalseを返す
        if Response.status_code != 200: 
            logger.info("Response status error")
            return None

        #取得したjsonにkey errorがあったらFalseを返す
        try:
            apiResponse = Response.json()
            resources = apiResponse["result"]["resources"]
        except KeyError:
            logger.info("Response json KeyError")
            return None

        apiResources = None
        csvAddress = None
        for i in range(len(resources)):
            apiResources = resources[i]
            csvAddress = apiResources["download_url"]
            root, ext = os.path.splitext(csvAddress)
            if ext.lower() == ".csv":
                logger.info(csvAddress)
                break
        #jsonの値がNoneだったらFalseを返す
        if apiResources["updated"][:-3] is None:
            logger.info("json value empty")
            return None
        dateStr = apiResources["updated"][:-3] + apiResources["updated"][-2:]
        tmp_dtUpdated = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
        dtUpdated = datetime.strptime(tmp_dtUpdated.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        logger.info(dtUpdated)

        return dtUpdated

    except Exception as e:
        logger.exception(e)
        return None
