#!usr/bin/python3.7
import asyncio
import sys
import os
import time
def carser(a):
    for i in range(1, 26):
        ans = []
        for j in a:
                j = chr(ord('A') + ((ord(j) - ord('A') + i) % 26))
                ans.append(j)
        ans=(''.join(ans))
        return(ans)

def filewrite(data):
    for i in range(1,100):
        if os.path.exists("security_message_"+str(i)+".txt")==False:
            f = open(("security_message_" + str(i) + ".txt"), 'w')
            f.write(str(data))
            f.close()
            break

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    if message!="__EXIT__":
        print("Send: %r" % message)
        message = message.split(',')
        plaintext = message[1]
        cipher=carser(plaintext)
        writer.write(('cipher,'+cipher).encode())
        await writer.drain()
    #print("Close the client socket")
        #writer.close()
        data2= await reader.read(100)
        message2=data2.decode()
        writer.write(('plain,'+message[1]).encode())
        await writer.drain()
        writer.close()
        data = [str(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))), plaintext,cipher]
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