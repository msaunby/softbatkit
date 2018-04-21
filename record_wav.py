
from gnuradio import gr
from gnuradio import audio
from gnuradio import blocks
from gnuradio.eng_option import eng_option
from optparse import OptionParser

class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        usage="%prog: [options] output_filename"
        parser = OptionParser(option_class=eng_option, usage=usage)
        parser.add_option("-I", "--audio-input", type="string", default="",
                          help="pcm input device name.  E.g., hw:0,0 or /dev/dsp")
        parser.add_option("-r", "--sample-rate", type="eng_float", default=48000,
                          help="set sample rate to RATE (48000)")
        parser.add_option("-N", "--nsamples", type="eng_float", default=None,
                          help="number of samples to collect [default=+inf]")

        (options, args) = parser.parse_args ()
        if len(args) != 1:
            parser.print_help()
            raise( SystemExit, 1 )
        filename = args[0]

        sample_rate = int(options.sample_rate)
        src = audio.source (sample_rate, options.audio_input)
        dst = blocks.wavfile_sink (filename, 1, sample_rate)

        if options.nsamples is None:
            self.connect((src, 0), dst)
        else:
            head = blocks.head(gr.sizeof_float, int(options.nsamples))
            self.connect((src, 0), head, dst)


if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
