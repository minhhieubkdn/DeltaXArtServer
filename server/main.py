import asyncio
import os
import websockets
import json
from PyQt5.QtCore import QObject, pyqtSignal

class WebSocketServer(QObject):
    received_message = pyqtSignal(str)
    def __init__(self, host='192.168.101.31', port=5000):
        super().__init__()
        self.host = host
        self.port = port

    async def handle_connection(self, websocket, path):
        async for message in websocket:
            # self.received_message.emit(message)
            # message = ""
            # print(message)
            if message.startswith("PUT"):                  #PUT|admin|spiderman|{spiderman_json_content} => Ok
                message_parts = message.split('|')
                username = message_parts[1]
                filename = message_parts[2]
                fileContent = message[message.rindex("|")+1:]

                json_data = json.loads(fileContent)
                with open('data/users/'+ username + '/' + filename +'.json', 'w') as f:
                    json.dump(json_data, f)

                await websocket.send("Ok")
            elif message.startswith("GET"):
                message_parts = message.split("|")
                username = message_parts[1]
                filename = message_parts[2]

                if (filename == "FILES"):                  #GET|admin|FILES => FILES|spiderman.json|spiderman2.json|DeltaXS.json
                    path = 'data/users/' + username
                    files = os.listdir(path)

                    return_mess = filename + "|"
                    for file in files:
                        if file.find(".json") > 0:
                            return_mess += file + "|"
                    
                    await websocket.send(return_mess)

                else:                                      #GET|admin|spiderman.json => JSON|spiderman|{spiderman_json_content}
                    path = "data/users/"+username+"/"+filename
                    with open(path, 'r') as f:
                        json_data = json.load(f)
                    await websocket.send("JSON|"+filename[:-5] +"|"+ json.dumps(json_data))


    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port):
            print(f"WebSocket server started at ws://{self.host}:{self.port}")
            await asyncio.Future()  # keep the server running indefinitely



import socket

def get_local_ip():
    try:
        # Get the local host name
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    host = get_local_ip()
    server = WebSocketServer(host=host)
    asyncio.run(server.start())

