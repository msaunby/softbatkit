#!/usr/bin/python
#
# Copyright 2018 Michael Saunby.
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This file derived from a GNU Radio example -
# Copyright 2012 Free Software Foundation, Inc.
# Distributed under GNU GPL3.
#

from gnuradio import gr, filter
from gnuradio import blocks, audio, analog, channels
import sys

try:
    from gnuradio import qtgui
    from PyQt4 import QtGui, QtCore
    import sip
except ImportError:
    sys.stderr.write("Error: Program requires PyQt4 and gr-qtgui.\n")
    sys.exit(1)


class dialog_box(QtGui.QWidget):
    def __init__(self, display, control):
        QtGui.QWidget.__init__(self, None)
        self.setWindowTitle('PyQt Test GUI')

        self.boxlayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
        self.boxlayout.addWidget(display, 1)
        self.boxlayout.addWidget(control)

        self.resize(800, 500)

class control_box(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Control Panel')

        self.setToolTip('Control the signals')
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))

        self.layout = QtGui.QFormLayout(self)

        self.quit = QtGui.QPushButton('Close', self)
        self.quit.setMinimumWidth(100)
        self.layout.addWidget(self.quit)

        self.connect(self.quit, QtCore.SIGNAL('clicked()'),
                     QtGui.qApp, QtCore.SLOT('quit()'))



class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        Rs = 100000
        npts = 2048

        #taps = filter.firdes.complex_band_pass_2(1, Rs, 1500, 2500, 100, 60)

        self.qapp = QtGui.QApplication(sys.argv)
        ss = open(gr.prefix() + '/share/gnuradio/themes/dark.qss')
        sstext = ss.read()
        ss.close()
        self.qapp.setStyleSheet(sstext)

        channel = channels.channel_model(0.01)
        thr = blocks.throttle(gr.sizeof_gr_complex, 100*npts)
        #filt = filter.fft_filter_ccc(1, taps)
        self.snk1 = qtgui.waterfall_sink_c(npts, filter.firdes.WIN_BLACKMAN_hARRIS,
                                           0, Rs,
                                           "Waterfall monitor", 2)

        float_to_complex = blocks.float_to_complex()

        input_rate = 96000
        #audio_input = "hw:Loopback,0,0"
        audio_input = "hw:PCH,0,0"
        src_audio = audio.source (input_rate, audio_input)
        self.connect((src_audio, 1), (float_to_complex, 0))
        self.connect((src_audio, 0), (float_to_complex, 1))

        self.connect(float_to_complex, channel, thr, (self.snk1, 0))
        #self.connect(thr, filt, (self.snk1, 1))
        self.connect(thr, (self.snk1, 1))

        self.ctrl_win = control_box()

        # Get the reference pointer to the SpectrumDisplayForm QWidget
        pyQt  = self.snk1.pyqwidget()

        # Wrap the pointer as a PyQt SIP object
        # This can now be manipulated as a PyQt4.QtGui.QWidget
        pyWin = sip.wrapinstance(pyQt, QtGui.QWidget)

        self.main_box = dialog_box(pyWin, self.ctrl_win)
        self.main_box.show()

if __name__ == "__main__":
    tb = my_top_block();
    tb.start()
    tb.qapp.exec_()
    tb.stop()
