#!/usr/bin/env python

from sys import argv
import numpy as np
import struct
import wave

FORMAT_CHARACTERS = {'2': 'h'}


def split_into_windows_by_framerate(frames, framerate, num_of_frames, sample_width, channels):
    windows = []
    format_character = FORMAT_CHARACTERS[str(sample_width)]

    frames_iterator = struct.iter_unpack(format_character, frames)

    for window in range(num_of_frames//framerate):
        frames = []
        for frame in range(framerate):
            data = 0
            for i in range(channels):
                data += next(frames_iterator)[0]
            data /= channels
            frames.append(data)
        windows.append(frames)

    return windows


def transform_and_evaluate_window(window, highest_peak, lowest_peak):
    new_highest_peak, new_lowest_peak = highest_peak, lowest_peak

    transformed_window = np.fft.rfft(window)
    amplitudes = np.absolute(transformed_window)
    average = np.average(amplitudes)

    for frequency, amplitude in enumerate(amplitudes):
        if amplitude >= 20 * average:
            if frequency < new_lowest_peak:
                new_lowest_peak = frequency
            if frequency > new_highest_peak:
                new_highest_peak = frequency

    return new_highest_peak, new_lowest_peak


def format_output(highest_peak, lowest_peak):
    for val in np.isinf((highest_peak, lowest_peak,)):
        if val:
            return 'no peaks'
    return 'low: {}, high: {}'.format(lowest_peak, highest_peak)


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    input_file = argv[1]

    highest_peak = -np.inf
    lowest_peak = np.inf

    with wave.open(input_file, 'rb') as file:
        channels = file.getnchannels()
        framerate = file.getframerate()
        sample_width = file.getsampwidth()
        num_of_frames = file.getnframes()
        frames = file.readframes(num_of_frames)

        windows_by_framerate = split_into_windows_by_framerate(frames, framerate, num_of_frames, sample_width, channels)

        for window in windows_by_framerate:
            highest_peak, lowest_peak = transform_and_evaluate_window(window, highest_peak, lowest_peak)

        print(format_output(highest_peak, lowest_peak))

        file.close()


if __name__ == '__main__':
    main()
