# 📝 Notepad

A feature-rich desktop-based Multimedia Text Editor built using Python and Tkinter.

This application extends the functionality of a traditional text editor by allowing users to embed and manage multimedia content directly inside documents.

---

## 📌 Problem Statement

Traditional text editors such as Notepad only support plain text editing and do not provide the ability to embed multimedia elements such as images, audio, or video within documents.

The objective of this project is to design and develop a Multimedia Notepad that:

- Supports text editing
- Embeds images within documents
- Plays audio files
- Launches video files
- Saves documents in a structured custom file format
- Can be packaged as a standalone Windows executable

---

## 🚀 Features

- 🖊 Rich Text Editing
- 🖼 Insert Images inside the editor
- 🎵 Insert Audio with Play / Stop controls
- 🎥 Insert Video (opens in system media player)
- 💾 Custom `.mynote` file format
- 📁 Automatic assets folder management
- 🔄 Save / Open / New file functionality
- 🖥 Scrollable interface
- ↩ Undo support
- 🧹 Clean application shutdown
- 📦 EXE packaging support using PyInstaller

---

## 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core programming language |
| Tkinter | GUI framework |
| Pillow | Image processing |
| Pygame | Audio playback |
| JSON | Structured file storage |
| PyInstaller | EXE packaging |

---

## 📦 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/CodeWithRoshan/Notepad.git
cd Notepad
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python main.py
```

---

## 💾 File Format Structure

When saving a document:

```
example.mynote
example_assets/
```

### `.mynote` file
- Stores structured JSON data
- Contains text blocks
- References multimedia files

### `_assets` folder
- Stores images
- Stores audio files
- Stores video files

This ensures proper multimedia management and portability.

---

## 🖥 Building as Windows Executable

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build the EXE

```bash
pyinstaller --onefile --windowed --icon=app.ico main.py
```

The executable will be available inside:

```
dist/
```

✔ No console window  
✔ Runs like real desktop software  

---

## 🎯 How It Works

1. Text is inserted normally.
2. Images are embedded inside the text widget.
3. Audio and video are inserted as structured placeholders.
4. When saving:
   - The content is serialized into JSON.
   - Multimedia files are copied into an assets folder.
5. When opening:
   - JSON is parsed.
   - Text and images are reconstructed.
   - Media references are restored.

---

## 📈 Future Improvements

- In-app video player
- Single compressed file format (ZIP-based `.mynote`)
- Dark mode theme
- Toolbar with icons
- Cross-platform support (Mac/Linux)
- Installer package (.msi)
- Drag & drop multimedia
- Autosave functionality

---

## 🎓 Learning Outcomes

This project demonstrates understanding of:

- GUI development using Tkinter
- Multimedia handling in Python
- File serialization using JSON
- Custom file format design
- Desktop application packaging
- Software architecture design
  
---

## 👨‍💻 Author

Developed by **Roshan**

If you like this project, feel free to ⭐ star the repository!
