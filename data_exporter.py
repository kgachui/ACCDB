import os
from dotenv import load_dotenv, dotenv_values
import db_writer
import http_requests
import json_parser
import datetime

def get_ts(time_delta: int) -> datetime:
    # Get current timestamp
    current_timestamp = datetime.datetime.now() 

    # Create a timedelta object for 1 minute
    delta = datetime.timedelta(minutes=time_delta)

    # Return current timestamp minus time delta
    return current_timestamp - delta

 
def main():
    # loading variables from .env file
    load_dotenv() 
    data_pull_interval_minutes = os.getenv("PULL_INTERVAL_MINUTES")
    base_url = os.getenv("BASE_URL")
    token_req_url = os.getenv("TOKEN_URL")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    db_driver = os.getenv("DB_DRIVER")
    db_server = os.getenv("DB_SERVER")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    database = os.getenv("DATABASE")
    db_table = os.getenv("DB_TABLE")
    rds_proxy_host = os.getenv("RDS_PROXY_HOST")

    interval_start = get_ts(int(data_pull_interval_minutes))
    interval_end = get_ts(1) # timestamp from 1 minute ago

    # set up db connection
    db=db_writer.database(rds_proxy_host=rds_proxy_host,
                          user_id=db_user,
                          password=db_pass,
                          database=database,
                          db_table=db_table)
    connection = db.cnxn
    cursor = connection.cursor()

    # set up request API object
    api = http_requests.HttpRequest(base_url=base_url, client_id=client_id, client_secret=client_secret, token_req_url=token_req_url)
    acd_data = api.get_workgroup_acd_data(start_time=interval_start, end_time=interval_end)
    acd_db_data = json_parser.workgroup_acd_parser(acd_data).parse(interval_start=interval_start, interval_end=interval_end)
    for row in acd_db_data:
        queue_name = api.get_queue(row["QueueID"])
        row["QueueName"]= queue_name

    db.insert_data(acd_db_data)
    

if __name__ == "__main__":    
    main()