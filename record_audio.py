#!/usr/bin/env python

import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import scipy.fftpack
import scipy.io.wavfile as wav
import argparse

def record_sample(time = 5, rate = 44100, channels = 1, chunk_size = 1024):

	"""Record an audio sample and return a 1D numpy array.

	Args:
		time (int): Duration of recording (seconds) 
		rate (int): sampling rate
		channels (int): number of channels
		chunk_size (int) chunk size

	Returns:
		array_like: audio sample represented as a 1D numpy array
	"""

	audio_format = pyaudio.paInt16
	audio = pyaudio.PyAudio()
 
	# start Recording
	stream = audio.open(format=audio_format, channels=channels,
	                rate=rate, input=True,
	                frames_per_buffer=chunk_size)
	print("recording...")
	frames = []
	 
	for i in range(0, int(rate / chunk_size * time)):
	    data = stream.read(chunk_size)
	    #frames.append(data)
	    frames.append(np.fromstring(data, dtype = np.int16))
	print("finished recording")

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# Transform audio to numpy array
	return(np.hstack(frames))


def save_audio(audio_array, filetype = "npy", filename = "test.wav", rate = 44100):
	
	"""Save audio captured using record_sample as a .wav or .npy

	Args:
		audio_array (array_like): Numpy array of audio sample (created by record_sample)
		filetype (str): Type of file to save (npy or wav)
		filename (str): Output filename
		rate (int): Sampling rate

	Returns:
		bool: True if successful, False otherwise.
	"""

	# Save file
	if filetype == "npy":
		np.save(filename, audio_array)
	elif filetype == "wav":
		wav.write(filename, rate, audio_array)
	else:
		raise ValueError("Invalid file type. Please choose npy or wav")

	return(True)

def main():

	parser = argparse.ArgumentParser(description = "Record audio sample and save as a .wav or .npy file.")

	parser.add_argument("-o", "--output", help = "Output filename (Default: audio.wav", default = "audio.wav")
	parser.add_argument("-f", "--format", help = "Format in which to save audio sample (wav or npy. Default: wav)", default = "wav")
	parser.add_argument("-t", "--time", help = "Duration of sample in seconds (Default: 5)", default = 5, type = int)
	parser.add_argument("-r", "--rate", help = "Sampling rate (Default: 44100)", default = 44100, type = int)

	args = parser.parse_args()

	numpyaudio = record_sample(time = args.time, rate = args.rate, channels = 1, chunk_size = 1024)

	save_audio(audio_array = numpyaudio, filetype = args.format, filename = args.output, rate = args.rate)

if __name__ == "__main__":
	main()
