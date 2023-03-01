import openai
import speech_recognition as sr
# This module is imported so that we can 
# play the converted audio
import os
# import playsound
from playsound import playsound
from gtts import gTTS 


###############################################################################################
# risponde alla domanda
def askGPT(text4qn):
    openai.api_key = "la tua chiave open ai"
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = text4qn,
        temperature = 0.6,
        max_tokens = 150,
    )
    resp = response.choices[0].text
    #return print(response.choices[0].text)
    return resp

###############################################################################################
# ascolta la domanda e trasforma in testo
def mySR():
    # create a new speech recognizer
    r = sr.Recognizer()
    # open the microphone and start recording
    with sr.Microphone() as source:
        print("Parla ora... (Speak now...)")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("finito di ascoltare...")

    # use Google Speech Recognition API to transcribe the speech in Italian language
    try:
        mySRtext = r.recognize_google(audio, language="it-IT")
        #return print("Hai detto: {}".format(text))  # translates to "You said:"
        print("finito di riconoscere...")
        qn = "{}".format(mySRtext)
        return qn  
    except sr.UnknownValueError:
        print("Mi dispiace, non ho capito il tuo discorso. (Sorry, I could not understand your speech.)")
    except sr.RequestError as e:
        print("Mi dispiace, non sono riuscito a richiedere i risultati del servizio di riconoscimento vocale di Google. {}".format(e))

###############################################################################################

def myGTTS(mytext):
    # The text that you want to convert to audio
    #mytext = 'dai trombone trombolone trombone Vai a suonare il pianoforte su'
    
    # Language in which you want to convert
    language = 'it'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("testo.mp3")
    audio_file = 'c:\\users\\ricca\\testo.mp3'
    #audio_file = os.path.dirname(__file__) + '\\..\\..\\testo.mp3'
    playsound(audio_file)
    #playsound("testo.mp3")
    #os.system("testo.mp3")

###############################################################################################
def main():
    secret_word = "mattonello"
    while True:

        MIR_enabled = False  
        
        while True:  
            print('MIR: attesa ...\n')
            myQn = mySR()  
            if myQn == secret_word.lower() :
                MIR_enabled = True
                break

        if MIR_enabled:
            print('GPT: Cosa mi vuoi chiedere?\n')
            myQn = mySR()
            print(myQn)
            print('\n')
            aiResp = askGPT(myQn)
            #askGPT(myQn)
            print(aiResp)
            print('\n')
            MIR_enabled = False 
            myGTTS(aiResp)
        

main()
