import socket


##################################################################################################
def download_chunked():

    # Input url and create file
    Input = "http://www.google.com/index.html"
    if (Input.find("http://") != -1):
        Input = Input.replace("http://", '')
    poshost = Input.find("/")
    if (poshost == -1):
        domain = Input.split('//')[-1].strip('/').split('/')[0]
        subdirectory = ""
    else:
        domain = Input.split('//')[-1].strip('/').split('/')[0]
        subdirectory = Input.split('//')[-1].lstrip(domain)

    temp_file_name = ''
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

    # socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((domain, 80))
    request = "GET "+subdirectory+" HTTP/1.1\r\nHost:" + \
        domain+"\r\nConnection: keep-alive\r\n\r\n"
    s.sendall(request.encode())

    # header download
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
                        print(data)
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


##################################################################################################
if __name__ == "__main__":
    download_chunked()
