# Requirements Document

## Introduction

This document specifies the requirements for a file renaming automation tool that renames files in a specified folder according to a consistent naming pattern. The tool will process image files in the photos directory and rename them from their current format (e.g., "1.PNG", "2.PNG") to a standardized format (e.g., "photo1.png", "photo2.png").

## Glossary

- **File Renamer**: The system that automates the renaming of files in a specified directory
- **Input Folder**: The directory containing files to be renamed
- **Naming Pattern**: The template format used for generating new filenames (e.g., "photo{number}.{extension}")
- **File Extension**: The suffix of a filename that indicates the file type (e.g., ".png", ".PNG")

## Requirements

### Requirement 1

**User Story:** As a user, I want to specify an input folder containing files to rename, so that I can organize files in that directory with consistent naming.

#### Acceptance Criteria

1. WHEN a user provides a folder path THEN the File Renamer SHALL validate that the folder exists
2. WHEN the specified folder does not exist THEN the File Renamer SHALL report an error and halt processing
3. WHEN the specified folder exists THEN the File Renamer SHALL proceed to identify files for renaming

### Requirement 2

**User Story:** As a user, I want files to be renamed in a sequential numeric format with a consistent prefix, so that files are easily identifiable and properly ordered.

#### Acceptance Criteria

1. WHEN the File Renamer processes files THEN the File Renamer SHALL rename each file using the pattern "photo{number}.{extension}"
2. WHEN assigning numbers to files THEN the File Renamer SHALL use sequential integers starting from 1
3. WHEN processing file extensions THEN the File Renamer SHALL normalize extensions to lowercase
4. WHEN multiple files have numeric names THEN the File Renamer SHALL preserve the numeric ordering in the new names

### Requirement 3

**User Story:** As a user, I want the system to handle various file extensions correctly, so that different file types are renamed appropriately while preserving their type information.

#### Acceptance Criteria

1. WHEN a file has an uppercase extension THEN the File Renamer SHALL convert it to lowercase in the new filename
2. WHEN a file has a mixed-case extension THEN the File Renamer SHALL normalize it to lowercase
3. WHEN renaming files THEN the File Renamer SHALL preserve the original file extension type

### Requirement 4

**User Story:** As a user, I want to avoid accidental data loss during renaming, so that my files remain safe throughout the process.

#### Acceptance Criteria

1. WHEN a target filename already exists THEN the File Renamer SHALL handle the conflict without overwriting existing files
2. WHEN renaming operations fail THEN the File Renamer SHALL report which files could not be renamed
3. WHEN processing completes THEN the File Renamer SHALL report the number of files successfully renamed

### Requirement 5

**User Story:** As a user, I want to see what changes will be made before they happen, so that I can verify the renaming operation is correct.

#### Acceptance Criteria

1. WHEN the File Renamer identifies files to rename THEN the File Renamer SHALL display the current filename and proposed new filename for each file
2. WHEN displaying rename operations THEN the File Renamer SHALL show the total count of files to be processed
3. WHEN the rename preview is complete THEN the File Renamer SHALL execute the renaming operations
