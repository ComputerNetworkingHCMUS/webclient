import os
import socket
import time


def download_chunked(Input=""):

    domain = Input.split('//')[-1].strip('/').split('/')[0]
    subdirectory = Input.split('//')[-1].lstrip(domain)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))

    request = "GET "+subdirectory+" HTTP/1.1\r\nHost:" + \
        domain+"\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())

    data = s.recv(1024*4)
    header = data[0:data.find(b'\r\n\r\n')]
    temp = header.decode()
    temp = temp.split('Content-Length: ')[-1]
    temp = temp.split('\r\n')[0]

    filename = Input.split('/')[-1]
    name_folder = subdirectory.split('/')[-2]
    dest_folder = domain+"_"+name_folder
    file_path = os.path.join(dest_folder, filename)
    print("saving to", os.path.abspath(file_path))

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    data = data[data.find(b'\r\n\r\n')+4:]
    with open(file_path, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


    BUFF_SIZE = 1024*4
    timeout = 2
    s.setblocking(0)
    begin = time.time()
    with open(file_path, 'ab') as f:
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
                    os.fsync(f.fileno())
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass

    print('Saving completed')
    s.close()
