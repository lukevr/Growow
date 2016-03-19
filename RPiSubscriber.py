__author__ = 'luke'

import zmq
import os
import time
import signal
import subprocess

# import sys


def main():
    #ip = sys.argv[1]
    ip = "178.214.221.154"

    port = 5563
    string = "tcp://" + ip + ":" + str(port)

    # Prepare our context and publisher
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(string)
    subscriber.setsockopt(zmq.SUBSCRIBE, b"P")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"S")

    pro = None
    time2sleep = 0.5
    while True:
        # Read envelope with address
        [address, contents] = subscriber.recv_multipart()

        if address == "P" and not is_process_running(pro):
            # Play
            cmd = "raspivid -vf -n -w 640 -h 480 -o -t 0 -b 2000000 | nc 178.214.221.154 5777"
            pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            print("[%s] %s -- %s" % (address, contents, pro))

        if address == "S" and is_process_running(pro):
            # Stop
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
            print("[%s] %s -- %s" % (address, contents, pro))

        address == 0;
        time.sleep(time2sleep)

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

def is_process_running(pro):

    if pro is None:
        return False
    try:
        os.kill(pro.pid, 0)
        return True
    except OSError:
        return False

if __name__ == "__main__":
    main()
