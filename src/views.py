from django.shortcuts import  render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import speech_recognition as sr
import pyttsx3
import webbrowser

import datetime

# Create an instance of speech recognition

# Initialize text-to-speech engine

# Define a function to speak the given text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Define a function to listen for audio input and return the transcribed text
def listen():
    r = sr.Recognizer()
    print("Listening...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # reduce background noise
        audio = r.listen(source)
        
        try:
            print("Recognizing...")
            # Use Google Speech Recognition to transcribe audio
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Unknow error occurred.")
            speak("Sorry, I didn't understand what you said.")
        except sr.RequestError:
            speak("Sorry, I couldn't access the speech recognition service.")

# Define assistant functionality
def start_assitant(request):
    print("Assistant started.")
    speak("Hello! How can I assist you?")
    try:
        while True:
            text = listen()
            if "your name" in text:
                voice_history.objects.create(user=request.user, voice_text=text)
                speak("My name is Mira")
            
            elif "open browser" in text:
                speak("Opening browser...")
                voice_history.objects.create(user=request.user, voice_text=text)
                webbrowser.open('http://www.google.com')
            
            elif "open youtube" in text:
                speak("Opening browser...")
                voice_history.objects.create(user=request.user, voice_text=text)
                webbrowser.open('https://www.youtube.com/')    
                # code to open browser
            elif "play music" in text:
                speak("Playing music...")
                webbrowser.open('https://www.youtube.com/watch?v=kJQP7kiw5Fk')
                # code to play music
            elif "what is the time" in text:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                voice_history.objects.create(user=request.user, voice_text=text)
                speak(f"The time is {current_time}.")
            
            elif "exit" in text:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand what you said.")
    except Exception as e:
        messages.error(request, "no input found")
        return redirect("src:home"
                        )            

    return render(request , 'home.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect("src:login")

    context={
        'speeches': voice_history.objects.filter(user=request.user)
    }
    return render(request , 'home.html' , context)


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("src:home")
            else:
                messages.error(request,"Invalid username or password.")
                return redirect("src:home")
        else:
            messages.error(request,"Invalid username or password.")
            return redirect("src:home")
    
    
    form = AuthenticationForm()
    return render(request , 'login.html')

def register_page(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("src:home")
        else:        
            messages.error(request, f"{form.errors}")
            return redirect("src:register")
    form = NewUserForm()
    return render (request, "register.html", context={"form":form})


def logout_page(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("src:login")
    