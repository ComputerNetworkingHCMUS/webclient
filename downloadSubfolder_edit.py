import os
import socket
import re
from download import downloadFile

if __name__ == "__main__":
    print("Nhập link: ")
    input=input()
    domain=input.split('//')[-1].strip('/').split('/')[0]
    subdirectory=input.split('//')[-1].lstrip(domain)
    
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

    name_folder=subdirectory.split('/')[-2]
    con=subdirectory.replace(name_folder+"/","")
    
    data=data[data.find(b'\r\n\r\n'):-1]
    count=len(data)
    
    
    while count <=content_length:
        my_dict = re.findall('(?<=<a href=")[^"]*', str(data))
        for x in my_dict:
        
            if x[0] == '#':
                continue
            if x[0] == '/':
                x = input + x
           
            if (x != "?C=N;O=D") & (x != "?C=M;O=A") & (x != "?C=S;O=A") & (x != "?C=D;O=A") &(x!=input+con):
                testDHT(input+x)
        count=count+len(data)
        data = s.recv(1024*20)
    
    s.close()