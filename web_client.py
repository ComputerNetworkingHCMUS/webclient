import os
import socket
import re
import time
import threading 
from download_contentlength_folder import downloadContentLength
from download_chunked_folder import download_chunked

def threaded_function(input):
        try:
            # tách domain và subdirectory
            domain=input.split('//')[-1].strip('/').split('/')[0]
            subdirectory=input.split('//')[-1].lstrip(domain)
            
            # tạo socket và kết nối, nhận dữ liệu từ webserver
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((domain, 80))
            request = "GET "+subdirectory+" HTTP/1.1\r\nHost:"+domain+"\r\n\r\n"
            s.sendall(request.encode())
            
            #filename = input.split('/')[-1]
            filename2=subdirectory.split('/')[-1]
            
            
            data = s.recv(1000)
            header=data[0:data.find(b'\r\n\r\n')]
            temp=header.decode()
            
            if isValidDomain(str(filename2)) == False :
                if temp.find('Content-Length')!=-1: # tìm thấy content-length
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
                                downloadContentLength(input+x)
                        count=count+len(data)
                        data = s.recv(1024*20)
                        
                    print('Saving completed')
                else:
                    BUFF_SIZE = 1024*4
                    timeout = 2
                    s.setblocking(0)
                    begin = time.time()
                    while 1:
                            # if you got some data, then break after wait sec
                        if data and time.time()-begin > timeout:
                            break
                            # if you got no data at all, wait a little longer
                        elif time.time()-begin > timeout*2:
                            break
                        try:
                            data = s.recv(BUFF_SIZE)
                            if data:
                                my_dict = re.findall('(?<=<a href=")[^"]*', str(data))
                            for x in my_dict:
                                
                                if x[0] == '#':
                                    continue
                                if x[0] == '/':
                                    x = input + x
                            
                                if (x != "?C=N;O=D") & (x != "?C=M;O=A") & (x != "?C=S;O=A") & (x != "?C=D;O=A") &(x!=input+con):
                                    download_chunked(input+x)
                                begin = time.time()
                            else:
                                time.sleep(0.1)
                        except:
                            pass
                print('Saving completed')
                    
            else:
                if temp.find('Content-Length')!=-1:
                    temp=temp.split('Content-Length: ')[-1]
                    temp=temp.split('\r\n')[0]
                    content_length=int(temp)

                    filename = input.split('/')[-1]
                    if filename=="":
                        filename=domain+"_"+"index.html"
                    else :
                        filename=domain+"_"+filename
                    data=data[data.find(b'\r\n\r\n')+4:]
                
                    print("saving to", os.path.abspath(filename))
                    count=len(data)
                    with open(os.path.abspath(filename), 'wb') as f:
                            f.write(data)
                            f.flush()
                    with open(os.path.abspath(filename), 'ab') as f:
                        while count<content_length:
                            data = s.recv(1000)
                            count=count+len(data)
                            f.write(data)
                            f.flush()
                else:
                    filename = input.split('/')[-1]
                    if filename=="":
                        filename=domain+"_"+"index.html"
                    else :
                        filename=domain+"_"+filename
                    print("saving to", os.path.abspath(filename))
                    
                    data = data[data.find(b'\r\n\r\n')+4:]
                    with open(os.path.abspath(filename), 'wb') as f:
                        f.write(data)
                        f.flush()

                    BUFF_SIZE = 1024*4
                    timeout = 2
                    s.setblocking(0)
                    begin = time.time()
                    with open(os.path.abspath(filename), 'ab') as f:
                        while 1:
                            # if you got some data, then break after wait sec
                            if data and time.time()-begin > timeout:
                                break
                            # if you got no data at all, wait a little longer
                            elif time.time()-begin > timeout*2:
                                break
                            try:
                                data = s.recv(BUFF_SIZE)
                                if data:
                                    f.write(data)
                                    f.flush()
                                    begin = time.time()
                                else:
                                    time.sleep(0.1)
                            except:
                                pass

                    print('Saving completed')
            time.sleep(0.1)
        except:
            time.sleep(0.1)
            print('Ngắt kết nối')
            s.close()


def isValidDomain(str):
    regex = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if((re.search(p, str)) or (re.findall('.ppt',str)) or (re.findall(".docx",str))):
        return True
    else:
        return False


if __name__ == "__main__":
    print('Nhập link(s): ')
    Input=input()
    count=1
    if(re.findall('http',Input)):
        count=count+1
    tempin=Input.split(" ")
    
    if len(tempin) > 1:
        for i in range(len(tempin)):
            thread = threading.Thread(target=threaded_function, args=(tempin[i],))  
            thread.start()
            thread.join()
    else: 
        thread = threading.Thread(target=threaded_function, args=(Input,))
        thread.start()
        thread.join()
    
    time.sleep(0.1)
    
    print("Bạn có muốn tiếp tục không? 1: yes, 0: no")
    choose=int(input())
    while choose == 1:
        print('Nhập link(s): ')
        Input=input()
        count=1
        if(re.findall('http',Input)):
            count=count+1
        tempin=Input.split(" ")
        
        if len(tempin) > 1:
            for i in range(len(tempin)):
                thread = threading.Thread(target=threaded_function, args=(tempin[i],))  
                thread.start()
                thread.join()
        else: 
            thread = threading.Thread(target=threaded_function, args=(Input,))
            thread.start()
            thread.join()
        
        time.sleep(0.1)
        
        print("Bạn có muốn tiếp tục không? 1: yes, 0: no")
        choose=int(input())
