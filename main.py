# Reference
# https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
# 
# Install packages
# pip install moviepy
# pip install pydub
# sudo apt-get install -y ffmpeg
# pip install SpeechRecognition
# pip install --upgrade AudioConverter

import glob
import os
import time
from moviepy.editor import *
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr 

def mp4_to_mp3():
    for video_file in glob.glob("./videofiles/*.mp4"):
        video = VideoFileClip(video_file)
        output_file_path = os.path.splitext(os.path.basename(video_file))[0]
        video.audio.write_audiofile("./audiofiles_mp3/" + output_file_path + ".mp3")


def mp3_to_wav():
    for mp3_file in glob.glob("./audiofiles_mp3/*.mp3"):
        sound = AudioSegment.from_mp3(mp3_file)
        output_file_path = os.path.splitext(os.path.basename(mp3_file))[0]
        output_file_path = "./audiofiles_wav/" + output_file_path + ".wav"
        sound.export(output_file_path, format="wav")
        os.remove(mp3_file)


def m4a_to_wav():
    for m4a_file in glob.glob("./audiofiles_m4a/*.m4a"):
        track = AudioSegment.from_file(m4a_file)
        output_file_path = os.path.splitext(os.path.basename(m4a_file))[0]
        output_file_path = "./audiofiles_wav/" + output_file_path + ".wav"
        track.export(output_file_path, format="wav")


def combine_wav_files(wav_files, output_file_path):
    combined_sound = None
    for i, wav_file in enumerate(wav_files):
        if i == 0:
            combined_sound = AudioSegment.from_wav(wav_file)
        else:
            combined_sound += AudioSegment.from_wav(wav_file)
    combined_sound.export(output_file_path, format="wav")


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    r = sr.Recognizer()
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 700,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    # whole_text = ""
    # create a file as output
    output_file_path = os.path.splitext(os.path.basename(path))[0]
    output_file_path = "./textfiles/" + output_file_path + ".txt"
    with open(output_file_path, 'a') as f:
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                # try converting it to text
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    print(text, file=f)
                    # whole_text += text
                finally:
                    os.remove(chunk_filename)
    # return the text for all chunks detected
    # return whole_text


def batch_wav_to_text():
    for wav_file in glob.glob("./audiofiles_wav/*.wav"):
        get_large_audio_transcription(wav_file)


def main():
    begin_time = time.time()
    try:
        # mp4_to_mp3()
        # mp3_to_wav()
        # m4a_to_wav()
        batch_wav_to_text()

        # l = [
        #     "./audiofiles_wav/test1.wav",
        #     "./audiofiles_wav/test2.wav",
        #     "./audiofiles_wav/test3.wav"
        # ]
        # output_file_path = "./audiofiles_wav/combined_test.wav"
        # combine_wav_files(l, output_file_path)

        # get_large_audio_transcription("./audiofiles_wav/test.wav")

    finally:
        print(f"elapsed_time:{time.time() - begin_time} [sec]")


if __name__ == '__main__':
    main()
