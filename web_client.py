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
            request = "GET /" + subdirectory + " HTTP/1.1\r\nHOST:" + \
                domain + "\r\nConnection: keep-alive\r\n\r\n"
            s.sendall(request.encode())
            
            
            filename2=subdirectory.split('/')[-1]
            tempsub=subdirectory.split('/')
            
            data = s.recv(1000)
            header=data[0:data.find(b'\r\n\r\n')]
            temp=header.decode()
            
            
            if isValidDomain(str(filename2)) == False and (len(tempsub) > 2):
                    if temp.find('Content-Length')!=-1: # tìm thấy content-length
                        temp=temp.split('Content-Length: ')[-1]
                        temp=temp.split('\r\n')[0]
                        content_length=int(temp)

                        name_folder=subdirectory.split('/')[-2]
                        con=subdirectory.replace(name_folder+"/","")
                        
                        data=data[data.find(b'\r\n\r\n')+4:]
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
                        file_name = ''
                        if (subdirectory == ""):
                            file_name = domain + "_index.html"
                        else:
                            reversed_file_dir = subdirectory[::-1]
                            posfilename = reversed_file_dir.find("/")
                            if (posfilename == -1):
                                file_name = domain + "_" + subdirectory
                            else:
                                temp_file_name = reversed_file_dir[0:posfilename]
                                temp_file_name = temp_file_name[::-1]
                                file_name = file_name = domain + "_" + temp_file_name
                        header = ""
                        while not header.endswith('\r\n\r\n'):
                            header += s.recv(1).decode()
                        header = header[0:header.find('\r\n\r\n')]
                        print(header)
                        print('-------------------------------------------------------------------------------------------------')

                        BUFFER_SIZE = 1024 * 2
                        with open(file_name, 'wb') as f:
                            while True:
                                try:
                                    # Get chunk size
                                    chunkSize_line = ""
                                    while not chunkSize_line.endswith('\n'):
                                        chunkSize_line += s.recv(1).decode()
                                    chunkSize_line = chunkSize_line[0:chunkSize_line.find('\r\n')]
                                    chunk_size = int(chunkSize_line, 16)
                                    print('Chunk_size = ', chunk_size)

                                    # download and save chunked data
                                    if chunk_size > 0:

                                        n = chunk_size
                                        while True:
                                            if n >= BUFFER_SIZE:
                                                data = s.recv(BUFFER_SIZE)
                                            else:
                                                data = s.recv(n+2)
                                            #print(data)
                                            my_dict = re.findall('(?<=<a href=")[^"]*', str(data))
                                            for x in my_dict:
                                            
                                                if x[0] == '#':
                                                    continue
                                                if x[0] == '/':
                                                    x = input + x
                                                
                                                if (x != "?C=N;O=D") & (x != "?C=M;O=A") & (x != "?C=S;O=A") & (x != "?C=D;O=A") &(x!=input+con):
                                                    download_chunked(input+x)

                                            n -= len(data)
                                            if n + 2 == 0:
                                                break
                                        print('Saving...')
                                except:
                                    pass
                                if chunk_size <= 0:
                                    break
                        print('Saving completed')
                    
            else:
                # truong hop content-length
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
                            
                    print('Saving completed')
                    
                else:
                    # trường hợp chunked
                    if (input.find("http://") != -1):
                        input = input.replace("http://", '')
                    poshost = Input.find("/")
                    if (poshost == -1):
                        domain = input.split('//')[-1].strip('/').split('/')[0]
                        subdirectory = ""
                    else:
                        domain = input.split('//')[-1].strip('/').split('/')[0]
                        subdirectory = input.split('//')[-1].lstrip(domain)

                    file_name = ''
                    if (subdirectory == ""):
                        file_name = domain + "_index.html"
                    else:
                        reversed_file_dir = subdirectory[::-1]
                        posfilename = reversed_file_dir.find("/")
                        if (posfilename == -1):
                            file_name = domain + "_" + subdirectory
                        else:
                            temp_file_name = reversed_file_dir[0:posfilename]
                            temp_file_name = temp_file_name[::-1]
                            file_name = file_name = domain + "_" + temp_file_name
                    header = ""
                    while not header.endswith('\r\n\r\n'):
                        header += s.recv(1).decode()
                    header = header[0:header.find('\r\n\r\n')]
                    print(header)
                    print('-------------------------------------------------------------------------------------------------')

                    BUFFER_SIZE = 1024 * 2
                    with open(file_name, 'wb') as f:
                        while True:
                            try:
                                # Get chunk size
                                chunkSize_line = ""
                                while not chunkSize_line.endswith('\n'):
                                    chunkSize_line += s.recv(1).decode()
                                chunkSize_line = chunkSize_line[0:chunkSize_line.find('\r\n')]
                                chunk_size = int(chunkSize_line, 16)
                                print('Chunk_size = ', chunk_size)

                                # download and save chunked data
                                if chunk_size > 0:

                                    n = chunk_size
                                    while True:
                                        if n >= BUFFER_SIZE:
                                            data = s.recv(BUFFER_SIZE)
                                        else:
                                            data = s.recv(n+2)
                                        #print(data)
                                        f.write(data)
                                        f.flush()

                                        n -= len(data)
                                        if n + 2 == 0:
                                            break
                                    print('Saving...')
                            except:
                                pass
                            if chunk_size <= 0:
                                break
                    print('Saving completed')
                    s.close()
                    
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
    if((re.search(p, str)) or (re.findall('.ppt',str)) or (re.findall(".docx",str)) ):
        return True
    else:
        return False


if __name__ == "__main__":
    print('Nhập link(s): ')
    Input=input()
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
