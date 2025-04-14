import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice).lower()

            if 'maya' in command:
                command = command.replace('maya', '').strip()
                print(f"Command: {command}")
    except sr.WaitTimeoutError:
        print("No speech detected within 5 seconds.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition; {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return command

def run_maya():
    command = take_command()
    if not command:
        return

    print(f"Executing: {command}")

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk(f"Current time is {time}")

    elif 'date' in command:
        date = datetime.date.today().strftime('%B %d, %Y')
        print(date)
        talk(f"The date today is {date}")

    elif 'who is' in command or 'tell me about' in command or 'explain about' in command or 'can you tell me about' in command:
        query = command.replace('who is', '').replace('tell me about', '').replace('explain about', '').replace('can you tell me about', '').strip()
        try:
            info = wikipedia.summary(query, sentences=1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"Multiple results found. Can you be more specific about {query}?")
        except wikipedia.exceptions.PageError:
            talk(f"Sorry, I couldn't find information about {query}.")

    elif 'am i good' in command:
        talk("You're doing your best, never give up!")

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'exit' in command or 'stop' in command:
        talk("Goodbye!")
        return True

    else:
        talk("I didn't get that. Can you repeat yourself?")

if __name__ == "__main__":
    talk("Hello! I am Maya. How can I help you?")
    while True:
        should_exit = run_maya()
        if should_exit:
            break