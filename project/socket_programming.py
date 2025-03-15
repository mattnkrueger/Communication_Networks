# Matthew Krueger
# Communication Networks Fall 2024
#
# Python Version:
#   3.12.4
#
# How to Run:
#   python3 socket_programming.py [arg1] [arg2] [arg3]

import sys
import socket

def connect_udp(udp_server_host: str, upd_server_port: int, uid: str) -> list[str]:
    """
    Connects to UDP server

    Parameters:
        udp_server_host: str - hostname of the server
        udp_server_port: int - port number of the server
        uid: str - string representation of uiowa student id.

    Returns: 
        list: list of strings containig parsed message response from udp server
    """
    try:
        # connect using udp socket (IPv4, User Datagram Protocol)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # define server
        server = (udp_server_host, udp_server_port)

        # send uid to server
        message_in = uid.encode("utf8")
        print("UDP data sent: ", uid)
        print("...")
        sock.sendto(message_in, server) 

        # receive from server
        data = sock.recv(udp_server_port)
        received = "{!r}".format(data.decode("utf8"))

        # unpack string 
        message_out = received.replace("'", "")
        split: list = message_out.split(" ")

        print("UDP data received: ", f"[{split[0]}] [{split[1]}] [{split[2]}]")

        # close socket
        sock.close()

        return split
    except socket.error: 
        print("main: something went wrong with udp socket connection")
        sys.exit(1)

def connect_tcp(tcp_server_host: str, tcp_server_port: int) -> None:
    """
    Connects to TCP server

    Parameters:
        tcp_server_host: str - hostname of the server
        tcp_server_port: int - port number of the server

    Returns: 
        None
    """
    try:
        # connect using tcp socket (IPv4, Transmission Control Protocol)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # define server & connect
        server = (tcp_server_host, tcp_server_port)
        sock.connect(server)

        # send initial message 
        message_in = "hello"
        print("TCP data sent: ", message_in)
        sock.sendall(message_in.encode("utf8"))

        # if this has worked, then there should be a connection
        # this is not multithreaded, only back and forth communication
        # starting counter at 1 as initial message already sent
        connected: bool = True
        bridge_crossed: bool = False
        quit_message: str = ""

        while connected:
            # receive message
            data = sock.recv(tcp_server_port)
            received = "{!r}".format(data.decode("utf8"))
            message_out = received.replace("'", "")
            message_out = received.replace("\n", "\n")
            print(f"TCP data received: ", message_out)

            # check if bridge crossed (this is the start of the message granting you to cross)
            if "Right, off you go." in message_out:
                bridge_crossed = True
                print("\nYOU HAVE CROSSED THE BRIDGE!\n")
                quit_message = "- send 'QUIT' to exit"
                
            # client console to get next message 
            message_in = input(f"Next message to send? {quit_message}: ")

            # either quit or send new message. User can only quit if the bridge is crossed
            if message_in.lower() == "quit" and bridge_crossed:
                print("disconnecting from server...")
                sock.close()
                connected = False
            else:
                sock.sendall(message_in.encode("utf8"))

    except socket.error: 
        print("main: something went wrong with tcp socket connection")
        sys.exit(1)
    finally:
        print("exiting program.")

if __name__ == "__main__":
    try:
        # get args
        udp_server_host: str = sys.argv[1]
        udp_server_port: int = int(sys.argv[2])
        uid: str = sys.argv[3]
        print(udp_server_host, udp_server_port, uid)
        print(type(udp_server_host), type(udp_server_port), type(uid))

    except IndexError:
        print("main: IndexError - incorrect number of arguments passed.")
        print("please input following arguments:", "[UDPServerHostName] [UDPServerPort] [YourStudentIDNumber]")
        sys.exit(1)
    except:
        print("main: something went wrong with cli args")
        sys.exit(1)

    # connect udp first
    server_response = connect_udp(udp_server_host, udp_server_port, uid)

    # unpack response
    tcp_server_host: str = server_response[0]
    tcp_server_port: int = int(server_response[1])
    secret_number: int = int(server_response[2])
    binary_secret_number: str = "{0:b}".format(secret_number)
    
    # prepend 0 (if binary not already 4 digs)
    needs_zeros = False
    if len(binary_secret_number) < 4:
        needs_zeros = True
        
    # prepend until length is 4
    while (needs_zeros):
        binary_secret_number = "0" + binary_secret_number
        
        if len(binary_secret_number) > 3:
            needs_zeros = False

    # print out for reference
    print("\nYour Secret Number: ", secret_number, f" (binary: {binary_secret_number})\n")

    # connect tcp second
    connect_tcp(tcp_server_host, tcp_server_port)
