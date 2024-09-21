import os
from dotenv import load_dotenv, dotenv_values
import db_writer
import http_requests
import json_parser
import sys
 
def main(interval_start: str="2024-08-05T13:00:00-0500", interval_end: str="2024-08-05T13:59:59-0500"):
    # loading variables from .env file
    load_dotenv() 
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

    # set up db connection
    db=db_writer.database(driver=db_driver,
                          server=db_server,
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
    interval_start = "2024-09-05T13:00:00-0500"#sys.argv[1]
    interval_end = "2024-09-05T13:59:59-0500"#sys.argv[2]
    main(interval_start, interval_end)