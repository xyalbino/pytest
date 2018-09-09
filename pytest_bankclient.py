#!usr/bin/python3.7
import asyncio
import sys
import time
import os

def filewrite(data):
    for i in range(1,100):
        if os.path.exists("bank_response_"+str(i)+".txt")==False:
            f = open(("bank_response_" + str(i) + ".txt"), 'w')
            f.write(str(data))
            f.close()
            break

async def tcp_echo_client(port, message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', port,
                                                   loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    data = [str(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))), message, data.decode()]
    filewrite(data)

    #print('Close the socket')
    #writer.close()

port = int(sys.argv[1])
command = str(sys.argv[2:])

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(port, command, loop))
loop.close()