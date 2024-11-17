'''
This module defines the behaviour of server in your Chat Application
'''
from pydoc import cli
import sys
import getopt
import socket
import threading
from time import get_clock_info
import util
from threading import Thread

class Server:
    
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''

    def __init__(self, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET == IPV4 family , SOCK_STREAM  == TCP packets communication
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows multiple clients to send data at same server port number 
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.username_list = []
        # self.threading_states =  threading.active_count()
        
        # {
        #     "user": "",
        #     "socket": 
        # } # sample lists of the usernames 


    def server_limit(self):
        self.sock.listen(util.MAX_NUM_CLIENTS)
   

    #def client_listener(self , client):

    #     while True :
    #         message = client.recv(2048).decode("utf-8")
    #         if(message != " "):
    #             pass
    #             # perform string manipulations to extract the type of message and it's respective attributes and then go to selective type using my own functions like send_msg_specific 

    #         else :
    #             print("message recieved from client is empty ")
            

    def send_msgs_to_all(self , message ):

        for users in self.username_list:

            self.send_msg_specific(self.username_list[1], message)

    def send_msg_specific( self , message , client):
        client.sendall(message.encode())

    def search_username(self, message_list):
        for user_name , cl in self.username_list:
            if (user_name == message_list[1]):
                return True
        return False

    def join_function( self , message_list , client ):
        
        response = ""
        
        if( len(self.username_list) >= util.MAX_NUM_CLIENTS ) :
            response = "err_server_full"
            print("disconnected : server full")
            client.send(util.make_message("err_server_full" , 2 , None).encode("utf-8"))
        
        elif(self.search_username(message_list)):
            response = "ERR_USERNAME_UNAVAILABLE"
            print("disconnected: username not available")
            client.send(util.make_message("err_username_unavailable" , 2 , None).encode("utf-8"))
        
        else :
            lst = [message_list[1] , client]
            self.username_list.append(lst)
            
            print("join:", message_list[1])
 
        # if(response !=""):
        #     client.send(response.encode("utf-8"))
    
    def req_user_function(self , message_list , client):
        
        response = "RESPONSE_USERS_LIST"
        target_username = ""
        l = len(self.username_list)
        for i in range(0, l):
           x = self.username_list[i]

           if x[1] == client:
               target_username = x[0]
               break


        print("request_users_list:" , target_username) # check this whether this works or not!!!!!

        self.response_user_function(client ,target_username)

    def response_user_function( self, client ,target_username) :

        arranged_list =  []
        # for i , x in self.username_list : 
        #     arranged_list = arranged_list.append(i)
        
        l = len(self.username_list)
        
        for i in range(0, l):
            x = self.username_list[i]
            arranged_list.append(x[0])
            #print(arranged_list)


        arranged_list.sort()
        
        #print(arranged_list)

        response = " ".join(arranged_list)

        response = "list: " + response

        client.send(util.make_message(response, 3 , ).encode("utf-8")) ## is this necessary or not adding "list:" ? 

    def get_part_from_list (self , message_list) :
        pass

    def get_client_username(self, client) :

        for user_name , cl in self.username_list:
            if (cl == client):
                return user_name
        
        return None
 
    def send_message( self , message_list , client) :

        #print(message_list)
        sender_username = self.get_client_username(client)
        #print("msg: " , sender_username )

        count = message_list[1]
        count = int(count)

        all_tagged_usernames = []
        
        #getting all the tagged usernames in the msg by the sender client
        for i in range(2 , 2 + count) :
            all_tagged_usernames.append(message_list[i])

        #creating actual message list
         
        message_send = message_list[2 + count : (len(message_list) -1) ]

        #joining msgs in the form of sentences
        response = " ".join(message_send)

        #adding the sender username aswell to the message
        response = "forward_message " + sender_username+ " " + response 

        all_stored_usernames = []
        
        #print(response)
        

        #making server forward the msgs
        for user_details in self.username_list:
            all_stored_usernames.append(user_details[0])
            if (user_details[0] in all_tagged_usernames ):
                #print("yesss!",user_details[0])
                user_details[1].send(util.make_message(response, 4 ,).encode("utf-8"))

        # all mentioned usernames :

        #making server print relevant msgs on it's screen
        for x in all_tagged_usernames :
            if(x != sender_username):
                if ( x in all_stored_usernames ) :
                    print ("msg: " , sender_username)
                else :
                    print ("msg: ",sender_username," to non-existent user ", x)

    def send_file(self, message_list , client) :

        
        #print("hereee")
        sender_username = self.get_client_username(client)

        # getting all the tagged usernames :

        count =message_list[1]

        count = int(count)

        all_tagged_usernames = []

        for i in range(2 , 2 + count) :
            all_tagged_usernames.append(message_list[i])

        # getting the name of the file  # dsdfsdsd abc.txt {124455}

        file_details = message_list[2+count : len(message_list)-1] 


        # making file details into a string :

        response = " ".join(file_details)

        # adding username to the response :

        response = "forward_file "+ str(count)+ " " +sender_username + " " + response

        # sending data over to the relevent users :

        print(response)
        #
        all_stored_usernames = []
        
        
        # for username , user_client in self.username_list:
        #     all_stored_usernames.append(username)
        #     if (username in all_tagged_usernames):
        #         user_client.send(util.make_message(response, 4 , ).encode("utf-8"))


        for user_details in self.username_list:
            all_stored_usernames.append(user_details[0])
            if (user_details[0] in all_tagged_usernames):
                #print("yesss!",user_details[0])
                user_details[1].send(util.make_message(response, 4 ,).encode("utf-8"))

        # printing relevent msg on server's screen :

        for x in all_tagged_usernames :
            if ( x in all_stored_usernames) :
                print ("file: " , sender_username)
            else :
                print ("file: ",sender_username," to non-existent user ", x)

    def remove_connection( self, client) :
        
        sender_username = self.get_client_username(client)

        print("disconnected:" , sender_username)

        counter = 0
        
        # for username , user_client in self.username_list:
        #     if (username == sender_username) :
        #         del self.username_list[counter]

        all_stored_usernames = []
        for user_details in self.username_list:
            all_stored_usernames.append(user_details[0])
            if (user_details[0] == sender_username):
                del self.username_list[counter]
            counter = counter+1

    def unknown_command(self , client ):
        
        target_username = self.get_client_username(client)
        print("disconnected: ", target_username , " sent unknown command")

        counter = 0
        
        # for username , user_client in self.username_list:
        #     if (username == sender_username) :
        #         del self.username_list[counter]

        
        
        
        all_stored_usernames = []
        for user_details in self.username_list:
            all_stored_usernames.append(user_details[0])
            if (user_details[0] == target_username):
                user_details[1].send(util.make_message("disconnected: server received an unknown command", 4 ,).encode("utf-8"))
                del self.username_list[counter]
            counter = counter+1
        
    def client_handler(self, client):
        
        # server will listen for client message including join request , username 
        while True :

            message = client.recv(2048).decode("utf-8")

            if(message != ""):
                
                message_list = message.split(" ")

                if(message_list[0] ==  "join"):
                    self.join_function(message_list , client)

                elif(message_list[0] == "request_users_list"):  # shouldnt this be message =="requestuserslist"
                    self.req_user_function(message_list , client)

                elif (message_list[0] == "send_message") :
                    self.send_message(message_list , client)               

                elif (message_list[0] == "send_file"):
                    self.send_file(message_list , client)
                
                elif (message_list[0] == "disconnect"):
                    self.remove_connection(client)
                    return
                else : 
                    self.unknown_command(client)
                    return
                  


            """

            # if(join_message[0:4] != "join") :

            #     print("Invalid join request ")
            
            # elif (join_message[5 : len(join_message)] in self.username_list[0] ):

            #     print ("Username already present in the database ")

            # else :
            #     self.username_list.append(join_message[5 : len(join_message)] , client)
            #     print("Username is sucessfully added ! ")
            #     break

        
        # A thread is made to deal with accepted client's msgs and 
        # is this required tho? like i already have create a thread for a client
        # threading.Thread(target= self.client_listener , args = (client , join_message[5 : len(join_message)],)).start()

            """

    def start(self):
        '''
        Main loop. 
        continue receiving messages from Clients and processing it
        '''
        #  make server listen all the time
        #self.server_limit()

        self.sock.listen(10)
        print("server started")
        while True :
            
            """
            Steps :

                1) make my socket (aka server) listen for the client connections 

                2) create a thread for each client's connection and perform respective funtionality
            """
            # making my server listen to the limit  
           

            client,address = self.sock.accept() # my server here is listening for all the clients connections. Also socket is my element having functionality of server here. Also we are getting a tuple having elements client and address .
            
            # a separate thread made to deal with a new client 
            threading.Thread(target= self.client_handler, args = (client,)).start()
            #print(threading.active_count())
            



        raise NotImplementedError

# Do not change this part of code


if __name__ == "__main__":
    
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a", ["port=", "address="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    SERVER = Server(DEST, PORT)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
