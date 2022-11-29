import os
import socket
import time

##################################################################################################


def socket_read_n(sock, n):
    """ Read exactly n bytes from the socket.
        Raise RuntimeError if the connection closed before
        n bytes were read.
    """
    buf = ''
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf


def recv_timeout(s, n):

    # total data partwise in an array
    total_data = []
    data = ''

    timeout = 2
    # beginning time
    begin = time.time()
    while 1:
        # if you got some data, then break after timeout
        if remain and time.time()-begin > timeout:
            break

        # if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        # recv something
        try:
            data = s.recv(n-len(data))
            if data:
                total_data.append(data)
                remain = n - len(data)
                # change the beginning time for measurement
                begin = time.time()
            else:
                # sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    # join all parts to make final string
    return b''.join(total_data)


def readnbytes(sock, n):
    buff = b''
    while n > 0:
        b = sock.recv(n)
        buff += b
        if len(b) == 0:
            raise EOFError
        n -= len(b)
    return buff


def readnbyte(sock, n):
    buff = bytearray(n)
    pos = 0
    while pos < n:
        cr = sock.recv_into(memoryview(buff)[pos:])
        if cr == 0:
            raise EOFError
        pos += cr
    return buff


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def recv_all(connection):
    """
    Function for all data

    :param connection: socket connection
    :return: received data
    """
    data = list()
    while True:
        data.append(connection.recv(2048))
        if not data[-1]:
            return b''.join(data)


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

    # body download
    timeout = 2
    s.setblocking(0)
    begin = time.time()
    BUFFER_SIZE = 1024 * 4
    with open(file_name, 'wb') as f:
        while True:
            try:

                chunkSize_line = ""
                while not chunkSize_line.endswith('\n'):
                    chunkSize_line += s.recv(1).decode()
                chunkSize_line = chunkSize_line[0:chunkSize_line.find('\r\n')]
                chunk_size = int(chunkSize_line, 16)
                print('Chunk_size = ', chunk_size)

                if chunk_size > 0:

                    data = s.recv(chunk_size + 2)
                    # data = socket_read_n(s, chunk_size + 2)
                    # data = recv_timeout(s, chunk_size + 2)
                    # data = readnbytes(s, chunk_size + 2)
                    # data = readnbyte(s, chunk_size + 2)
                    # data = recvall(s, chunk_size + 2)
                    # data = recv_all(s, chunk_size + 2)

                    # data = ""
                    # while len(data) < chunk_size + 2:
                    #     if len(data) + BUFFER_SIZE < chunk_size + 2:
                    #         data += s.recv(BUFFER_SIZE).decode()
                    #     else:
                    #         data += s.recv(chunk_size + 2 - len(data)).decode()

                    # n = chunk_size + 2
                    # count = 0
                    # while count < n:
                    #     data = s.recv(n - count)
                    #     if not data:
                    #         break
                    #     print(data)
                    #     f.write(data)
                    #     f.flush()
                    #     count += len(data.decode())

                    # n = chunk_size + 2
                    # while n > 0:
                    #     data = s.recv(n)
                    #     if data == '':
                    #         n -= len(data)
                    #         print(data)
                    #         f.write(data)
                    #         f.flush()
                    #     else:
                    #         raise RuntimeError('unexpected connection close')

                    print(data)
                    f.write(data)
                    f.flush()
                    print('Saving...')
                    begin = time.time()
                else:
                    time.sleep(0.1)

            except:
                pass

            # if you got some chunk size, then break after wait sec
            if chunk_size and time.time()-begin > timeout:
                break
            # if you got no chunk size at all, wait a little longer
            elif time.time()-begin > timeout * 2:
                break

    print('Saving completed')
    s.close()


##################################################################################################
if __name__ == "__main__":
    download_chunked()
