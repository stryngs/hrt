#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Fmrx
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip



class fmRX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fmrx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fmrx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fmRX")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.swap__ = swap__ = 0
        self.samp_in = samp_in = 10e6
        self.ptl = ptl = 1
        self.freq = freq = 103.7e6
        self.die__ = die__ = 0
        self.chan_width = chan_width = 200e3

        ##################################################
        # Blocks
        ##################################################

        self._volume_range = qtgui.Range(0, 100, 1, 1, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        _ptl_check_box = Qt.QCheckBox("Mute")
        self._ptl_choices = {True: 0, False: 1}
        self._ptl_choices_inv = dict((v,k) for k,v in self._ptl_choices.items())
        self._ptl_callback = lambda i: Qt.QMetaObject.invokeMethod(_ptl_check_box, "setChecked", Qt.Q_ARG("bool", self._ptl_choices_inv[i]))
        self._ptl_callback(self.ptl)
        _ptl_check_box.stateChanged.connect(lambda i: self.set_ptl(self._ptl_choices[bool(i)]))
        self.top_layout.addWidget(_ptl_check_box)
        self._freq_range = qtgui.Range(88e6, 108e6, 100e3, 103.7e6, 200)
        self._freq_win = qtgui.RangeWidget(self._freq_range, self.set_freq, "Frequency Slider", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_win)
        _swap___push_button = Qt.QPushButton('Switch to TX')
        _swap___push_button = Qt.QPushButton('Switch to TX')
        self._swap___choices = {'Pressed': 1, 'Released': 0}
        _swap___push_button.pressed.connect(lambda: self.set_swap__(self._swap___choices['Pressed']))
        _swap___push_button.released.connect(lambda: self.set_swap__(self._swap___choices['Released']))
        self.top_layout.addWidget(_swap___push_button)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_in, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_in)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            (int(10e6/chan_width)),
            firdes.low_pass(
                1,
                10e6,
                75e3,
                25e3,
                window.WIN_HAMMING,
                6.76))
        _die___push_button = Qt.QPushButton('GUI Kill')
        _die___push_button = Qt.QPushButton('GUI Kill')
        self._die___choices = {'Pressed': 1, 'Released': 0}
        _die___push_button.pressed.connect(lambda: self.set_die__(self._die___choices['Pressed']))
        _die___push_button.released.connect(lambda: self.set_die__(self._die___choices['Released']))
        self.top_layout.addWidget(_die___push_button)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.audio_stop = blocks.multiply_const_ff(ptl)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=480e3,
        	audio_decimation=10,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_in, analog.GR_COS_WAVE, 1000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_stop, 0))
        self.connect((self.audio_stop, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_wfm_rcv_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fmRX")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)

    def get_swap__(self):
        return self.swap__

    def set_swap__(self, swap__):
        self.swap__ = swap__

    def get_samp_in(self):
        return self.samp_in

    def set_samp_in(self, samp_in):
        self.samp_in = samp_in
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_in)
        self.osmosdr_source_0.set_sample_rate(self.samp_in)
        self.qtgui_sink_x_1.set_frequency_range(self.freq, self.samp_in)

    def get_ptl(self):
        return self.ptl

    def set_ptl(self, ptl):
        self.ptl = ptl
        self._ptl_callback(self.ptl)
        self.audio_stop.set_k(self.ptl)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_sink_x_1.set_frequency_range(self.freq, self.samp_in)

    def get_die__(self):
        return self.die__

    def set_die__(self, die__):
        self.die__ = die__

    def get_chan_width(self):
        return self.chan_width

    def set_chan_width(self, chan_width):
        self.chan_width = chan_width




def main(top_block_cls=fmRX, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
