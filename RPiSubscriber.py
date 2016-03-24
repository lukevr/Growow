__author__ = 'luke'

import zmq
import os
import time
import signal
import subprocess
from threading import Thread,Event

# import sys

class RasPiVidThread(Thread):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.event_stop = Event()
        self.cmd = "raspivid -vf -n -w 640 -h 480 -o -t 0 -b 2000000 | nc 178.214.221.154 5777"
    
    def stop(self):
        self.event_stop.set()
        self.process.terminate()

    def run(self):
        self.process = subprocess.Popen(self.cmd,
                                        stdout=subprocess.PIPE,
                                        shell=True)

class SubscriberListenerThread(Thread):
    def __init__(self,connect_to='tcp://178.214.221.154:5563'):
        super(self.__class__,self).__init__()
        self.is_streaming = False
        self.context = zmq.Context()
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect(connect_to)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b"P")
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b"S")
        self.streamer = RasPiVidThread()
    
    def start_streaming(self):
        self.is_streaming = True
        self.streamer.run()

    def stop_streaming(self):
        self.streamer.stop()
        self.is_streaming = True
    
    def run(self):
        while 1:
            [address, contents] = self.subscriber.recv_multipart()
            print('{} {} {}'.format(self.streamer,
                                    repr(address),
                                    rerp(contents)))
            if "P" == address and not self.is_streaming:
                self.start_streaming()

            if "S" == address and self.is_streaming:
                self.stop_streaming()
            
            time.sleep(1)


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


def main2():
    subscriber = SubscriberListenerThread()
    subscriber.join()

if __name__ == "__main__":
    main2()
