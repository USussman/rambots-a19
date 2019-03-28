import socket,subprocess

hostMACAddress = 'B8:27:EB:AA:76:6B'
port = 3
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            process = subprocess.Popen(data, shell=True, stdout = subprocess.PIPE)
            process.stdout.read()
            client.send(data)
except:	
    print("Closing socket")	
    client.close()
    s.close()
