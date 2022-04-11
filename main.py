#Completely stole all this from drew

#from scipy.io.wavfile import write
import soundfile as sf
import multiprocessing as mp
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np


def rec_audio(frames, which_device, storage_array, channel):
    print("in device" + str(which_device) + "\n")
    data = sd.rec(frames, device=which_device, channels=channel, samplerate=44100)
    sd.wait()
    storage_array.put(data)


def shift(arr, num, fill_value):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


def trim(handheld_rec_array):
    array_size = len(handheld_rec_array)
    begin_interest = 0
    while handheld_rec_array[begin_interest, 0] <= 0.01 and handheld_rec_array[begin_interest, 1] <= 0.01:
        begin_interest += 1

    if begin_interest < 10000:
        begin_interest = 0
    else:
        begin_interest -= 10000

    end_interest = array_size
    while handheld_rec_array[end_interest - 1, 0] <= 0.01 and handheld_rec_array[end_interest - 1, 1] <= 0.01:
        end_interest -= 1

    if end_interest > array_size - 10000:
        end_interest = array_size
    else:
        end_interest += 10000

    return begin_interest, end_interest


def smooth(array, window):
    if window % 2 == 0:
        window += 1
    retval = array
    window_div_2 = window // 2
    window_array = np.array
    for ii in range(window_div_2 - 1):
        window_array.append(0)
    window_array.append(array[:window_div_2])
    for ii in array[:]:
        window_array.roll()
        window_array[window] = array[ii + window_div_2]
        array[ii] = np.mean(window_array)
    return retval


if __name__ == '__main__':
    # mp.set_start_method('fork')
    recordings = mp.Queue()
    seconds = 10
    sampleRate = 44100
    handheldProcess = mp.Process(target=rec_audio, args=(int(seconds * sampleRate), 1, recordings, 2))
    webcamProcess = mp.Process(target=rec_audio, args=(int(seconds * sampleRate), 1, recordings, 1))

    handheldProcess.start()
    # webcamProcess.start()
    print("Recording audio...")
    handheldProcess.join(15)
    handheldRecArray = recordings.get()
    #shift to simulate multiple mics
    handheldRecArray[:, 1] = shift(handheldRecArray[:, 1], sampleRate, 0)
    # sf.write('TwoChannelStereo.wav', handheldRecArray, sampleRate)  # Save as WAV file
    # webcamProcess.join(1)
    # webcamRecArray = recordings.get()
    # sf.write('OneChannelMono.wav', webcamRecArray, sampleRate)  # Save as WAV file
    # print("Finished Recording.")
    #
    # #sf.read reads the same number of channels as the array
    # MonoSourceStereoOutput = sf.read('OneChannelMono.wav', always_2d=True)
    # StereoSourceStereoOutput = sf.read('TwoChannelStereo.wav')
    #
    # MonoSourceStereoOutput = np.array(MonoSourceStereoOutput)
    # StereoSourceStereoOutput = np.array(StereoSourceStereoOutput)
    # print(MonoSourceStereoOutput)
    # print(StereoSourceStereoOutput)
    #
    # plt.title("Channel 1 Stereo")
    # plt.plot(StereoSourceStereoOutput[:0], color="red")
    #
    # plt.show()
    #
    # plt.title("Channel 2 Stereo")
    # plt.plot(StereoSourceStereoOutput[:1], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 1 Mono")
    # plt.plot(MonoSourceStereoOutput[:0], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 2 Mono")
    # plt.plot(MonoSourceStereoOutput[:1], color="red")
    # #
    # plt.show()


    # np.set_printoptions(precision=3)
    # print("Original Size: " + str(handheldRecArray.size))
    # print(str(handheldRecArray.ndim))
    # print (handheldRecArray)
    #
    # newArray = np.array(handheldRecArray)
    # x = seconds
    # y = handheldRecArray
    #
    noise = np.random.normal(0, .001, handheldRecArray.shape)
    new_signal = handheldRecArray + noise
    noise2 = np.random.normal(0, .0002, handheldRecArray.shape)
    new_signal2 = handheldRecArray + noise2
    noise3 = np.random.normal(0, .0003, handheldRecArray.shape)
    new_signal3 = handheldRecArray + noise3
    #sf.write('OneChannelMono.wav', webcamProcess, sampleRate)  # Save as WAV file

    #how to print
    #when doing multi channel stuff
    plt.title("Channel 1 No noise")
    plt.plot(handheldRecArray[:, 0], color="red")
    #
    plt.show()

    plt.title("Channel 2 No noise")
    plt.plot(handheldRecArray[:, 1], color="red")
    #
    plt.show()

    handheldRecArray[:, 0] = smooth(handheldRecArray[:, 0], 7)
    handheldRecArray[:, 1] = smooth(handheldRecArray[:, 1], 7)

    plt.title("Channel 1 No noise")
    plt.plot(handheldRecArray[:, 0], color="red")
    #
    plt.show()

    plt.title("Channel 2 No noise")
    plt.plot(handheldRecArray[:, 1], color="red")
    #
    plt.show()

    # plt.title("Channel 1 With Noise")
    # plt.plot(new_signal[:, 0], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 2 With noise")
    # plt.plot(new_signal[:, 1], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 1 With Noise")
    # plt.plot(new_signal2[:, 0], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 2 With noise")
    # plt.plot(new_signal2[:, 1], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 1 With Noise")
    # plt.plot(new_signal3[:, 0], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 2 With noise")
    # plt.plot(new_signal3[:, 1], color="red")
    # #
    # plt.show()

    beginInterest, endInterest = trim(new_signal)

    plt.title("Channel 1 No noise")
    plt.plot(new_signal[beginInterest:endInterest, 0], color="red")
    #
    plt.show()

    plt.title("Channel 2 No noise")
    plt.plot(new_signal[beginInterest:endInterest, 1], color="red")
    #
    plt.show()
    # beginInterest = 0
    # while handheldRecArray[beginInterest, 0] <= 0.01 and handheldRecArray[beginInterest, 1] <= 0.01:
    #     beginInterest += 1
    #
    # if beginInterest < 10000:
    #     beginInterest = 0
    # else:
    #     beginInterest -= 10000
    #
    # endInterest = int(seconds * sampleRate)
    # while handheldRecArray[endInterest - 1, 0] <= 0.01 and handheldRecArray[endInterest - 1, 1]:
    #     endInterest -= 1
    #
    # if endInterest > int(seconds * sampleRate) - 10000:
    #     endInterest = int(seconds * sampleRate)
    # else:
    #     endInterest += 10000
    #
    # plt.title("Channel 1 No noise")
    # plt.plot(handheldRecArray[beginInterest:endInterest, 0], color="red")
    # #
    # plt.show()
    #
    # plt.title("Channel 2 No noise")
    # plt.plot(handheldRecArray[beginInterest:endInterest, 1], color="red")
    # #
    # plt.show()
    # shiftFactor = int(newArray.size/5)
    # newArray.resize(newArray.size + shiftFactor)
    # newArray = np.roll(newArray, shiftFactor)
    #
    # print("Adjusted Size: " + str(newArray.size))
    #
    # plt.title("Shifted Recording")
    # plt.plot(newArray, color="red")
    # #
    # plt.show()



# handheldMicRec = sd.rec(int(seconds * sampleRate), device=1)
# webcamMicRec = sd.rec(int(seconds * sampleRate), device=2)
# print("Recording audio...")
# sd.wait()  # Wait until recording is finished
# print("Finished Recording.")
