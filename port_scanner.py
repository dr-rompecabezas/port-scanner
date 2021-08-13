import socket
import sys
import subprocess
import common_ports
# import threading
# from queue import Queue

subprocess.call('clear', shell=True)


def get_open_ports(target, port_range, verbose=None):
    """A simple port scan tool"""
    
    open_ports = []
    unknown_hostname = False

    if target[0].isdigit():
        try:
            host_ip = socket.gethostbyaddr(target)[2][0]
            hostname = socket.gethostbyaddr(target)[0]
            print(host_ip)
        except socket.gaierror as err:
            print(err)
            return "Error: Invalid IP address"
        except socket.herror as err:
            print(err)
            try:
                host_ip = socket.gethostbyname(target)
                unknown_hostname = True
                print(host_ip)
            except socket.herror as err:
                print(err)
                return "Error: Invalid IP address"
    else:
        try:
            host_ip = socket.gethostbyname_ex(target)[2][0]
            hostname = socket.gethostbyname_ex(target)[0]
            print(host_ip)
        except socket.gaierror as err:
            print(err)
            return "Error: Invalid hostname"

    try:
        for port in range(port_range[0], port_range[1]+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((host_ip, port)):
                # print(f"Port {port} is closed")
                pass
            else:
                # print(f"Port {port} is open")
                open_ports.append(port)
            sock.close()

    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()
            
    if verbose:
        if unknown_hostname:
            header = f'Open ports for {host_ip}'
        else:
            header = f'Open ports for {hostname} ({host_ip})'
        sub_header = "\nPORT     SERVICE"
        content = ''
        for port in open_ports:
            if port in common_ports.ports_and_services:
                content = content + "\n" + str(port) \
                          + ' ' * (9 - len(str(port))) \
                          + common_ports.ports_and_services[port]
            else:
                content = content + str(port) + "\n"

        printout = '' + header + sub_header + content
        print(printout)
        return printout
    else:
        return open_ports
