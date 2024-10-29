import pickle
import time
import socket
import threading

ERROR_OPCODE = 0x01
END_OPCODE = 0x00
class WiFiManager:
    """
    This class implement a simple wifi manager. There is two components the client (typically the raspberry pi) and the
    server (typically the jetson nano). The client ask things to the server (the opposite is not possible).
    """
    def __init__(self,ip_connect,port_connect,role):
        """
        See the doc on the own cloud
        ip_connect: ip of the server (localhost if role=="server")
        port_connect: port of the server
        role: "server" or "client"
        """
        self.server_ip = ip_connect
        self.server_port = port_connect
        self.role = role
        if(role == "server"):
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.functions_call=dict()
            self.functions_call[ERROR_OPCODE]=self.error
            self.functions_call[END_OPCODE] = self.close
        else:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        """
        Start the server or client and make the connections.

        """
        if (self.role == "server"):
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            self.client_socket, client_address = self.server_socket.accept()
            #make a thread to receipt the instructions in parrallel
            self.thread = threading.Thread(target=self.server_job)
            self.alive=True
            self.thread.start()
        else:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("connect")
            self.client_socket.connect((self.server_ip, self.server_port))

        if(self.role == "server"):
            self.alive=True


    def server_job(self):
        """
        Server function
        """
        while(self.alive):
            data=self.receive()
            if data is None:
                continue
            id_op=data[0]
            if not self.functions_call.keys().__contains__(id_op):
                print("Wifi communication: Error op code not valid.")
            else:
                result=self.functions_call[id_op](data[1:])
                if(result!=None):
                    self.send(result)


    def send(self, data):
        """
        Send data
        """
        serialized_data = pickle.dumps(data)
        self.client_socket.send(serialized_data)

    def send_return(self, data):
        """
        Can only be used by the client to send an instruction and wait for the result.
        """
        serialized_data = pickle.dumps(data)
        self.client_socket.send(serialized_data)
        return self.receive()

    def receive(self):
        serialized_data = self.client_socket.recv(4096)
        if len(serialized_data)==0:
            return None
        received_data = pickle.loads(serialized_data)
        return received_data


    def close(self,args):
        if (self.role == "server"):
            self.server_socket.close()
            self.alive = False
        self.client_socket.close()


    def error(self,args):
        print("Wifi communication: error raised by the user!")



