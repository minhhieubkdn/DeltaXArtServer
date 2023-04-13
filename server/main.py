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


if __name__ == '__main__':
    server = WebSocketServer()
    asyncio.run(server.start())

# import asyncio
# import websockets
# import json

# async def server(websocket, path):
#     data = await websocket.recv()
#     # print(f"Nhận được chuỗi dữ liệu từ ứng dụng QT Quick: {data}")
#     json_data = json.loads(data)

#     # Lưu đối tượng Python thành file JSON bằng json.dump()
#     with open('data.json', 'w') as f:
#         json.dump(json_data, f)

# start_server = websockets.serve(server, "localhost", 5000)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()