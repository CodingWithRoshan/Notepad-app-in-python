import warnings
warnings.filterwarnings("ignore")

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame
import json
import os
import shutil
import sys

pygame.mixer.init()

# Global Storage
images = []
image_references = {}
media_references = {}
current_file = None


# Resource Path (EXE Safe)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Main Window
root = tk.Tk()
root.title("Notepad")
root.geometry("1000x650")
root.minsize(800, 500)

main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

scrollbar = tk.Scrollbar(main_frame)
scrollbar.pack(side="right", fill="y")

text = tk.Text(
    main_frame,
    wrap=tk.WORD,
    font=("Segoe UI", 13),
    undo=True,
    yscrollcommand=scrollbar.set
)
text.pack(expand=True, fill="both")
scrollbar.config(command=text.yview)


# New File
def new_file():
    global current_file
    text.delete("1.0", tk.END)
    images.clear()
    image_references.clear()
    media_references.clear()
    pygame.mixer.music.stop()
    current_file = None
    root.title("Notepad")


# Insert Image
def insert_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((500, 350))
        photo = ImageTk.PhotoImage(img)

        images.append(photo)
        text.image_create(tk.INSERT, image=photo)
        text.insert(tk.INSERT, "\n")

        image_references[str(photo)] = file_path


# Insert Audio
def insert_audio():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )
    if file_path:
        filename = os.path.basename(file_path)
        placeholder = f"[Audio ▶ {filename}]\n"

        index = text.index(tk.INSERT)
        text.insert(tk.INSERT, placeholder)

        media_references[index] = {
            "type": "audio",
            "path": file_path
        }


# Insert Video
def insert_video():
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv")]
    )
    if file_path:
        filename = os.path.basename(file_path)
        placeholder = f"[Video ▶ {filename}]\n"

        index = text.index(tk.INSERT)
        text.insert(tk.INSERT, placeholder)

        media_references[index] = {
            "type": "video",
            "path": file_path
        }


# Double Click Media
def play_media(event):
    index = text.index(f"@{event.x},{event.y}")

    for key in media_references:
        if index.startswith(key):
            media = media_references[key]

            if media["type"] == "audio":
                pygame.mixer.music.load(media["path"])
                pygame.mixer.music.play()
            elif media["type"] == "video":
                os.startfile(media["path"])
            break


text.bind("<Double-1>", play_media)


# Audio Button Control
def play_selected_audio():
    cursor_index = text.index(tk.INSERT)
    line_number = cursor_index.split('.')[0]

    line_text = text.get(f"{line_number}.0", f"{line_number}.end")

    if "[Audio ▶" in line_text:
        for media in media_references.values():
            if media["type"] == "audio":
                filename = os.path.basename(media["path"])
                if filename in line_text:
                    pygame.mixer.music.load(media["path"])
                    pygame.mixer.music.play()
                    break


def stop_audio():
    pygame.mixer.music.stop()


# Save File (.mynote)
def save_file():
    global current_file

    if not current_file:
        current_file = filedialog.asksaveasfilename(
            defaultextension=".mynote",
            filetypes=[("My Note Files", "*.mynote")]
        )
    if not current_file:
        return

    base_name = os.path.splitext(current_file)[0]
    assets_folder = base_name + "_assets"
    os.makedirs(assets_folder, exist_ok=True)

    blocks = []
    dump_data = text.dump("1.0", tk.END, image=True, text=True)

    img_count = 0

    for item in dump_data:
        if item[0] == "text" and item[1]:
            blocks.append({"type": "text", "value": item[1]})

        elif item[0] == "image":
            image_name = item[1]
            original_path = image_references.get(image_name)
            if original_path:
                ext = os.path.splitext(original_path)[1]
                filename = f"image_{img_count}{ext}"
                destination = os.path.join(assets_folder, filename)
                shutil.copy(original_path, destination)

                blocks.append({
                    "type": "image",
                    "path": os.path.basename(assets_folder) + "/" + filename
                })
                img_count += 1

    with open(current_file, "w", encoding="utf-8") as file:
        json.dump(blocks, file, indent=4)

    messagebox.showinfo("Saved", "File saved successfully!")


# Open File
def open_file():
    global current_file
    file_path = filedialog.askopenfilename(
        filetypes=[("My Note Files", "*.mynote")]
    )
    if not file_path:
        return

    new_file()
    current_file = file_path

    with open(file_path, "r", encoding="utf-8") as file:
        blocks = json.load(file)

    base_folder = os.path.dirname(file_path)

    for block in blocks:
        if block["type"] == "text":
            text.insert(tk.END, block["value"])

        elif block["type"] == "image":
            path = os.path.join(base_folder, block["path"])
            if os.path.exists(path):
                img = Image.open(path)
                img.thumbnail((500, 350))
                photo = ImageTk.PhotoImage(img)

                images.append(photo)
                text.image_create(tk.END, image=photo)
                text.insert(tk.END, "\n")
                image_references[str(photo)] = path


# Clean Exit
def on_closing():
    pygame.mixer.music.stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_closing)

insert_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Insert", menu=insert_menu)
insert_menu.add_command(label="Image", command=insert_image)
insert_menu.add_command(label="Audio", command=insert_audio)
insert_menu.add_command(label="Video", command=insert_video)


# Audio Control Panel
control_frame = tk.Frame(root)
control_frame.pack(fill="x")

play_btn = tk.Button(control_frame, text="▶ Play Selected Audio", command=play_selected_audio)
play_btn.pack(side="left", padx=10, pady=5)

stop_btn = tk.Button(control_frame, text="⏹ Stop Audio", command=stop_audio)
stop_btn.pack(side="left", padx=5)

root.mainloop()
