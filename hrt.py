#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import sys
from PyQt5 import Qt
from distutils.version import StrictVersion
from gnuradio import analog, audio, blocks, eng_notation, filter, gr, qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
from shlex import split
import fcntl, os, osmosdr, sip, subprocess, sys, time

## USER DEFINED LIBS, here for clarity purposes
from lib import control, fmRX, fmTX


def choose(choice):
    """Actions taken by user input"""
    global initLaunch
    global PROC

    if (choice == '1' or choice == '2') and initLaunch == 1:
        ctl.kill(PROC)
    if initLaunch == 0 and (choice == '1' or choice == '2'):
        initLaunch = 1

    if choice == '1':
        PROC = ctl.startTX()
    elif choice == '2':
        PROC = ctl.startRX()
    elif choice == '3':
        ctl.kill(PROC)


def menu():
    """stdout for the menu"""
    print('\n1 - Send')
    print('2 - Receive')
    print('3 - Reset')
    print('4 - Quit\n')
    return ''


if __name__ == '__main__':

    ## Bring in the pre-built GRC flow pre-reqs
    x11 = ctypes.cdll.LoadLibrary('libX11.so')
    x11.XInitThreads()
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        # Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    ## Keep track of user actions
    initLaunch = 0
    PROC = ''

    ## Load our control module
    ctl = control.Control(rx = fmRX, tx = fmTX)

    ## Launcher
    while True:
        uChoice = input(menu())
        if uChoice == '4':
            ctl.kill(PROC)
            break
            sys.exit(0)
        else:
            choose(uChoice)
    sys.exit(0)
