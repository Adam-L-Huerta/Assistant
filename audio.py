import pyaudio
import wave
import speech_recognition as sr
import subprocess
from commands import Commander


def say(text):
    subprocess.call('say '+ text, shell=True)


def play_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=pa.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True

    )

    data_stream = wf.readframes(chunk)

    while data_stream:
        stream.write(data_stream)
        data_stream = wf.readframes(chunk)

    stream.close()
    pa.terminate()


r = sr.Recognizer()
running = True
cmd = Commander()


def initSpeech():

    print("Listening...")
    play_audio("./audio/aladdin_who_disturbs.wav")

    with sr.Microphone() as source:
        print("Say something...")
        r.adjust_for_ambient_noise(source, duration=3)
        r.energy_threshold = 300
        audio = r.listen(source)

    play_audio("./audio/aladdin_outta_here.wav")

    command = ""

    try:
        command = r.recognize_google(audio)
    except:
        print("Couldn't understand you...")

    print("Your command:")
    print(command)
    if command == ["quit", "exit", "goodbye", "bye"]:
        global running
        running = False

    cmd.discover(command)
    # say("You said" + command)


while running:
    initSpeech()
