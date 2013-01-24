from flask import Flask, render_template, redirect, url_for
import socket
import sys
import os
import ConfigParser
import getopt
import signal
import query

SELF_IP='192.168.1.10'
SELF_PORT='5000'

MPD_IP='192.168.1.10'
MPD_PORT=6600

app = Flask(__name__)

@app.route('/mpd/') 
def default():
    currentsong = query.get_currentsong()
    playlist = query.get_currentplaylist()
    return render_template('mpd.html', 
           currentsong=currentsong,
           currentsong_lengthm=currentsong.length / 60,
           currentsong_lengths=currentsong.length % 60,
           playlist=playlist)

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    print "Command: " + cmd
    print  query.mpd_query(cmd)
    return redirect(SELF_URL)

@app.route('/command/<cmd>/<arg>', methods=['POST'])
def command_arg(cmd, arg):
    query.mpd_query(cmd, arg)
    return redirect(SELF_URL)


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
    CONF_FILE = '/etc/mpd_wc/server.conf'
    optlist, args = getopt.getopt(sys.argv[1:], 'p:', ['pidfile=', 'config='])
    for opt,arg in optlist:
        if "--pidfile" == opt:
            PID=arg
        elif "--config" == opt:
            CONF_FILE=arg
    if PID is None:
        usage()
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.readfp(open(CONF_FILE))
    SELF_IP = config.get('WebServer','WEBSERVICE_IP')
    SELF_PORT = config.get('WebServer','WEBSERVICE_PORT')
    SELF_URL='http://' + SELF_IP + ':' + SELF_PORT + '/mpd/'
    MPD_IP = config.get('MPDServer','MPDSERVER_IP')
    MPD_PORT = config.get('MPDServer','MPDSERVER_PORT')

    signal.signal(signal.SIGINT, signal_handler)
    make_pid(pidfile=PID)
    app.debug = False
    app.run(host='0.0.0.0')
