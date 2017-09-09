#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fmrx
# Generated: Sat Sep  9 14:49:15 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
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
from optparse import OptionParser
import osmosdr
import sip
import sys
import time
from lib import control
ctl = control.Control()


class fmRX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fmrx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fmrx")
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

        self.settings = Qt.QSettings("GNU Radio", "fmRX")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

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
        self._volume_range = Range(0, 100, 1, 1, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "volume", "counter_slider", float)
        self.top_layout.addWidget(self._volume_win)
        _ptl_check_box = Qt.QCheckBox("Mute")
        self._ptl_choices = {True: 0, False: 1}
        self._ptl_choices_inv = dict((v,k) for k,v in self._ptl_choices.iteritems())
        self._ptl_callback = lambda i: Qt.QMetaObject.invokeMethod(_ptl_check_box, "setChecked", Qt.Q_ARG("bool", self._ptl_choices_inv[i]))
        self._ptl_callback(self.ptl)
        _ptl_check_box.stateChanged.connect(lambda i: self.set_ptl(self._ptl_choices[bool(i)]))
        self.top_layout.addWidget(_ptl_check_box)
        self._freq_range = Range(88e6, 108e6, 100e3, 103.7e6, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency Slider", "counter_slider", float)
        self.top_layout.addWidget(self._freq_win)
        _swap___push_button = Qt.QPushButton("Switch to TX")
        self._swap___choices = {'Pressed': 1, 'Released': 0}
        _swap___push_button.pressed.connect(lambda: self.set_swap__(self._swap___choices['Pressed']))
        _swap___push_button.released.connect(lambda: self.set_swap__(self._swap___choices['Released']))
        self.top_layout.addWidget(_swap___push_button)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq, #fc
        	samp_in, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        
        self.qtgui_sink_x_1.enable_rf_freq(True)
        
        
          
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_in)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(int(10e6/chan_width), firdes.low_pass(
        	1, 10e6, 75e3, 25e3, firdes.WIN_HAMMING, 6.76))
        _die___push_button = Qt.QPushButton("GUI Kill")
        self._die___choices = {'Pressed': 1, 'Released': 0}
        _die___push_button.pressed.connect(lambda: self.set_die__(self._die___choices['Pressed']))
        _die___push_button.released.connect(lambda: self.set_die__(self._die___choices['Released']))
        self.top_layout.addWidget(_die___push_button)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.audio_stop = blocks.multiply_const_vff((ptl, ))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=480e3,
        	audio_decimation=10,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_in, analog.GR_COS_WAVE, 1000, 1, 0)

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
        event.accept()


    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_swap__(self):
        return self.swap__

    def set_swap__(self, swap__):
        ctl.kill(self)
        ctl.startTX()
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
        self.audio_stop.set_k((self.ptl, ))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_sink_x_1.set_frequency_range(self.freq, self.samp_in)

    def get_die__(self):
        return self.die__

    def set_die__(self, die__):
        ctl.kill(self)
        self.die__ = die__

    def get_chan_width(self):
        return self.chan_width

    def set_chan_width(self, chan_width):
        self.chan_width = chan_width


def main(top_block_cls=fmRX, options=None):

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
