#!/bin/bash
# Starts a virtual X display and serves it in the browser at http://localhost:6080/vnc.html

set -e

export DISPLAY=${DISPLAY:-:1}
RESOLUTION=${VNC_RESOLUTION:-1920x1080x24}

Xvfb "$DISPLAY" -screen 0 "$RESOLUTION" -nolisten tcp > /tmp/xvfb.log 2>&1 &

# Wait for the X socket to exist before starting anything that draws on it.
for _ in $(seq 1 50); do
    [ -e "/tmp/.X11-unix/X${DISPLAY#:}" ] && break
    sleep 0.1
done

fluxbox > /tmp/fluxbox.log 2>&1 &
x11vnc -display "$DISPLAY" -forever -shared -nopw -rfbport 5900 -quiet > /tmp/x11vnc.log 2>&1 &
websockify --web /usr/share/novnc 6080 localhost:5900 > /tmp/novnc.log 2>&1 &

echo "GUI available at http://localhost:6080/vnc.html"
