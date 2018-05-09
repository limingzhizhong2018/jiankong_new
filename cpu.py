## - * - coding: utf-8 - * -
import psutil
import datetime
import time
from utils import db
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

#获取逻辑cpu
logical_cpu= str(psutil.cpu_count(logical=True))
#cpu使用率
def get_rate():
    time.sleep(2)
    cpu = str(psutil.cpu_percent(1))
    return cpu

def insert_success_point_2db():
    db_conn = db.get_db_connection()
    success_point = [
                     {
                        "measurement": "cpu_load_short",
                        "tags":
                             {
                                 "host": "server01"
                             },
                        "fields":
                             {
                                 "value": get_rate(),
                                 "success": 1,
                             }
                     }
                     ]


    try:
        db_conn.write_points(success_point)
    except InfluxDBClientError as e:
        print("influxdb db client error: {0}".format(e))
    except InfluxDBServerError as e:
        print("influxdb db server error: {0}".format(e))
    except Exception as e:
        print("influxdb error: {0}".format(e))
    finally:
        if db_conn is not None:
            db_conn.close()
def main():
    insert_success_point_2db()

if __name__ == '__main__':
    while 1:
     main()
     result = db.get_db_connection().query('select value from cpu_load_short;')
     print("Result: {0}".format(result))

