#!/usr/bin/env python
#


from gnuradio import gr
from gnuradio import audio, analog, blocks, filter
from gnuradio.eng_option import eng_option
from optparse import OptionParser


class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option)
        parser.add_option("-I", "--audio-input", type="string", default="",
                          help="pcm input device name.  E.g., hw:0,0 or /dev/dsp")
        parser.add_option("-O", "--audio-output", type="string", default="",
                          help="pcm output device name")
        parser.add_option("-r", "--sample-rate", type="eng_float", default=192000,
                          help="set sample rate to RATE (192000)")
        parser.add_option("-f", "--frequency", type="eng_float", default=45000)
        parser.add_option("-a", "--amplitude", type="eng_float", default=0.5)

        (options, args) = parser.parse_args ()
        if len(args) != 0:
            parser.print_help()
            raise SystemExit, 1

        sample_rate = int(options.sample_rate)
        ampl = float(options.amplitude)
        if ampl > 1.0: ampl = 1.0

        to_real = blocks.complex_to_real()
        to_imag = blocks.complex_to_imag()

        src = audio.source (sample_rate, options.audio_input)
        firdes_taps = filter.firdes.low_pass_2(1, 1, 0.2, 0.1, 60)
        converter = filter.freq_xlating_fir_filter_fcf ( 1, firdes_taps, 0, sample_rate )
        converter.set_center_freq(0 - options.frequency)
        dst = audio.sink (sample_rate, options.audio_output, True)

        #self.connect(src, converter, to_real, dst)
        self.connect(src, converter)
        self.connect(converter, to_real, (dst,0))
        self.connect(converter, to_imag, (dst,1))
if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
