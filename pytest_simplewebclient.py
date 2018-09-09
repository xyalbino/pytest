#!usr/bin/python3.7
import asyncio
import sys
import re
import os
import time

def filewrite(data):
    for i in range(1,100):
        if os.path.exists("web_response_"+str(i)+".txt")==False:
            f = open(("web_response_" + str(i) + ".txt"), 'w')
            f.write(str(data))
            f.close()
            break

async def tcp_echo_client(port, filename, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', port,
                                                   loop=loop)

    print('Send: %r' % filename)
    writer.write(filename.encode())

    response = await reader.read(4096)
    response=response.decode()
    print(response)

    data = [str(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))), filename, response]
    filewrite(data)

    #print('Close the socket')
    #writer.close()

port = int(sys.argv[1])
filename = str(sys.argv[2])

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(port, filename, loop))
loop.close()