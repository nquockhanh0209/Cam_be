import asyncio
import websockets
import json
from typing import Callable

from EventDriven.Event.EventBase import EventBase
class EventProducerBase(EventBase):
    
        
    async def send_msg(self, msg: str) :
        await self.ws.send(msg)

    