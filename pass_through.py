#!/usr/bin/env python
#


from gnuradio import gr
from gnuradio import audio, analog, blocks
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

       # osc = analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, options.frequency, ampl)
        src = audio.source (sample_rate, options.audio_input)
       # mixer = blocks.multiply_ff ()
       # self.connect (osc, (mixer, 0))
       # self.connect (src, (mixer, 1))
        dst = audio.sink (sample_rate, options.audio_output, True)
        self.connect (src, dst)


if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
