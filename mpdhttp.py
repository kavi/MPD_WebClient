from flask import Flask, render_template, redirect, url_for
import logging
import getopt
import query
import socket
import sys
import os
import signal

MPD_IP='192.168.1.10'
MPD_PORT=6600

app = Flask(__name__)

@app.route('/mpd/') 
def hello_world():
    currentsong = query.get_currentsong()
    playlist = query.get_currentplaylist()
    return render_template('hello.html', 
           currentsong=currentsong,
           currentsong_lengthm=currentsong.length / 60,
           currentsong_lengths=currentsong.length % 60,
           playlist=playlist)

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    print "Command: " + cmd
    print  query.mpd_query(cmd)
    return redirect('http://192.168.1.10:5000/mpd/')

@app.route('/command/<cmd>/<arg>', methods=['POST'])
def command_arg(cmd, arg):
    query.mpd_query(cmd, arg)
    return redirect('http://192.168.1.10:5000/mpd/')


def make_pid(pidfile):
    pid = str(os.getpid())
 
    if os.path.isfile(pidfile):
        print "%s already exists, exiting" % pidfile
        sys.exit(1)
    else:
        file(pidfile, 'w').write(pid)

def signal_handler(signal, frame):
    if os.path.isfile(PID):
      os.remove(PID)
    sys.exit(0)

def usage():
    print "Usage: --pidfile=<pidfile>"

if __name__ == '__main__':
    PID = None
    optlist, args = getopt.getopt(sys.argv[1:], 'p:', ['pidfile='])
    for opt,arg in optlist:
        if "--pidfile" == opt:
            PID=arg
    if PID is None:
        usage()
        sys.exit(1)
    signal.signal(signal.SIGINT, signal_handler)
    make_pid(pidfile=PID)
    app.debug = False
    app.run(host='0.0.0.0')
