# Design Document

## Overview

The File Renamer is a command-line utility that automates the renaming of files in a specified directory. It will be implemented as a Python script that processes files in a given folder, validates the input, generates new filenames based on a sequential pattern, and performs the rename operations safely. The tool will provide clear feedback to users about what changes will be made and report on the success of operations.

## Architecture

The system follows a simple pipeline architecture:

1. **Input Validation** - Validates the folder path and checks for existence
2. **File Discovery** - Scans the directory and identifies files to rename
3. **Rename Planning** - Generates new filenames based on the naming pattern
4. **Preview Display** - Shows users the planned changes
5. **Execution** - Performs the actual file renaming operations
6. **Result Reporting** - Reports success/failure statistics

The implementation will use Python's built-in `os` and `pathlib` modules for file system operations, ensuring cross-platform compatibility.

## Components and Interfaces

### FileRenamer Class

The main class that orchestrates the renaming process.

**Methods:**
- `__init__(folder_path: str, pattern: str = "photo{n}")` - Initializes the renamer with folder path and naming pattern
- `validate_folder() -> bool` - Validates that the input folder exists
- `discover_files() -> List[Path]` - Finds all files in the folder
- `generate_rename_plan() -> List[Tuple[Path, Path]]` - Creates mapping of old to new filenames
- `preview_changes() -> None` - Displays the planned rename operations
- `execute_renames() -> Dict[str, int]` - Performs the renaming and returns statistics
- `run() -> None` - Main entry point that executes the full pipeline

### Helper Functions

- `normalize_extension(ext: str) -> str` - Converts file extensions to lowercase
- `extract_numeric_order(filename: str) -> int` - Extracts numeric value from filename for sorting
- `handle_name_conflict(target_path: Path) -> Path` - Resolves filename conflicts by appending suffixes

## Data Models

### RenameOperation

A data structure representing a single rename operation:

```python
@dataclass
class RenameOperation:
    source: Path          # Original file path
    target: Path          # New file path
    status: str          # 'pending', 'success', 'failed'
    error: Optional[str] # Error message if failed
```

### RenameResult

Statistics about the renaming operation:

```python
@dataclass
class RenameResult:
    total_files: int
    successful: int
    failed: int
    skipped: int
    errors: List[str]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After reviewing the prework analysis, I've identified the following redundancies:
- Properties 3.1 and 3.2 are specific cases of property 2.3 (extension normalization)
- These will be consolidated into a single comprehensive property about extension normalization

The remaining properties provide unique validation value and will be included.

### Properties

Property 1: Folder validation correctness
*For any* folder path provided as input, the validation function should return true if and only if the folder exists on the filesystem
**Validates: Requirements 1.1**

Property 2: Valid folder processing
*For any* existing folder path, the File Renamer should successfully identify and list files within that folder
**Validates: Requirements 1.3**

Property 3: Naming pattern compliance
*For any* set of files processed, all renamed files should match the pattern "photo{number}.{extension}" where number is a positive integer
**Validates: Requirements 2.1**

Property 4: Sequential numbering
*For any* set of files renamed, the numbers assigned should form a sequence starting at 1 with no gaps (1, 2, 3, ..., n)
**Validates: Requirements 2.2**

Property 5: Extension normalization
*For any* file with any case variation in its extension, the renamed file should have the extension converted to lowercase
**Validates: Requirements 2.3, 3.1, 3.2**

Property 6: Extension type preservation
*For any* file being renamed, the file extension type should remain the same (e.g., .PNG becomes .png, not .jpg)
**Validates: Requirements 3.3**

Property 7: Numeric order preservation
*For any* set of files with numeric names, the relative ordering by number should be preserved in the renamed files
**Validates: Requirements 2.4**

Property 8: No file overwriting
*For any* rename operation where the target filename already exists, the system should not overwrite the existing file
**Validates: Requirements 4.1**

Property 9: Error reporting accuracy
*For any* rename operation that fails, the system should include that file in the error report
**Validates: Requirements 4.2**

Property 10: Success count accuracy
*For any* completed rename operation, the reported count of successful renames should equal the actual number of files successfully renamed
**Validates: Requirements 4.3**

Property 11: Preview completeness
*For any* set of files to be renamed, the preview should display both the current and proposed filename for each file
**Validates: Requirements 5.1**

Property 12: Count display accuracy
*For any* preview operation, the displayed total count should match the actual number of files to be processed
**Validates: Requirements 5.2**

## Error Handling

The system will handle the following error conditions:

1. **Invalid Folder Path** - If the specified folder doesn't exist, display an error message and exit gracefully
2. **Permission Errors** - If the system lacks permissions to read or rename files, report the specific files affected
3. **Name Conflicts** - If a target filename already exists, append a suffix (e.g., "_1", "_2") to avoid overwriting
4. **File System Errors** - Catch and report any OS-level errors during file operations
5. **Empty Folder** - If no files are found, inform the user and exit without error

All errors will be logged with clear messages indicating what went wrong and which files were affected.

## Testing Strategy

### Unit Testing

Unit tests will cover:
- Folder validation logic with valid and invalid paths
- Extension normalization function with various case combinations
- Numeric extraction from filenames
- Conflict resolution logic
- Result statistics calculation

### Property-Based Testing

We will use **Hypothesis** (Python's property-based testing library) for testing universal properties.

Each property-based test will:
- Run a minimum of 100 iterations
- Be tagged with a comment referencing the design document property
- Use the format: `# Feature: file-renamer, Property {number}: {property_text}`

Property-based tests will verify:
- Property 1: Folder validation correctness across random paths
- Property 3: Naming pattern compliance across random file sets
- Property 4: Sequential numbering across various file counts
- Property 5: Extension normalization across all case variations
- Property 6: Extension type preservation across different file types
- Property 7: Numeric order preservation across random numeric filenames
- Property 8: No overwriting when conflicts exist
- Property 10: Success count accuracy across various scenarios
- Property 11: Preview completeness across random file sets
- Property 12: Count display accuracy across different file counts

### Integration Testing

Integration tests will verify:
- End-to-end renaming workflow with real file system operations
- Preview display followed by execution
- Error handling in realistic scenarios

## Implementation Notes

- Use `pathlib.Path` for cross-platform file path handling
- Sort files by extracting numeric values to preserve ordering
- Implement dry-run mode for testing without actual file changes
- Use atomic operations where possible to prevent partial failures
- Provide verbose output option for debugging
