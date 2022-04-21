from background_task import background
from data.models import Nodes
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import json

@background(schedule=60)
def publish_status():
    async_send("status", get_status())
    print('TASK STARTA......')

def async_send(channel_name, jsonData):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(channel_name, {"type": "send_data"})

def get_status():
        Status = {} 
        try:
            Status['Data'] = json.loads(Nodes.objects.all().to_dataframe().to_json(orient="table"))
            Status['Data_Type'] = "Status_Data"
            Status['Node_ID'] = 0
        except Exception as e:
            print('{!r}; Get status data failed - '.format(e)) 
        return Status