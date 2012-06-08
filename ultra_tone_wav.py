#!/usr/bin/env python
# 

from gnuradio import gr

class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)


        frequency = 57000
        sample_rate = 500000
        ampl = 0.8


        src0 = gr.sig_source_f (sample_rate, gr.GR_SIN_WAVE, frequency, ampl)
        # use 'head' to stop block running after 10 seconds 
        head = gr.head(gr.sizeof_float, sample_rate*10)
        dst = gr.wavfile_sink ("sample_57k_sin.wav", 1, sample_rate)
        self.connect (src0, head, dst)


if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
