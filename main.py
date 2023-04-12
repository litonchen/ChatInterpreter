import speech_recognition as sr
import pyttsx3,time,openai,time

# Initialize OpenAI API
openai.api_key = “ your api_key "
# Initialize the text to speech engine 
engine=pyttsx3.init()

def transcribe_audio_to_txt(filename):
    recogizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recogizer.record(source) 
    try:
        return recogizer.recognize_google(audio,language = 'zh-tw')
    except:
        print("skipping unkown error")
    
def voiceid(lan):
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name.lower().find(lan.lower()) >0:
            # print("voice:",voice.id)
            voice_id = voice.id
    return voice_id
        
def generate_response(messages):
    # https://platform.openai.com/docs/guides/chat/introduction
    response=openai.ChatCompletion.create(
                                            model="gpt-3.5-turbo",
                                            messages=messages
                                            )
    content = response['choices'][0]['message']['content']
    usages = response['usage']
    return content,usages

def speak_text(voice_id,text):
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #Waith for user say "genius"
        print("Say language you want to simultaneous interpret")
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            audio=recognizer.listen(source)
            try:
                lan = recognizer.recognize_google(audio)   
                print("input lan:",lan)

                voice_id = voiceid(lan)
                # engine.setProperty('voice', voice_id)
                print("language:",lan.lower(),"  voice_id:",voice_id)                
                filename ="input.wav"
                while True:               
                    print("Say your question")
                    #record audio                       
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())

                    #transcript audio to test 
                    text=transcribe_audio_to_txt(filename)
                    if text=="拜拜":
                        break
                        
                    if text:
                        print(f"yuo said {text}")
                        #Generate the response
                        r = [
                                {"role": "system", "content": f"you are a translator,translate my languange in to {lan}"},
                                {"role": "user", "content": text}                            
                            ]          
                        
                        content,usage = generate_response(r)
                        print(f"chat gpt 3 say {content}")
                        print(f" tokens usged {usage}")                            
                        #read resopnse using GPT3
                        speak_text(voice_id,content)

                    else:
                        text=''
            except :                
                break
if __name__=="__main__":
    main()
