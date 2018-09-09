#!usr/bin/python3.7
import asyncio
import sys
import os
import time
from pathlib import Path

def success(filename):
    f=open(filename,'r')
    html=f.read()
    date=time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
    length=len(html)
    report="HTTP/1.1 200 OK\r\nDate: "+str(date)+" GMT\r\nContent-Type: text/html;charset=ISO-8859-1\r\nContent-Length: "+str(length)+ "\r\n"
    report=report+html
    return report


def filewrite(data):
    for i in range(1,100):
        if os.path.exists("web_message_"+str(i)+".txt")==False:
            f = open(("web_message_" + str(i) + ".txt"), 'w')
            f.write(str(data))
            f.close()
            break

async def handle_echo(reader, writer):
    data = await reader.read(100)
    filename = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (filename, addr))
    if filename!="__EXIT__":
        print("Send: %r" % filename)
        my_file = Path("./path/to/server/root/"+filename)
        if (my_file.exists()):
            response=success(my_file)
            code="200 OK"
        else:
            response="404 not found"
            code="404 Not Found"
        writer.write(response.encode())
        await writer.drain()
    #print("Close the client socket")
        #writer.close()
        data = [str(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))), filename,code]
        filewrite(data)
    else:
        server.close()


port=int(sys.argv[1])
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