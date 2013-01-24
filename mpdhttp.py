from flask import Flask, render_template, redirect, url_for
import traceback
import socket
import sys
import os
import ConfigParser
import getopt
import signal
import query
import serverconf

app = Flask(__name__)
conf = None
mpdQuery = query.Query()


def run():
    app.debug = False
    app.run(host='0.0.0.0')

@app.route('/mpd/')
def default():
    try:
        currentsong = mpdQuery.get_currentsong()
        playlist = mpdQuery.get_currentplaylist()
        return render_template('mpd.html',
               currentsong=currentsong,
               currentsong_lengthm=currentsong.length / 60,
               currentsong_lengths=currentsong.length % 60,
               playlist=playlist)
    except:
        traceback.print_exc()

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    print "Command: " + cmd
    print  mpdQuery.mpd_query(cmd)
    return redirect(conf.url)

@app.route('/command/<cmd>/<arg>', methods=['POST'])
def command_arg(cmd, arg):
    mpdQuery.mpd_query(cmd, arg)
    return redirect(conf.url)


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
    print "Usage: --pidfile=<pidfile> [--config=<config-file>]"

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
    conf = serverconf.Config()
    conf.ip = SELF_IP
    conf.port = SELF_PORT
    mpdQuery.mpd_ip = MPD_IP
    mpdQuery.mpd_port = int(MPD_PORT)
    run()
