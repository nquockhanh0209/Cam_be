from EventDriven.Consumer.consumer_base import EventConsumerBase
from Camera.repository.camera_repository import *
import json

from EventDriven.Producer.producer_base import EventProducerBase
class EventCameraHandler(EventConsumerBase, EventProducerBase):
    
    def callback_function(msg: any, args):
        data = json.loads(json.loads(msg)["data"])
        print("**WSS DATA**", data)
        cam_repo = CameraRepository(args)
        cam_repo.create_or_update_cam(CameraDTO(int(data["id"]), data["activate"], data["name"], data["restreamEndpoint"], data["state"]))
        
    async def handle_wss_msg(self, session):
        await self.start_websocket(callback= self.callback_function, callback_arg=session)
        
      
            
    
        
        