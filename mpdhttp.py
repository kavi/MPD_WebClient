from flask import Flask, render_template, redirect, url_for
import logging
import socket
import sys
import os
import ConfigParser
import getopt
import signal
import query
import serverconf
import json

app = Flask(__name__)
conf = None
mpdQuery = query.Query()

LOGFORMAT = '%(asctime)-15s|%(levelname)-5s|%(message)s'

def run():
    app.debug = False
    app.run(host='0.0.0.0')

@app.errorhandler(500)
def internal_server_error(error):
    logger.exception('An internal error occurred.')
    return render_template('error.html', msg=str(error)), 500

@app.route('/mpd/')
def default():
    logger.debug("Querying mpd for playlist.")
    currentsong = mpdQuery.get_currentsong()
    playlist = mpdQuery.get_currentplaylist(currentsong.pos)
    allsongs = mpdQuery.get_all_songs()
    status = mpdQuery.get_status()
    currentsong.elapsed = status.elapsed
    return render_template('mpd.html',
                           status=status,
                           currentsong=currentsong,
                           currentsong_lengthm=currentsong.length / 60,
                           currentsong_lengths=currentsong.length % 60,
                           playlist=playlist,
                           allsongs=allsongs)

@app.route('/currentsong', methods=['GET'])
def get_currentsong():
    logger.debug("Get CurrentSong");
    currentsong = mpdQuery.get_currentsong()
    status = mpdQuery.get_status()
    currentsong.elapsed = status.elapsed
    currentsong.state = status.state
    return json.dumps(currentsong.__dict__)

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    logger.debug("Command: " + cmd)
    result = mpdQuery.mpd_query(cmd)
    logger.debug("Query result: " + result)
    return result

@app.route('/command/<cmd>/<arg>', methods=['POST'])
def command_arg(cmd, arg):
    r=mpdQuery.mpd_query(cmd, arg)
    return json.dumps(r);


def make_pid(pidfile):
    pid = str(os.getpid())

    if os.path.isfile(pidfile):
        logger.error("%s already exists, exiting" % pidfile)
        sys.exit(1)
    else:
        file(pidfile, 'w').write(pid)

def signal_handler(signal, frame):
    if os.path.isfile(PID):
        os.remove(PID)
    sys.exit(0)

def usage():
    print ("Usage: --pidfile=<pidfile> [--config=<config-file>]")

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

    logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
    logger = logging.getLogger('mpdhttp')


    signal.signal(signal.SIGINT, signal_handler)
    make_pid(pidfile=PID)
    conf = serverconf.Config()
    conf.ip = SELF_IP
    conf.port = SELF_PORT
    mpdQuery.mpd_ip = MPD_IP
    mpdQuery.mpd_port = int(MPD_PORT)
    run()
