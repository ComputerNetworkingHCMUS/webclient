import socket
import requests
import os
from bs4 import BeautifulSoup 
from urllib import parse  # for separating path and hostname
chunk_size =20*1024
FORMAT = 'utf8'
#myurl = "https://web.stanford.edu/class/cs224w/slides/"


def getHTML(myurl):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    url = parse.urlparse(myurl)
    s.connect((url[1], 80))
    msg = "GET " + url[2] + " HTTP/1.1\r\nHost: "+url[1]+"\r\n\r\n"
    print(msg)
    s.sendall(msg.encode(FORMAT))
    #print(s.recv(chunk_size).decode(FORMAT))
    request=requests.get(myurl)
    soup=BeautifulSoup(request.text,'html.parser')
    urls=[]
    name_folder=url[2].split('/')[-2]
    for link in soup.find_all('a'):
         #print(link.get('href'))
         if (link.get('href') != "?C=N;O=D") & (link.get('href') != "?C=M;O=A") & (link.get('href') != "?C=S;O=A") & (link.get('href') != "?C=D;O=A"):
             download(myurl+link.get('href'),url[1]+"_"+name_folder)
             print(link.get('href'))
    
def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


if __name__ == "__main__":
    print("Enter ur url: ")
    myurl=input()
    getHTML(myurl)
    
