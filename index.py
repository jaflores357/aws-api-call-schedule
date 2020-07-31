import json
import pymysql
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

db_host  = os.environ['dbHost']
db_name  = os.environ['dbName']
db_user  = os.environ['dbUser']
db_pass  = os.environ['dbPass']
bulk_url = os.environ['bulkUrl']

try:
    conn = pymysql.connect(db_host, user=db_user, passwd=db_pass, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)

def lambda_handler(event, context):
    try:
        with conn.cursor() as cur:
            
            sql = "select Carrier, provider, user, pass, ServiceType, Request from tab_bulk_schedule"
            cur.execute(sql)
            rows = cur.fetchall()
            headers = {'Content-Type':'application/xml'}

            for row in rows:
                trans_id = "{0}-{1}-{2}-{3}".format(datetime.now().strftime('%Y%m%d%H%M'), row[0], row[1], row[4]) 
                print("{0} {1} {2} {3} {4}".format(row[0], row[1], row[2], row[3], row[4]))
                r = requests.post(bulk_url, data=row[5].replace("__TRANSACTIONID__", trans_id), headers=headers, auth=HTTPBasicAuth(row[2], row[3]))
                print("Status: {0} :: Response: {1}".format(r.status_code, r.content))

    except pymysql.Error as e:
        print("Database error %d: %s" % (e.args[0], e.args[1]))
                
