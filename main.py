import os
import streamlit as st
import pyttsx3
from dotenv import load_dotenv
from groq import Groq
import speech_recognition as sr


load_dotenv()

client = Groq(api_key = os.getenv('GroqAPI'))

def speak_text(text):
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('voice', 'English')
        tts_engine.setProperty("rate", 185)
        tts_engine.setProperty('volumne', 1)
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        st.error(f"Error converting text to speech: {e}")


def capture_voice():
    speech = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Listining.......Speak into the Microphone")

        try:
            audio = speech.listen(source, timeout= 5)
            text = speech.recognize_google(audio)
            st.success(f"You said: {text}")
            return text

        except sr.RequestError as e:
            st.error(f"Speech Request Error {e}")
            return None
        except sr.UnknownValueError:
            st.error("Speech Recognition could not understand audio")
            return None
        except sr.WaitTimeoutError:
            st.error("Listening timed out.")
            return None

        
st.title("TensorGo Voice Chat-Bot")
st.markdown("Technologies : Groq, SpeechRegconition, Pyttsx3")


if 'conversation' not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("Type your messages here:")

if st.button("Send Text") and user_input:
    st.session_state.conversation.append({'role': 'user', 'content': user_input})
    try:
        response= client.chat.completions.create(
            messages = st.session_state.conversation,
            model = 'llama3-8b-8192',
        )
        bot = response.choices[0].message.content
        st.session_state.conversation.append({'role': 'assistant', 'content': bot})
        st.success(f"Bot: {bot}")
        speak_text(bot)
    except Exception as e:
        st.error(f"An error occured {e}")

if st.button("Click here to Speak"):
    voice_in = capture_voice()
    if voice_in:
        st.session_state.conversation.append({'role': 'user', 'content': voice_in})
        try:
            response = client.chat.completions.create(
                messages = st.session_state.conversation,
                model = 'llama3-8b-8192',
            )
            bot_re = response.choices[0].message.content
            st.session_state.conversation.append({'role': 'assistant', 'content': bot_re})
            st.success(f"Bot: {bot_re}")
            speak_text(bot_re)
        except Exception as e:
            st.error(f"An error occured {e}")           

st.markdown("#### Conversation History:")
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Bot:** {message['content']}")