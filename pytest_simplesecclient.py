#!usr/bin/python3.7
import asyncio
import sys
import re
import os
import time

def filewrite(data):
    for i in range(1,100):
        if os.path.exists("security_response_"+str(i)+".txt")==False:
            f = open(("security_response_" + str(i) + ".txt"), 'w')
            f.write(str(data))
            f.close()
            break

async def tcp_echo_client(port, plaintext, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', port,
                                                   loop=loop)

    print('Send: %r' % plaintext)
    writer.write(("encrypt,"+plaintext).encode())

    data = await reader.read(100)
    data=data.decode()
    print(data)
    cipher=(data.split(','))[1]

    msg=re.sub('cipher','decrypt',(data))
    #msg='abc2'
    writer.write(msg.encode())

    data2=await reader.read(100)
    print(data2.decode())

    data = [str(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))), plaintext, cipher]
    filewrite(data)

    #print('Close the socket')
    #writer.close()

port = int(sys.argv[1])
text = str(sys.argv[2])
text=text.split(',')
plaintext=text[1]

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(port, plaintext, loop))
loop.close()