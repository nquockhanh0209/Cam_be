
import websockets
from typing import Callable
import json
class EventBase():
    wss_domain: str= "ws://192.168.1.212:48080/"
    wss_end_point: str
    wss_url: str
    ws: websockets.WebSocketClientProtocol
    def __init__(self,_wss_end_point):
        self.wss_end_point = _wss_end_point
        
        self.wss_url = self.wss_domain + self.wss_end_point
    async def start_websocket(self, callback: Callable[...,None], callback_arg: [...]):
        print("self.wss_url", self.wss_url)
        async with websockets.connect(self.wss_url) as ws: 
            while True:
                msg = await ws.recv()
                callback(msg, callback_arg)
                await ws.send(json.dumps(json.loads(msg)))
                    
      
            
    # async def listen_wss(self) -> any:
    #     while True:
    #         msg = await self.ws.recv()
    #         return msg
        
    # async def send_msg(self, msg: str) :
    #     await self.ws.send(msg)
        
    