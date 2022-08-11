#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fmtx
# Generated: Sat Sep  9 14:49:16 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget

from gnuradio.fft import window

from optparse import OptionParser
import osmosdr
import sip
import sys
import time
from lib import control
ctl = control.Control()


class fmTX(gr.top_block, Qt.QWidget):

    def __init__(self, control):
        self.ctl = control
        gr.top_block.__init__(self, "Fmtx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fmtx")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "fmTX")
        # self.restoreGeometry(self.settings.value("geometry").toByteArray())
        ## try bytes(foo) rather than foo.toByteArray()

        ##################################################
        # Variables
        ##################################################
        self.swap__ = swap__ = 0
        self.samp_rate = samp_rate = 1.323e6
        self.ptt = ptt = 0
        self.freq = freq = 103.7e6
        self.die__ = die__ = 0
        self.audio_samp_in = audio_samp_in = 44100

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate_range = Range(0, 6.00e6, 1, 1.323e6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "Sample Rate Slider", "counter_slider", float)
        self.top_layout.addWidget(self._samp_rate_win)
        _ptt_push_button = Qt.QPushButton("ptt")
        self._ptt_choices = {'Pressed': 1, 'Released': 0}
        _ptt_push_button.pressed.connect(lambda: self.set_ptt(self._ptt_choices['Pressed']))
        _ptt_push_button.released.connect(lambda: self.set_ptt(self._ptt_choices['Released']))
        self.top_layout.addWidget(_ptt_push_button)
        self._freq_range = Range(88e6, 108e6, 100e3, 103.7e6, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency Slider", "counter_slider", float)
        self.top_layout.addWidget(self._freq_win)
        _swap___push_button = Qt.QPushButton("Switch to RX")
        self._swap___choices = {'Pressed': 1, 'Released': 0}
        _swap___push_button.pressed.connect(lambda: self.set_swap__(self._swap___choices['Pressed']))
        _swap___push_button.released.connect(lambda: self.set_swap__(self._swap___choices['Released']))
        self.top_layout.addWidget(_swap___push_button)
        # self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
        #         interpolation=10,
        #         decimation=1,
        #         taps=None,
        #         fractional_bw=None,
        # )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=10,
                decimation=1
        )
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	# firdes.WIN_BLACKMAN_hARRIS, #wintype
            window.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(True)



        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(14, 0)
        self.osmosdr_sink_0.set_if_gain(47, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        _die___push_button = Qt.QPushButton("GUI Kill")
        self._die___choices = {'Pressed': 1, 'Released': 0}
        _die___push_button.pressed.connect(lambda: self.set_die__(self._die___choices['Pressed']))
        _die___push_button.released.connect(lambda: self.set_die__(self._die___choices['Released']))
        self.top_layout.addWidget(_die___push_button)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((ptt, ))
        self.audio_source_0 = audio.source(44100, "", True)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=audio_samp_in,
        	quad_rate=audio_samp_in * 3,
        	tau=75e-6,
        	max_dev=75e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.audio_source_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fmTX")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_swap__(self):
        return self.swap__

    def set_swap__(self, swap__):
        self.ctl.kill(self)
        self.ctl.startRX()
        self.swap__ = swap__

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_ptt(self):
        return self.ptt

    def set_ptt(self, ptt):
        self.ptt = ptt
        self.blocks_multiply_const_vxx_0.set_k((self.ptt, ))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)

    def get_die__(self):
        return self.die__

    def set_die__(self, die__):
        self.ctl.kill(self)
        self.die__ = die__

    def get_audio_samp_in(self):
        return self.audio_samp_in

    def set_audio_samp_in(self, audio_samp_in):
        self.audio_samp_in = audio_samp_in


def main(top_block_cls=fmTX, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
