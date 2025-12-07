# Automating-File-Renaming

This project is to automating files renaming using Kiro. Instead of manually renaming 100+ photos, this script renames all files inside a folder automatically, cleanly, and consistently.

## Problem

Managing photos manually is time-consuming. Renaming 100+ files by hand is boring, repetitive, and error-prone.
Photos exported from your phone (IMG_001, IMG_002…)
PDFs downloaded from email (document(1).pdf, document(2).pdf…)
Dataset files with inconsistent naming
Project assets that require a uniform naming format

## Common issues include:

Renaming each file manually takes minutes or hours
High chance of naming mistakes
No way to prefix, suffix, or reorder files easily
Repeating this task across multiple folders becomes frustrating
This is exactly the kind of repetitive, rule-based task that should be automated.

Example:
Your camera or mobile exports files like:
IMG_20240102_113244.png
IMG_20240102_113245.png
DCIM_0001.JPG

## Solution

Python provides everything needed to rename files programmatically using just a few lines of code. But instead of manually designing the entire script from scratch, we’ll use Kiro to help plan, generate, and refine the project quickly.

The script:
1. Reads all image files
2. Normalizes file extensions
3. Applies a clean naming pattern
4. Avoids conflicts

Usage

Run:
```
python file_renamer.py
```

Photos will be renamed to:

```
photo1.png
photo2.png
photo3.png
```

## How Kiro Helped

Kiro accelerated development by generating:
Requirements
Design plan
Task breakdown
Code templates
Final implementation

All generated files are included inside:

```
/.kiro/specs/file-renamer
```

## Final Output

<img width="1578" height="819" alt="60" src="https://github.com/user-attachments/assets/7b97bdc9-2cf9-4474-966f-8a205b412b31" />

## Directory Structure

```bash
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
```

## Tech Stack

```
Python 3

OS module

Kiro (for spec + automation generation)
```

## Conclusion

Automating file renaming is one of the simplest yet most useful tasks for beginners exploring Python automation. With tools like Kiro, the entire process—planning, coding, debugging, and iterating—becomes faster and more intuitive.
You not only build a real working automation tool but also experience how AI-assisted development accelerates everyday productivity.

