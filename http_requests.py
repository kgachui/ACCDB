import requests
import base64
import json
import datetime

class HttpRequest:
    def __init__(self, base_url: str, 
                 client_id: str, 
                 client_secret: str,
                 token_req_url: str):
        self.base_url = base_url
        auth_headers = {
            "content-type": "application/x-www-form-urlencoded"
        }

        auth_params = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        r = requests.post(url=token_req_url, headers=auth_headers, params=auth_params)
        json_response = json.loads(r.content)
        self.__token = json_response["access_token"]
        self.__base_url = base_url

        self.__req_headers = {
            "Content-Type": "application/json",
            "Authorization": "bearer " + self.__token
        }


    def __get(self, endpoint, params=None):
        url = self.base_url + endpoint
        response = requests.get(url, data=params, headers=self.__req_headers)
        return response.json()

    def __post(self, endpoint, headers=None, params=None):
        url = self.base_url + endpoint
        response = requests.post(url, json=params, headers=headers)
        return response.json()
    
    def get_queue(self,queue_id):
        get_response = self.__get(f"/api/v2/routing/queues/divisionviews?id={queue_id}")
        return get_response["entities"][0]["name"] if "entities" in get_response else queue_id
    
    def get_workgroup_acd_data(self, start_time: str="2024-08-05T13:00:00-0500", end_time: str="2024-08-05T13:59:59-0500"):
        post_data = {
            "groupBy": [
                "dnis",
                "queueId",
                "mediaType"
            ],
            "timeZone": "America/New_York",
            "metrics": [
                "nOffered",
                "tAlert",
                "tAnswered",
                "tAbandon",
                "tAcw",
                "tAcd",
                "tWait",
                "oServiceLevel",
                "oServiceTarget",
                "nOverSla",
                "tHandle",
                "tTalkComplete",
                "tTalk",
                "tHeldComplete",
                "tHeld",
                "nTransferred",
                "nBlindTransferred",
                "nConsultTransferred",
                "nConnected",
                "tActiveCallbackComplete",
                "tActiveCallback",
                "tFlowOut",
                "tDialing",
                "nOutbound",
                "nOutboundAbandoned",
                "nOutboundAttempted",
                "nOutboundConnected"
            ],
            "interval": f"{start_time}/{end_time}"
        }
        return self.__post(endpoint="/api/v2/analytics/conversations/aggregates/query", headers=self.__req_headers, params=post_data)

# Example usage:
if __name__ == "__main__":
    api = HttpRequest()
    get_response = api.get("/api/v2/routing/queues/divisionviews")
    queue_names: dict[str, str] = {}
    for entry in get_response['entities']:
        queue_names[entry["id"]] = entry["name"]

    pass
    post_data = {
        "groupBy": [
            "dnis",
            "queueId",
            "mediaType"
        ],
        "timeZone": "America/New_York",
        "metrics": [
            "nOffered",
            "tAlert",
            "tAnswered",
            "tAbandon",
            "tAcw",
            "tAcd",
            "tWait",
            "oServiceLevel",
            "oServiceTarget",
            "nOverSla",
            "tHandle",
            "tTalkComplete",
            "tTalk",
            "tHeldComplete",
            "tHeld",
            "nTransferred",
            "nBlindTransferred",
            "nConsultTransferred",
            "nConnected",
            "tActiveCallbackComplete",
            "tActiveCallback",
            "tFlowOut",
            "tDialing",
            "nOutbound",
            "nOutboundAbandoned",
            "nOutboundAttempted",
            "nOutboundConnected"
        ],
        "interval": "2024-08-05T13:00:00-0500/2024-08-05T13:59:59-0500"
    }
    post_response = api.post(endpoint="/api/v2/analytics/conversations/aggregates/query", headers=api.req_headers, params=post_data)
    print("POST response:", post_response)