import socket
import socketserver
import threading
from dnslib import DNSRecord


class TCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        conn = self.request
        while True:
            data = conn.recv(1024)

            if not data:
                break
            parsed_packet = DNSRecord.parse(data[2:])
            print("TCP from connected user: " + str(parsed_packet))
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dns_host = "1.1.1.1"
            dns_port = 53
            client_socket.sendto(data[2:], (dns_host, dns_port))
            dns_response, source_address = client_socket.recvfrom(1024)
            client_socket.close()


            response = (b'\x00' + chr(len(dns_response)).encode() + dns_response)
            print(response)

            conn.sendall(response)


class UDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        csocket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_host = "1.1.1.1"


        dns_port = 53
        client_socket.sendto(data, (dns_host, dns_port))
        received_data, dns_addr = client_socket.recvfrom(1024)
        print(received_data)

        csocket.sendto(received_data, self.client_address)



if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(
            ("0.0.0.0", 5000), TCPRequestHandler
    ) as tcpserver, socketserver.UDPServer(("0.0.0.0", 5000), UDPRequestHandler) as udpserver:
        tcpserver.daemon_threads = True
        tcp_thread = threading.Thread(target=tcpserver.serve_forever)
        tcp_thread.start()
        udpserver.daemon_threads = True
        udpserver.serve_forever()

