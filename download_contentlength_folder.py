import os
import socket

def downloadContentLength(input=" "):
    domain=input.split('//')[-1].strip('/').split('/')[0]
    subdirectory=input.split('//')[-1].lstrip(domain)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    request = "GET "+subdirectory+" HTTP/1.1\r\nHost:"+domain+"\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())
    filename = input.split('/')[-1]

    data = s.recv(1000)
    header=data[0:data.find(b'\r\n\r\n')]
    temp=header.decode()
    temp=temp.split('Content-Length: ')[-1]
    temp=temp.split('\r\n')[0]
    content_length=int(temp)
    print(content_length)

    
    data=data[data.find(b'\r\n\r\n')+4:]
    name_folder=subdirectory.split('/')[-2]
    dest_folder=domain+"_"+name_folder
    file_path = os.path.join(dest_folder, filename)
    # print(data)
    print("saving to", os.path.abspath(file_path))
    count=len(data)
    
    
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder) # create folder

    with open(file_path, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    with open(file_path, 'ab') as f:
        while count<content_length:
            data = s.recv(1000)
            count=count+len(data)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
    s.close()
