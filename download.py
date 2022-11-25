import os
import socket

def downloadFile(input=" "):
    # print("Nhập url: ")
    # input=input()
    domain=input.split('//')[-1].strip('/').split('/')[0]
    print(domain)

    subdirectory=input.split('//')[-1].lstrip(domain)
    print(subdirectory)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    request = "GET "+subdirectory+" HTTP/1.1\r\nHost:"+domain+"\r\n\r\n"
    s.sendall(request.encode())


    data = s.recv(1000)
    header=data[0:data.find(b'\r\n\r\n')]
    temp=header.decode()
    temp=temp.split('Content-Length: ')[-1]
    temp=temp.split('\r\n')[0]
    content_length=int(temp)
    print(content_length)

    filename = input.split('/')[-1]
    data=data[data.find(b'\r\n\r\n'):-1]
    name_folder=subdirectory.split('/')[-2]
    dest_folder=domain+"_"+name_folder
    file_path = os.path.join(dest_folder, filename)
    
    print("saving to", os.path.abspath(file_path))
    count=len(data)
    
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder) # create folder
            
    while count <=content_length:
        with open(file_path, 'ab') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        count=count+len(data)
        data = s.recv(1000)
    s.close()
