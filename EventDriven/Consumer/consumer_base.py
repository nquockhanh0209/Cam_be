import asyncio
import websockets
import json
from typing import Callable

from EventDriven.Event.EventBase import EventBase
class EventConsumerBase(EventBase):
   
    async def listen_wss(self) -> any:
        
    
        print
        msg = await self.ws.recv()
        return msg
    