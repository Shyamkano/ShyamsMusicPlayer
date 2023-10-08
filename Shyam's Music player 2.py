import tkinter as tk
from tkinter import filedialog
import pygame
import os
import io
import keyboard
from PIL import Image, ImageTk
from mutagen.id3 import ID3

# Initialize Pygame for audio playback
def initialize():
    global playlist, muted
    pygame.init()
    playlist = []
    muted = False

# Function to add a folder to the playlist
def add_folder():
    """
    Opens a file dialog to select a folder and adds all MP3 files from the selected folder to the playlist.
    """
    global playlist
    folder_path = filedialog.askdirectory(initialdir="/", title="Select a Folder")
    if folder_path:
        playlist = []
        playlist_box.delete(0, tk.END)
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp3"):
                song_path = os.path.join(folder_path, filename)
                playlist.append(song_path)
                playlist_box.insert(tk.END, os.path.basename(song_path))
        print("Added songs to the playlist.")

# Function to update the album art displayed on the GUI
def update_album_art(song_path):
    """
    Updates the album art displayed on the GUI based on the selected song's ID3 tag.
    """
    audio = ID3(song_path)
    if 'APIC:' in audio:
        img_data = audio['APIC:'].data
        image = Image.open(io.BytesIO(img_data))
        image = image.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        album_art_label.config(image=photo)
        album_art_label.image = photo
    else:
        album_art_label.config(image=default_album_art)
        album_art_label.image = default_album_art

# Function to play and pause music
def play_music():
    """
    Plays or pauses the currently selected song in the playlist.
    """
    global current_song_index
    selected_song = playlist_box.curselection()
    if selected_song:
        selected_song = int(selected_song[0])
        if current_song_index != selected_song:
            current_song_index = selected_song  # Update the current song index
            update_album_art(playlist[current_song_index])  # Update album art for the new song
        song = playlist[current_song_index]
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            playButton.config(image=play_img)
            print("Paused playback.")
        else:
            pygame.mixer.music.unpause()
            playButton.config(image=pause_img)
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            print("Started playback of:", os.path.basename(song))

# Function to play the next song in the playlist
def next_song():
    """
    Plays the next song in the playlist. 
    """
    global current_song_index
    if current_song_index < len(playlist) - 1:
        current_song_index += 1
    else:
        current_song_index = 0
    playlist_box.selection_clear(0, tk.END)
    playlist_box.activate(current_song_index)
    playlist_box.selection_set(current_song_index)
    pygame.mixer.music.load(playlist[current_song_index])
    pygame.mixer.music.play(loops=0)
    update_album_art(playlist[current_song_index])  
    print("Playing next song:", os.path.basename(playlist[current_song_index]))

# Function to play the previous song in the playlist
def prev_song():
    """
    Plays the previous song in the playlist.
    """
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
    else:
        current_song_index = len(playlist) - 1
    playlist_box.selection_clear(0, tk.END)
    playlist_box.activate(current_song_index)
    playlist_box.selection_set(current_song_index)
    pygame.mixer.music.load(playlist[current_song_index])
    pygame.mixer.music.play(loops=0)
    update_album_art(playlist[current_song_index])
    print("Playing previous song:", os.path.basename(playlist[current_song_index]))

# Function to toggle mute/unmute
def toggle_mute():
    """
    Toggles between muting and unmuting the audio.
    """
    global muted
    if not muted:
        muted = True
        pygame.mixer.music.set_volume(0)
        muteButton.config(image=unmute_img)
        muteButton.image = unmute_img
        print("Muted audio.")
    else:
        muted = False
        pygame.mixer.music.set_volume(0.5)
        muteButton.config(image=mute_img)
        muteButton.image = mute_img
        print("Unmuted audio.")

# Class to create tooltips for widgets
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 10
        y += self.widget.winfo_rooty() + 10
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Function to handle play/pause using the spacebar key
def play_pause_with_keyboard(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'space':
        play_music()

# Function to handle next song using the right arrow key
def next_song_with_keyboard(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'right':
        next_song()

# Function to handle previous song using the left arrow key
def prev_song_with_keyboard(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'left':
        prev_song()

# Function to handle mute/unmute using the 'm' key
def toggle_mute_with_keyboard(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'm':
        toggle_mute()

# Function to add a folder using the 's' key
def add_folder_with_keyboard(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 's':
        add_folder()

# Create and configure the root window
root = tk.Tk()
root.title("Shyam's Music Player")
root.resizable(False, False)
root.configure(background="#c99cfb")

# Initialize Pygame for audio playback
initialize()

# Create a label for album art display
default_album_art = ImageTk.PhotoImage(Image.open("default.png").resize((300, 300), Image.LANCZOS))
album_art_label = tk.Label(root, image=default_album_art, bg="#2c3e50", borderwidth="0")
album_art_label.place(x=15, y=0)

# Load button images
play_img = ImageTk.PhotoImage(Image.open("play.png"))
pause_img = ImageTk.PhotoImage(Image.open("pause.png"))
next_img = ImageTk.PhotoImage(Image.open("next.png"))
prev_img = ImageTk.PhotoImage(Image.open("prev.png"))
mute_img = ImageTk.PhotoImage(Image.open("mute.png"))
unmute_img = ImageTk.PhotoImage(Image.open("unmute.png"))

# Create and configure buttons with images
playButton = tk.Button(root, image=play_img, borderwidth="0", command=play_music)
nextButton = tk.Button(root, image=next_img, borderwidth="0", command=next_song)
prevButton = tk.Button(root, image=prev_img, borderwidth="0", command=prev_song)
addButton = tk.Button(root, width=20, height=2, text="Select your Playlist", font=10, bg="#e7d3fd", fg="black", command=add_folder).place(x=45, y=330)
muted = False
muteButton = tk.Button(root, image=mute_img, borderwidth="0", command=toggle_mute)

# Arrange buttons in a horizontal row
prevButton.pack(side=tk.LEFT,anchor="s", padx=10, pady=10)
playButton.pack(side=tk.LEFT,anchor="s", padx=10, pady=10)
nextButton.pack(side=tk.LEFT,anchor="s", padx=10, pady=10)
muteButton.pack(side=tk.LEFT,anchor="s", padx=10, pady=10)

# Create tooltips for buttons
Tooltip(prevButton, "Previous")
Tooltip(playButton, "Play/Pause")
Tooltip(nextButton, "Next")
Tooltip(muteButton, "Mute/Unmute")

# Bind keyboard shortcuts to functions
keyboard.on_press_key('left', prev_song_with_keyboard)
keyboard.on_press_key('right', next_song_with_keyboard)
keyboard.on_press_key('space', play_pause_with_keyboard)
keyboard.on_press_key('m', toggle_mute_with_keyboard)
keyboard.on_press_key('s', add_folder_with_keyboard)

# Create and configure the playlist listbox
playlist_box = tk.Listbox(root, bg="#D6B4FC", fg="white", selectbackground="black", selectforeground="blue", width=50, height=30, borderwidth="0")
playlist_box.pack(side='top', anchor="se", fill="both", expand=True)
current_song_index = -1

# Start the GUI main loop
root.mainloop()
