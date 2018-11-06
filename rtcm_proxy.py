#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import socket
import signal
import time # XXX

import proto

termRequest = False

def terminateHandler(signum, frame):
    global termRequest
    print('Termination requested')
    termRequest = True

def runRtcmServer(hub, address='0.0.0.0', port=10081):
    global termRequest
    signal.signal(signal.SIGINT, terminateHandler)

    try:
        sock = socket.socket()
        sock.bind((address, port))
        print('Listening for connections...')
        sock.listen(1)
        conn, addr = sock.accept()
        print('Connection from {:s}:{:d}'.format(*addr))
        ublox = hub['Ublox']
    except:
        return

    while not termRequest:
        data = conn.recv(256)
        if not data:
            break
        while len(data) > 0:
            length = min(len(data), 32)
            chunk = data[:length]
            data = data[length:]
            packet = {'id': proto.Message.COMPONENT_RAW_DATA, 'component': ublox.address, 'payload': chunk}
            hub.messenger.invokeAsync(packet=packet, callback=None)

    conn.close()

args = argparse.ArgumentParser()
args.add_argument('--serial', dest='serial', help='serial port name', default='')
args.add_argument('--baudrate', dest='baudrate', help='serial port baud rate', type=int, default=57600)
args.add_argument('--address', dest='address', help='server address', default='')
args.add_argument('--modem', dest='modem', help='modem socket', default='1:2')
args.add_argument('--cache', dest='cache', help='component cache directory', default='cache')
args.add_argument('-d', dest='debug', help='enable debug messages', default=False, action='store_true')
args.add_argument('-v', dest='verbose', help='enable verbose mode', default=False, action='store_true')
options = args.parse_args()

proto.debugEnabled, proto.verboseEnabled = options.debug, options.verbose

if options.serial != '' and options.address != '':
    print('Only one connection type can be specified')
    raise Exception()
elif options.serial != '':
    stream = proto.SerialStream(options.serial, options.baudrate)
elif options.address != '':
    try:
        parts = options.address.split(':')
        if len(parts) == 1:
            address, port = parts[0], 5500
        else:
            address, port = parts[0], int(parts[1])
        parts = options.modem.split(':')
        modemAddress, modemPort = int(parts[0]), int(parts[1])

        stream = proto.NetworkStream(address, port, modemAddress, modemPort)
    except:
        print('Incorrect arguments')
        exit()
else:
    print('No connection type specified')
    raise Exception()

messenger = proto.Messenger(stream, options.cache)
messenger.connect()
#messenger.hub.connectAsync()
time.sleep(2)

ublox = messenger.hub['Ublox']
if ublox is not None:
    runRtcmServer(messenger.hub)
else:
    print('Ublox not found')
messenger.stop()
