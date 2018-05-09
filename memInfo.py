import psutil
import datetime
from utils import db
from Entiers import SystemInfo
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
def get_now():
    now = datetime.datetime.now()
    return now

def getCpuRate():
    cpu = psutil.cpu_percent(1)
    return cpu

def getMemInfo():

    mem_info = psutil.virtual_memory()
    return mem_info
def getMemTotal():
        
    mem_total = round(getMemInfo().total / 1024 / 1024 / 1024)
        
    return  mem_total
    
def getMemUsed():
        
    mem_used = round(getMemInfo().used / 1024 / 1024 / 1024)
        
    return mem_used


def getMemLoad():
        
    mem_load = round(getMemUsed() / getMemTotal() * 100)
        
    return mem_load




def insert_success_mem_2db():
    db_conn = db.get_db_connection()



    mem_load = [
            {
                "measurement": "mem_load_short",
                "tags":
                    {
                        "host": "server01"
                    },
                "fields":
                    {
                        "value": getMemLoad(),
                        "success": 1,
                    }
            }
        ]
    mem_used = [
        {
            "measurement": "mem_used_hort",
            "tags":
                {
                    "host": "server01"
                },
            "fields":
                {
                    "value": getMemUsed(),
                    "success": 1,
                }
        }
    ]
    mem_total = [
        {
            "measurement": "mem_total_short",
            "tags":
                {
                    "host": "server01"
                },
            "fields":
                {
                    "value": getMemTotal(),
                    "success": 1,
                }
        }
    ]
    cpu_point = [
        {
            "measurement": "cpu_load_short",
            "tags":
                {
                    "host": "server01"
                },
            "fields":
                {
                    "value": getCpuRate(),
                    "success": 1,
                }
        }
    ]
    try:
        db_conn.write_points(mem_load)
        db_conn.write_points(mem_used)
        db_conn.write_points(mem_total)
        db_conn.write_points(cpu_point)
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
    insert_success_mem_2db()

if __name__ == '__main__':
    while 1:
        main()