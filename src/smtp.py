import base64
import os
from socket import *

from dotenv import load_dotenv

load_dotenv()

username = os.environ["USER_NAME"]
password = os.environ["PASS"]


msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"


mailserver = ("localhost", 1025)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode()

print(recv)
if recv[:3] != "220":
    print("220 reply not received from server.")

heloCommand = "EHLO Alice\r\n"
clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != "250":
    print("250 reply not received from server.")


isLocalhost = os.environ["DEV"] == "dev"
if isLocalhost == False:
    base64_str = ("\x00" + username + "\x00" + password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
    clientSocket.send(authMsg)
    recv_auth = clientSocket.recv(1024)
    if recv_auth.decode()[:3] != "235":
        print(f"Auth failed: {recv_auth.decode()}")
        clientSocket.close()
        raise SystemExit(1)
    print(recv_auth.decode())

if recv1[:3] != "250":
    print("250 reply not received from server.")

mailFrom = "MAIL FROM: <anyemailid@gmail.com> \r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
print(f"After MAIL FROM command: {recv2}")
if recv1[:3] != "250":
    print("250 reply not received from server.")

rcptTo = "RCPT TO: <destination@gmail.com> \r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
print(f"After RCPT TO command: {recv3}")
if recv1[:3] != "250":
    print("250 reply not received from server.")

data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
print(f"After DATA command: {recv4}")
if recv1[:3] != "250":
    print("250 reply not received from server.")

subject = "Subject: SMTP mail client testing \r\n\r\n"
clientSocket.send(subject.encode())
message = msg + endmsg
clientSocket.send(message.encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:" + recv_msg.decode())
if recv1[:3] != "250":
    print("250 reply not received from server.")

clientSocket.send("QUIT\r\n".encode())
message = clientSocket.recv(1024)
print(message)
clientSocket.close()
