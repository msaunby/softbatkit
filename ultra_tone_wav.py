#!/usr/bin/env python
#

from gnuradio import gr
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
import time

class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)


        frequency = 57000
        sample_rate = 500000
        ampl = 0.8


        src0 = analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, frequency, ampl)
        dst = blocks.wavfile_sink ("sample_57k_sin.wav", 1, sample_rate)
        self.connect (src0, dst)

if __name__ == '__main__':
    try:
        tb =  my_top_block()
        tb.start()
        time.sleep(5.0)
        tb.stop()
    except KeyboardInterrupt:
        pass
