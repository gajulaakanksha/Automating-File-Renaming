# Automating-File-Renaming

This project is to automating files renaming using Kiro. Instead of manually renaming 100+ photos, this script renames all files inside a folder automatically, cleanly, and consistently.

Problem

Managing photos manually is time-consuming.
Renaming 100+ files by hand is boring, repetitive, and error-prone.

Problem

Renaming dozens of files manually is:

Time-consuming

Repetitive

Error-prone

Mentally exhausting
Example:
Your camera or mobile exports files like:
IMG_20240102_113244.png
IMG_20240102_113245.png
DCIM_0001.JPG


Solution

I built an automated file renaming script with Kiro.
The script:

Reads all image files

Normalizes file extensions

Applies a clean naming pattern

Avoids conflicts

Renames photos automatically

Includes Kiro-generated specs, design, and tasks

Solution

I automated the entire task using a Python-based File Renamer generated with the help of Kiro.

This script:

Reads all files inside a given folder

Ignores non-image files if needed

Normalizes extensions (.jpg, .jpeg, .png)

Renames files into a clean sequence:

photo1.png
photo2.png
photo3.png



Project Structure

.kiro/
photos/
file_renamer.py
.gitignore
README.md


Usage

Run:

python file_renamer.py

Photos will be renamed to:
photo1.png
photo2.png
photo3.png
...

How Kiro Helped

Kiro generated:

Requirements

Design

Task breakdown

Test cases

Code implementation

I used Kiro to speed up development and ensure clean structure.

How Kiro Helped

Kiro accelerated development by generating:

Requirements

Design plan

Task breakdown

Code templates

Final implementation

All generated files are included inside:
/.kiro/specs/file-renamer

Project File Structure

file-renamer-project/
│
├── .kiro/
│   └── specs/
│       └── file-renamer/
│           ├── design.md
│           ├── requirements.md
│           ├── tasks.md
│
├── photos/       
│   └── (your images here)
│
├── file_renamer.py
│
├── .gitignore
│
└── README.md


Tech Stack

Python 3

OS module

Kiro (for spec + automation generation)


