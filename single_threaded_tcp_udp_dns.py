import socket
import socketserver
import threading
from dnslib import DNSRecord
import logging






class TCP_RequestHandler(socketserver.BaseRequestHandler):


    def handle(self) -> None:
        conn = self.request
        while True:
            data = conn.recv(1024)

            if not data:
                break

            logging.info(f"recv: {data!r}")
            conn.sendall(data)

    



class TCP:
    @staticmethod
    def server_program():
        # get the hostname
        host = "0.0.0.0" #socket.gethostname()
        port = 5000  # initiate port no above 1024

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(2)
        
        while True:
            conn, address = server_socket.accept()  # accept new connection
            print("TCP Connection from: " + str(address))
            while True:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                data = conn.recv(1024)
                if not data:
                    # if data is not received break
                    break
                parsed_packet = DNSRecord.parse(data[2:])
                print("TCP from connected user: " + str(parsed_packet))
                client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dns_host= "1.1.1.1"
                dns_port= 53
                client_socket.sendto(data[2:], (dns_host, dns_port))
                dns_response, source_address=client_socket.recvfrom(1024)
                client_socket.close()

                response=(b'\x00'+chr(len(dns_response)).encode() + dns_response)
                conn.sendall(response)

            conn.close()  # close the connection

class UDP:
    @staticmethod
    def server_program():
        host = "0.0.0.0"
        port = 5000

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host, port))

        print("UDP Server started")

        while True:
            data, addr = server_socket.recvfrom(1024)
            parsed_packet = DNSRecord.parse(data)
            print("UDP from connected user: " + str(parsed_packet))
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM )  # instantiate
            dns_host = "1.1.1.1"
            dns_port = 53
            client_socket.sendto(data, (dns_host, dns_port))
            received_data, dns_addr= client_socket.recvfrom(1024)

            server_socket.sendto(received_data, addr)

        server_socket.close()

# Create threads for both TCP and UDP server programs
tcp_thread = threading.Thread(target=TCP.server_program)
udp_thread = threading.Thread(target=UDP.server_program)

# Start both threads
tcp_thread.start()
udp_thread.start()

# Wait for both threads to finish
#tcp_thread.join()
#udp_thread.join()