#!/usr/bin/env python
#
# Resample a high speed recording, default 500k samples per second, to a lower rate, 
# default 192k. 192k is supported by some sound cards, others might support 88200.
# Caution, resampling to a lower rate, such as the industry standard 44100 will
# lose all ultra-sonic content.
# The highest frequency retained will be f/2.  i.e. 96KHz for a sample rate of 192k.
#
#
# A high-pass filter is optionally applied to remove all audible sounds, though this may
# not be completely effective if the input file is clipped, i.e. signals that reach maximum 
# value at their peak.  
#
# Michael Saunby. June 2012.
# 

from gnuradio import gr, gru, blks2
from gnuradio import audio
from gnuradio.eng_option import eng_option
from optparse import OptionParser
from numpy import convolve, array


class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option)
        parser.add_option("-I", "--filename", type="string", help="read input from wav FILE")
        parser.add_option("-s", "--input-rate", type="eng_float", default="500k",
                          help="set sample rate to RATE (500k)")
        parser.add_option("-O", "--outname", type="string", help="output to wav file FILE")
        parser.add_option("-r", "--output-rate", type="eng_float", default="192k",
                          help="set output sample rate to RATE (192k)")
        parser.add_option("-F", "--filter", action="store_true", default=False,
                          help="filter out audible sounds, retain ultrasonic")
        (options, args) = parser.parse_args()
        if len(args) != 0:
            parser.print_help()
            raise SystemExit, 1


        src = gr.wavfile_source (options.filename)

        input_rate = int(options.input_rate)
        output_rate = int(options.output_rate) 
        interp = gru.lcm(input_rate, output_rate) / input_rate
        decim = gru.lcm(input_rate, output_rate) / output_rate

        dst = gr.wavfile_sink (options.outname, 1, output_rate)

        rr = blks2.rational_resampler_fff(int(interp), int(decim))

        if options.filter:
            highpass = gr.firdes.high_pass (1,                # gain
                                  output_rate,            # sampling rate
                                  15000,               # cutoff freq
                                  2000,                # width of trans. band
                                  gr.firdes.WIN_HANN) # filter type
            filt = gr.fir_filter_fff(1,highpass)
            self.connect (src, rr, filt, dst)
        else:
            self.connect (src, rr, dst)

if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
