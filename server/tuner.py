#!/usr/bin/env python
# bat detector tuner

# Decode IQ stream(s) and convert to audio stream with tuneable frequency shift.

from gnuradio import gr
from gnuradio import audio, analog, blocks, filter


class tuner_top_block(gr.top_block):

    def __init__(self, audio_input, input_rate, audio_output, output_rate, frequency=55000, ampl=1.0):
        gr.top_block.__init__(self)

        if ampl > 1.0: ampl = 1.0

        to_real = blocks.complex_to_real()
        to_imag = blocks.complex_to_imag()
        float_to_complex = blocks.float_to_complex()

        src = audio.source (input_rate, audio_input)
        firdes_taps = filter.firdes.low_pass_2(1, 1, 0.2, 0.1, 60)
        self._converter = filter.freq_xlating_fir_filter_ccf ( 1, firdes_taps, 0, input_rate )
        self._converter.set_center_freq(frequency)
        dst = audio.sink (output_rate, audio_output, True)

        #self.connect(src, converter, to_real, dst)
        self.connect((src, 1), (float_to_complex, 0))
        self.connect((src, 0), (float_to_complex, 1))
        self.connect(float_to_complex, self._converter)
        self.connect(self._converter, to_real, (dst,0))
        self.connect(self._converter, to_imag, (dst,1))

    def set_freq(self, f):
        self._converter.set_center_freq(f)

if __name__ == '__main__':
    try:
        loop_in = "hw:Loopback,0,0"  # The other side of this device is hw:Loopback,1,0
        loop_out = "hw:Loopback,1,1" # The other side of this device is hw:Loopback,0,1
        tb = tuner_top_block( loop_in, 96000, loop_out, 48000, 55000, 1.0)
        tb.start()
        resp = raw_input("quit now? ")
        tb.stop()

    except KeyboardInterrupt:
        pass
