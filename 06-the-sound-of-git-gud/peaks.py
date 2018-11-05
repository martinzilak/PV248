#!/usr/bin/env python

from sys import argv
import numpy as np
import struct
import wave

FORMAT_CHARACTERS = {'2': 'h'}


def split_into_windows(frames, num_of_frames, sample_width, channels):
    windows = []
    format_character = FORMAT_CHARACTERS[str(sample_width)]

    frames_iterator = struct.iter_unpack(format_character, frames)

    for frame in range(num_of_frames):
        data = 0
        for i in range(channels):
            data += next(frames_iterator)[0]
        data /= channels
        windows.append(data)

    return windows


def analyze_window(window, high, low):
    pass


def format_output(high, low):
    for val in np.isinf((high, low,)):
        if not val:
            return 'no peaks'
    return 'low: {}, high: {}'.format(low, high)


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    input_file = argv[1]

    high = np.inf
    low = -np.inf

    with wave.open(input_file, 'rb') as file:
        channels = file.getnchannels()
        framerate = file.getframerate()
        sample_width = file.getsampwidth()
        num_of_frames = file.getnframes()
        frames = file.readframes(num_of_frames)

        # print(channels, framerate, sample_width, num_of_frames)
        # python peaks.py samples/20_hz_mono.wav
        # 1 44100 2 176400
        # python peaks.py samples/20_hz_stereo.wav
        # 2 44100 2 88200

        windows = split_into_windows(frames, num_of_frames, sample_width, channels)

        for window in windows:
            analyze_window(window, high, low)

        print(format_output(high, low))

        file.close()


if __name__ == '__main__':
    main()
