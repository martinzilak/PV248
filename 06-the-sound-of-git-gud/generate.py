# stolen from http://code.activestate.com/recipes/578168-sound-generator-using-wav-file/
# generate wav file containing sine waves
# FB36 - 20120617
import math, wave, array
for a in range(20, 460, 20):
    for j in range(1, 3):
        duration = 4 # seconds
        freq = a # of cycles per second (Hz) (frequency of the sine waves)
        volume = 100 # percent
        data = array.array('h') # signed short integer (-32768 to 32767) data
        sampleRate = 44100 # of samples per second (standard)
        numChan = j # of channels (1: mono, 2: stereo)
        dataSize = 2 # 2 bytes because of using signed short integers => bit depth = 16
        numSamplesPerCyc = int(sampleRate / freq)
        numSamples = sampleRate * duration
        for i in range(numSamples):
            sample = 32767 * float(volume) / 100
            sample *= math.sin(math.pi * 2 * (i % numSamplesPerCyc) / numSamplesPerCyc)
            data.append(int(sample))
        f = wave.open('samples/' + str(freq) + 'hz_' + ('mono' if numChan == 1 else 'stereo') + '.wav', 'w')
        f.setparams((numChan, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
        f.writeframes(data.tostring())
        f.close()