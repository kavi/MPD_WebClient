#!/bin/bash
SERVICE="MPD WebClient"
DEFAULT_CONF=/etc/mpd_wc.conf
CONF_FILE=${2:-$DEFAULT_CONF}

do_start() {
  source ${CONF_FILE}
  VENV_BIN=${FLASK_HOME}/venv/bin
  WC_HOME=${FLASK_HOME}/mpdhttp
  . ${VENV_BIN}/activate
  python "${WC_HOME}/mpdhttp.py" "--pidfile=${PIDFILE}" "--config=${SERVERCONF}" &>> ${LOGFILE}
}

### main logic ###
case "$1" in
  start)
        do_start
        ;;
  *)
        echo $"Usage: $0 {start} <conf-file>"
        exit 1
esac
exit 0
