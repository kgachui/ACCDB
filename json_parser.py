import json
import datetime
import time
from dateutil import parser

# Step 1: Define your class
class workgroup_acd_parser:
    def __init__(self, data: str):
        self.data = data            

    def parse(self, interval_start: datetime="2024-08-05T14:00:00.000-04:00", interval_end: datetime="2024-08-05T14:59:59.000-04:00") -> list[dict]:
        output_data = []
        
        for entry in self.data["results"]: 
            if entry["group"]["mediaType"] == "voice":
                dnis = entry["group"]["dnis"] if "dnis" in entry["group"] else "undefined"
                queue_id = entry["group"]["queueId"] if "queueId" in entry["group"] else "undefined"
                queue_name = "undefined"
                if "metrics" in entry["data"][0]:
                    db_entry = {}
                    for  dataset  in entry["data"][0]["metrics"]:
                        db_entry["QueueID"] = queue_id
                        db_entry["DNIS"] = dnis
                        db_entry["IntervalStartDateTime"] = parser.parse(interval_start).replace(tzinfo=None)
                        db_entry["IntervalEndDateTime"] = parser.parse(interval_end).replace(tzinfo=None)
                        db_entry["QueueID"] = queue_id
                        db_entry["QueueName"] = queue_name
                        metric = dataset["metric"]
                        if metric == "nOffered":
                            db_entry["TotalCallsOffered"] = dataset["stats"]["count"]
                        elif metric == "tAlert":
                            db_entry["TotalAlertingTime"] = dataset["stats"]["sum"]
                        elif metric == "tAnswered":
                            db_entry["TotalCallsAnswered"] = dataset["stats"]["count"]
                        elif metric == "tAbandon":
                            db_entry["TotalCallsAbandoned"] = dataset["stats"]["count"]
                            db_entry["TotalAbandonTime"] = dataset["stats"]["sum"]
                        elif metric == "tAcw":
                            db_entry["TotalAfterCallWorkTime"] = dataset["stats"]["sum"]
                        elif metric == "tWait":
                            db_entry["TotalCallsWaiting"] = dataset["stats"]["count"]
                            db_entry["TotalCallsWaitingTime"] = dataset["stats"]["sum"]
                        elif metric == "oServiceLevel":
                            db_entry["ServiceLevel"] = dataset["stats"]["ratio"]
                            db_entry["ServiceLevelTarget"] = dataset["stats"]["target"]
                        elif metric == "nOverSla":
                            db_entry["TotalCallsOverSLA"] = dataset["stats"]["count"]
                        elif metric == "tHandle":
                            db_entry["TotalHandleTime"] = dataset["stats"]["sum"]
                            db_entry["MaxHandleTime"] = dataset["stats"]["max"]
                        elif metric == "tTalkComplete":
                            db_entry["TotalTalkTime"] = dataset["stats"]["sum"]
                        elif metric == "tHeldComplete":
                            db_entry["TotalHeld"] = dataset["stats"]["count"]
                            db_entry["TotalHoldTime"] = dataset["stats"]["sum"]
                            db_entry["MaxHoldTime"] = dataset["stats"]["max"]
                        elif metric == "nTransferred":
                            db_entry["TotalCallsTransferred"] = dataset["stats"]["count"]
                        elif metric == "nBlindTransferred":
                            db_entry["TotalCallsBlindTransferred"] = dataset["stats"]["count"]
                        elif metric == "nConsultTransferred":
                            db_entry["TotalCallsConsultTransferred"] = dataset["stats"]["count"]
                        elif metric == "tCallbackComplete":
                            db_entry["TotalCallbacks"] = dataset["stats"]["count"]  
                            db_entry["TotalCallbackHandleTime"] = dataset["stats"]["sum"]   
                        elif metric == "tFlowOut":
                            db_entry["TotalFlowOuts"] = dataset["stats"]["count"]
                            db_entry["TotalFlowOutTime"] = dataset["stats"]["sum"]
                        elif metric == "nOutbound":
                            db_entry["TotalQueueOutbound"] = dataset["stats"]["count"]       
                            db_entry["TotalQueueOutboundTime"] = dataset["stats"]["sum"]     

                    output_data.append(db_entry)

        return output_data                   





