'''
This module defines the behaviour of a client in your Chat Application
'''
from email import message
from http import client
import sys
import getopt
import socket
import random
from threading import Thread
import os
from tkinter.filedialog import Open
from turtle import forward
import util


'''
Write your code inside this class. 
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen 
for incoming messages in this function.
'''

class Client:
    '''
    This is the main Client Class. 
    '''

    def __init__(self, username, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(None)
        self.name = username
        self.sock.connect((self.server_addr,self.server_port))


    def join_message(self):
        self.sock.send(util.make_message("join",1,self.name).encode("utf-8"))

    def send_list_req(self):
        self.sock.send(util.make_message("request_users_list" ,2,).encode("utf-8"))

    def print_list(self, message_list):
        
        reduced_list = message_list[1 : -1]

        message = " ".join(reduced_list)
        message = "list: " + message
        print (message)
        
    def send_message(self , message_list):
        
        message_list[0] = "send_message"

        response = " ".join(message_list)
        print(response)
        self.sock.send(util.make_message(response ,4,).encode("utf-8")) 

    def get_message(self, message_list):

        # print(message_list)
        
        # print("hereee!")
        
        reduce_message_list = message_list[0 : -1]
        reduce_message_list[0] = "msg:"
        reduce_message_list[1] = reduce_message_list[1] + ":"

        response = " ".join(reduce_message_list)

        print(response) 

    def send_file(self , message_list):

        file_name = message_list[-1]

        with open(file_name,"r") as file:
            file_contents = file.read()

        #print(file_contents)

        message_list.append(file_contents)

        message_list[0] = "send_file"

        response = " ".join(message_list)

    
        #self.sock.send(util.make_message(response ,4,).encode("utf-8")) 

        self.sock.send(util.make_message(response , 4 ,).encode("utf-8"))

    def get_file(self , message_list):

        file_contents = []
        file_name = message_list[3]
        file_content = message_list[4:-1]

        response = " ".join(file_content)
        #print(response)

        file = open("{file_name}","w")
        file.write(response)
        file.close
        
    def disconnect(self):
        response = "disconnect"
        self.sock.send(util.make_message(response , 1 ,).encode("utf-8"))
        
   

    
    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it

        steps : 

            1) connect to the server and then send the join function:

        '''

        self.join_message()

        while True :

            
            message =input("enter the command...")

            # splitting the list request :

            message_list = message.split(" ")

            # checking the types of the commands :
            if (message_list[0] == "list"):
                self.send_list_req()
            elif(message_list[0] == "msg"):
                self.send_message(message_list)
            elif(message_list[0] == "file"):
                self.send_file(message_list)
            elif(message_list[0] == "quit"):
                self.disconnect()
                print("quitting")
                return
            

            




            
            





        #raise NotImplementedError

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''
        
        # self.sock.recv(5012)
        while True:
            
            message = self.sock.recv(2048).decode("utf-8")

            message_list = message.split(" ")

            if(message_list[0] =="list:"):
                self.print_list(message_list)
            elif(message_list[0] == "forward_message"):
                self.get_message(message_list)
            elif(message_list[0] == "forward_file"):
                self.get_file(message_list)
            elif(message_list[0]== "err_server_full"):
                print("disconnected : server full")
                return
            elif(message_list[0] == "err_username_unavailable"):
                print("disconnected : username not available")
                return
            elif(message == "disconnected: server received an unknown command"):
                print("disconnected: server received an unknown command")
                return
            else :
                continue 

                
            
            

            
                

            



        
        
        #raise NotImplementedError














# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our Client module completion
        '''
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "u:p:a", ["user=", "port=", "address="])
    except getopt.error:
        helper()
        exit(1)

    PORT = 15000
    DEST = "localhost"
    USER_NAME = None
    for o, a in OPTS:
        if o in ("-u", "--user="):
            USER_NAME = a
        elif o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    if USER_NAME is None:
        print("Missing Username.")
        helper()
        exit(1)

    S = Client(USER_NAME, DEST, PORT)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
