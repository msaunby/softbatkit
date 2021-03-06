#!/usr/bin/env python
#
# Generate an pulsing ultrasound tone using the default or user specified output device.
# To discover what output devices are availble specify a nonexistant device, e.g.
# ultra_tone.py -O qwerty
#
# Specify tone frequency with -f freg_in_hz  e.g. -f 60000
# The default is 1000 which is an audible tone - just so we know the program runs.
#
# To be able to generate an ultrasound tone the output device should ideally support
# a sample rate of 88200 or better.  Typical rates are 88200, 96000, and 192000.
# Some sound cards are only capable of 44100 samples/second in which case the
# maximum output frequency will be 22kHz. This is above human hearing range so
# can be used for some test purposes, but a high speed sound card can do much
# better.
#
# Michael Saunby. June 2012

from gnuradio import gr
from gnuradio import audio, analog, blocks
from gnuradio.eng_option import eng_option
from optparse import OptionParser


class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option)
        parser.add_option("-O", "--audio-output", type="string", default="",
                          help="pcm output device name")
        parser.add_option("-r", "--sample-rate", type="eng_float", default=192000,
                          help="set sample rate to RATE (192000)")
        parser.add_option("-f", "--frequency", type="eng_float", default=81000)
        parser.add_option("-a", "--amplitude", type="eng_float", default=0.5)

        (options, args) = parser.parse_args ()
        if len(args) != 0:
            parser.print_help()
            raise SystemExit, 1

        sample_rate = int(options.sample_rate)
        ampl = float(options.amplitude)
        pulse_freq = 1.0 # 1Hz
        pulse_dc = 0.1 # Low DC value to give high/low value rather than on/off
        if ampl > 1.0: ampl = 1.0

        osc = analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, options.frequency, ampl)
        osc2 =  analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, 80000, .5)
        mixer = blocks.multiply_ff ()
        self.connect (osc, (mixer, 0))
        self.connect (osc2, (mixer, 1))
        dst = audio.sink (sample_rate, options.audio_output, True)
        self.connect (mixer, dst)


if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
