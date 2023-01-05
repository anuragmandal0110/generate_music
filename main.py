from tkinter import *
import tkinter as Tk
from tkinter import LabelFrame
from functools import partial
from PIL import Image, ImageTk
from generate_instrument_music import generate_music, generate_piano, generate_drums
from generate_emotion_music import generate_emotional_music,generate_emotion_music

CONTINUE = True



instrument_type = ""
emotion_type = ""

#function for quit button in Tkinter
def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

#function to switch frames in Tkinter
def change_frame(disp,dest):
    disp.pack(fill='both', expand=1)
    dest.pack_forget()

#function to switch between the two siren templates
def music(arg):
  pass


def change_instrument_type():
    global instrument_type
    if(v.get() == '1'):
        instrument_type = "piano"
    else :
        instrument_type = "drums"
    print(instrument_type,v.get())


def change_emotion():
    global emotion_type
    if (x.get() == 1):
        emotion_type = "happy"

    elif (x.get() == 2):
        emotion_type = "angry"
    elif (x.get() == 3):
        emotion_type = "calm"
    else:
        emotion_type = "sad"
    print(emotion_type, x.get())



#--------------------------------
#Part1: TKinter

# Define Tkinter root\\\
root = Tk.Tk()
root.geometry('450x450')
root.title("DSP Project Application")
path ="./piano.jfif"
img = ImageTk.PhotoImage(Image.open(path))
# label1.image = test

#here I hae made different frames for different templates
#this is the first frame. Here the user will be asked to select between the two templates. We call this frame "Home"
frame_main = LabelFrame(root, text="Home", fg="Red", padx=15, pady=15)
frame_main.pack(fill="both", expand=1)
frame_main_lab2 = Label(frame_main, text="Welcome to the Home Page of our Music Generator AI", fg="blue")
frame_main_lab2.place(relx=0.20, rely=0.30)
frame_main_lab1 = Label(frame_main, image = img)
# frame_main.pack()
frame_main_lab1.place(relx=0.0, rely=0.40)



#frame for the sinusoidal siren
frame_music = LabelFrame(root, text="Generating Music with AI", fg="blue", padx=15, pady=15)

filename = Tk.Entry(frame_music)
filename.insert(0, "Default_filename")
filename.pack()



frame_emotion = LabelFrame(root, text="Generating Music according to emotion", fg="Red", padx=15, pady=0)

filename2 = Tk.Entry(frame_emotion)
filename2.insert(0, "Default_filename")
filename2.pack()


clip_time = Tk.DoubleVar()
clip_time.set(2)


clip_time_2 =  Tk.DoubleVar()
clip_time_2.set(2)





Randomness = Tk.DoubleVar()
f_min = Tk.DoubleVar()
# Initialize to 5000hz and
Randomness.set(2)
f_min.set(5)


Randomness_2 = Tk.DoubleVar()
Randomness_2.set(2)

v = StringVar(frame_main, "1")
x = IntVar(frame_main, "1")

# Dictionary to create multiple buttons
values = {"The Grand Piano": "1",
          "The MIDI Drums": "2",
          }

# Loop is used to create multiple Radiobuttons
# rather than creating each button separately
for (text, value) in values.items():
  Radiobutton(frame_music, text=text, variable=v,
              value=value, indicator=0,command=change_instrument_type,
              background="light blue").pack(fill=X, ipady=5)


# Dictionary to create multiple buttons
emotions = {"Happy": "1",
          "Sad": "2",
          "Angry": "3",
          "Calm": "4",
          }

for (text, value) in emotions.items():
  Radiobutton(frame_emotion, text=text, variable=x,
              value=value, indicator=0,command=change_emotion,
              background="light blue").pack(fill=X, ipady=5)

def generate_music_with_type():
    from tkinter import messagebox
    global instrument_type
    time = clip_time.get()
    name = filename.get()

    if(len(name) == 0):
        name = "generate_music.mid"
    else:
        name = name + ".mid"

    randomness = Randomness.get()
    if(instrument_type == ""):
        messagebox.showerror('Error', 'Please select the intrument type')
    elif(instrument_type == "piano"):
        messagebox.showinfo("Please Wait","Generating Piano music , this will take a minute")
        generate_piano(name, int(time * 60) , int(randomness + 1))
    else:
        messagebox.showinfo("Please Wait", "Generating Drums music , this will take a minute")
        generate_drums(name, int(time * 60) , int(randomness + 1))


def generate_music_with_emotion():
    from tkinter import messagebox
    global emotion_type
    time = clip_time_2.get()
    name = filename2.get()

    if(len(name) == 0):
        name = "generate_music.mid"
    else:
        name = name + ".mid"

    randomness = Randomness_2.get()
    if(emotion_type == ""):
        messagebox.showerror('Error', 'Please select the emotion type')
    elif(emotion_type == "happy"):
        messagebox.showinfo("Please Wait","Generating Happy music , this will take a minute")
        generate_emotional_music(name, int(time * 60) , int(randomness + 1),"0")
    elif (emotion_type == "angry"):
        messagebox.showinfo("Please Wait", "Generating Angry music , this will take a minute")
        generate_emotional_music(name, int(time * 60), int(randomness + 1),"1")
    elif (emotion_type == "calm"):
        messagebox.showinfo("Please Wait", "Generating Calm music , this will take a minute")
        generate_emotional_music(name, int(time * 60), int(randomness + 1),"2")
    elif (emotion_type == "sad"):
        messagebox.showinfo("Please Wait", "Generating Sad music , this will take a minute")
        generate_emotional_music(name, int(time * 60), int(randomness + 1),"3")



# Define widgets
s_time_1 = Tk.Scale(frame_music, label ='The length of clip', variable = clip_time, from_ = 1, to = 10, tickinterval = 1, orient=HORIZONTAL)
s_random_1 = Tk.Scale(frame_music, label ='Randomness of Notes', variable = Randomness, from_ = 0, to = 10, tickinterval = 1, orient=HORIZONTAL)

s_time_2 = Tk.Scale(frame_emotion, label ='The length of clip', variable = clip_time_2, from_ = 1, to = 10, tickinterval = 1, orient=HORIZONTAL)
s_random_2 = Tk.Scale(frame_emotion, label ='Randomness of Notes', variable = Randomness_2, from_ = 0, to = 10, tickinterval = 1, orient=HORIZONTAL)

#quit button
btn_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

btn_music = Tk.Button(frame_main, text="Go to generate Music with different instruments", command=partial(change_frame, frame_music, frame_main))

btn_emotion = Tk.Button(frame_main, text="Go to generate Music on the basis of emotion", command=partial(change_frame, frame_emotion, frame_main))

#buttons for the sinusoidal siren frame
btn_home1 = Tk.Button(frame_music, text="Back", command=partial(change_frame, frame_main, frame_music))
btn_play1 = Tk.Button(frame_music, text="Generate Music File", command=partial(generate_music_with_type))

#buttons for min max frame
btn_home2 = Tk.Button(frame_emotion, text="Back", command=partial(change_frame, frame_main, frame_emotion))
btn_play2 = Tk.Button(frame_emotion, text="Generate Music File", command=partial(generate_music_with_emotion))

# Place widgets- for the alignment of different widgets in frames
btn_quit.pack(side="bottom", pady=20)

# S2.pack(side = "right",fill="both")
s_time_1.pack(side ="top", fill="both", expand=1)
s_random_1.pack(fill="both")

s_time_2.pack(side ="top", fill="both", expand=1)
s_random_2.pack(fill="both")

btn_music.pack(pady=10)
btn_emotion.pack(pady=5)
btn_home1.pack(side="bottom",fill="both")
btn_home2.pack(side="bottom",fill="both")
btn_play1.pack(side="bottom", fill="both")
btn_play2.pack(side="bottom", fill="both")

sel=''

while CONTINUE:
  root.update()

  #for sinusoidal siren
  #Here we use a sinusoidal wave to generate fluctuating frequencies.
  #this is frequency modulation formula that we are using here
  if sel=="modulation":
    pass

  #for min-max siren
  #Here we give alternating blocks maximum and minimum frequency entered by the user to generate fluctuating frequencies.
  elif sel=="min-max":
    pass

print('* Finished')
