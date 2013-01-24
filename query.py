#!/usr/bin/python
import sys
import socket
import time
import model

MPD_IP='192.168.1.10'
MPD_PORT=6600
BUFFER_SIZE = 8192

def get_currentplaylist():
    str_play = mpd_query('playlistinfo')
    songs = []
    for line in str_play.split('\n'):
      if line.strip():
        v = line.strip().split(':')
        if v[0] == 'file':
            songs.append(model.MpdSong())
        else:
            set_songproperty(songs[len(songs) - 1], v)
    return songs

def set_songproperty(sng, v):
    if len(v) != 2:
        return
    value = v[1].strip().decode('utf-8')
    value = value.encode('ascii', 'xmlcharrefreplace')
    if v[0] == 'Artist':
        sng.artist = value
    elif v[0] == 'Album':
        sng.album = value
    elif v[0] == 'Title':
        sng.title = value
    elif v[0] == 'Track':
        sng.trackno = value
    elif v[0] == 'Time':
        sng.length = int(value)
    elif v[0] == 'Genre':
        sng.genre = value
    elif v[0] == 'Date':
        sng.date = value
    elif v[0] == 'Pos':
        sng.pos = value
#    else:
#       print v[0]+ ":" + v[1] + " - not supported"


def get_currentsong():
    str_song = mpd_query('currentsong')
    sng = model.MpdSong()
    for line in str_song.split('\n'):
      if line.strip():
        v = line.strip().split(':')
        set_songproperty(sng, v)
#    if sng.title == '':
#        return []
    return sng

def get_status():
    str_status = mpd_query('status')
    stat = model.MpdStatus()
    for line in str_status.split('\n'):
      if line.strip():
        v = line.strip().split(':')
        if v[0] == 'volume':
          stat.volume = int(v[1])
        elif v[0] == 'elapsed':
          stat.elapsed = float(v[1])
        elif v[0] == 'state':
          stat.state = v[1].strip()
#        else:
#          if len(v) == 2:
#            break
#            print v[0]+ ":" + v[1] + " - not supported"
    return stat


def mpd_query(command, arg=''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((MPD_IP, MPD_PORT))
    sock.setblocking(0)

    request = command
    if not arg == '':
        request += ' ' + arg
    request += '\n'
    if handshake(sock):
        sock.send(request)
	response = recv_timeout(sock)
    else:
        print "Failed to connect."

    sock.close()
    return response
    

def is_done(data):
    return data.endswith('\nOK\n')

def handshake_done(data):
    return data.startswith('OK')

def recv_timeout(the_socket,finish=is_done,timeout=1):
    total_data=[];data='';begin=time.time()
    done=0
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout: 
            break
        #if done
        elif done:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break
        try:
            data=the_socket.recv(BUFFER_SIZE)
            if data:
                total_data.append(data)
                if finish(data):
                    done=1
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)


def handshake(sock):
    data = recv_timeout(sock,handshake_done)
    return data.startswith('OK')

if __name__ == '__main__':
#    print mpd_query(sys.argv[1])
    print get_currentsong()
    print get_status()
    for i in get_currentplaylist():
        print i
