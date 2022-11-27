import os
import socket


# def recvall(sock, buffer_size=1024*4):
#     buf = sock.recv(buffer_size)
#     while buf:
#         yield buf
#         if len(buf) < buffer_size:
#             break
#         buf = sock.recv(buffer_size)


# def decode_chunked(content):
#     content = content.decode('utf-8')
#     content = content.lstrip('\r')
#     content = content.lstrip('\n')
#     temp = content.find('\r\n')
#     strtemp = content[0:temp]
#     readbytes = int(strtemp, 16)
#     newcont = ''
#     start = 2
#     offset = temp + 2
#     newcont = ''
#     while (readbytes > 0):
#         newcont += content[offset:readbytes + offset]
#         offset += readbytes
#         endtemp = content.find('\r\n', offset + 2)
#         if (endtemp > -1):
#             strtemp = content[offset + 2:endtemp]
#             readbytes = int(strtemp, 16)
#             if (readbytes == 0):
#                 break
#             else:
#                 offset = endtemp + 2

#     content = newcont
#     return content


def download_chunked():

    Input = "http://www.google.com/index.html"
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
    print(data)
    print(header)

    filename = Input.split('/')[-1]
    data = data[data.find(b'\r\n\r\n')+4:]
    name_folder = subdirectory.split('/')[-2]
    dest_folder = domain+"_"+name_folder
    file_path = os.path.join(dest_folder, filename)
    print("saving to", os.path.abspath(file_path))

    with open(file_path, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    BUFF_SIZE = 1024*4
    with open(file_path, 'ab') as f:
        while True:
            data = s.recv(BUFF_SIZE)
            if not data:
                break
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
    s.close()


if __name__ == "__main__":
    download_chunked()
