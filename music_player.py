from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import os

pygame.mixer.init()

fileDirector = ''
paused = False

main = Tk()
main.title('Music Player')
main.geometry('1000x500')

frame = Frame(main, bg='black')
frame.pack(expand=True, fill=BOTH)

list_frame = Frame(frame)
list_frame.place(x=400, y=250)

listBox = Listbox(list_frame, background='white', width=85, height=12)
listBox.pack(padx=5, pady=5)

def get_cur_song_index():
    selected_index = listBox.curselection()
    return selected_index[0] if selected_index else None

def play_song():
    global fileDirector, paused
    index = get_cur_song_index()
    if index is not None:
        cur_song = listBox.get(index)
        pygame.mixer.music.load(os.path.join(fileDirector, cur_song))
        pygame.mixer.music.play()
        paused = False

def prev_song():
    index = get_cur_song_index()
    if index is not None:
        prev_index = listBox.size() - 1 if index == 0 else index - 1
        listBox.select_clear(0, END)
        listBox.select_set(prev_index)
        play_song()

def pause_song():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True

def resume_song():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False

def next_song():
    index = get_cur_song_index()
    if index is not None:
        next_index = index + 1 if index < listBox.size() - 1 else 0
        listBox.select_clear(0, END)
        listBox.select_set(next_index)
        play_song()

def Folder():
    global fileDirector
    fileDirector = filedialog.askdirectory(title='Select a Music Folder')
    if not fileDirector:
        return
    music_files = [file for file in os.listdir(fileDirector) if file.endswith(('.mp3', '.wav'))]
    if music_files:
        listBox.delete(0, END)
        for song in music_files:
            listBox.insert(END, song)
    else:
        listBox.insert(0, 'No audio files in selected folder')

def load_image(image_path, size):
    img = Image.open(image_path).resize(size)
    return ImageTk.PhotoImage(img)

def btn(img, fun):
    return Button(frame, image=img, bg='black', activebackground='white', border=0, command=fun)

imgGrd = load_image('bgc.png', (1000, 250))
topGradient = Label(frame, image=imgGrd, bg='black')
topGradient.pack(side=TOP)

playImg = load_image('play.jpg', (50, 50))
play_btn = btn(playImg, play_song)
play_btn.place(x=180, y=300)

prevImg = load_image('prev.png', (40, 40))
prev_btn = btn(prevImg, prev_song)
prev_btn.place(x=95, y=370)

pauseImg = load_image('pause.png', (40, 40))
pause_btn = btn(pauseImg, pause_song)
pause_btn.place(x=160, y=370)

resumeImg = load_image('resume.png', (40, 40))
resume_btn = btn(resumeImg, resume_song)
resume_btn.place(x=225, y=370)

nextImg = load_image('next.png', (40, 40))
next_btn = btn(nextImg, next_song)
next_btn.place(x=280, y=370)

open_folder = Button(frame, text='Open Folder', bg="#064F61", padx=5, pady=5, foreground='white', command=Folder)
open_folder.place(x=400, y=200)

main.mainloop()