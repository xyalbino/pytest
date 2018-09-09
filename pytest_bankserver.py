#!usr/bin/python3.7
import asyncio
import os
import sys
import time
import re

def filewrite(data):
    for i in range(1,100):
        if os.path.exists("bank_message_"+str(i)+".txt")==False:
            f = open(("bank_message_" + str(i) + ".txt"), 'w')
            f.write(str(data))
            f.close()
            break

async def handle_echo(reader, writer):
    global money,i
    cmd=""
    data = await reader.read(100)
    message = data.decode()
    message=re.sub(r'[\]\[\'\,\]]',' ',message)
    message=message.split()
    #print(message[1])
    addr = writer.get_extra_info('peername')
    #print("Received %r from %r" % (message, addr))
    if message=="__EXIT__":
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        exit()

    if len(message)==2:
        cmd=message[0]
        num=int(message[1])
        if cmd=="deposit":
            money+=num
            writer.write('OK'.encode())
        elif cmd=="withdraw":
            if num<=money:
                money-=num
            else:
                num=money
                money=0
            writer.write(str(num).encode())
    elif len(message)==1:
        cmd=message[0]
        if cmd=="balance":
            writer.write(str(money).encode())

    data = [str(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))), cmd, str(money)]
    filewrite(data)

    await writer.drain()
    writer.close

port=int(sys.argv[1])
global money
money=0
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', port, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
#server.close()
#loop.run_until_complete(server.wait_closed())
#loop.close()