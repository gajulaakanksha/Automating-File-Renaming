# Implementation Plan

- [x] 1. Set up project structure and core utilities





  - Create main Python script file `file_renamer.py`
  - Import required modules (pathlib, os, dataclasses, typing)
  - Set up basic project structure with proper imports
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Implement data models




  - Create `RenameOperation` dataclass with source, target, status, and error fields
  - Create `RenameResult` dataclass with statistics fields
  - _Requirements: 4.2, 4.3_

- [x] 3. Implement helper functions





  - Write `normalize_extension()` function to convert extensions to lowercase
  - Write `extract_numeric_order()` function to extract numbers from filenames
  - Write `handle_name_conflict()` function to resolve filename conflicts
  - _Requirements: 2.3, 2.4, 3.1, 3.2, 4.1_

- [ ]* 3.1 Write property test for extension normalization
  - **Property 5: Extension normalization**
  - **Validates: Requirements 2.3, 3.1, 3.2**

- [ ]* 3.2 Write property test for conflict handling
  - **Property 8: No file overwriting**
  - **Validates: Requirements 4.1**

- [x] 4. Implement FileRenamer class initialization and validation





  - Create `FileRenamer` class with `__init__` method
  - Implement `validate_folder()` method to check folder existence
  - _Requirements: 1.1, 1.2_

- [ ]* 4.1 Write property test for folder validation
  - **Property 1: Folder validation correctness**
  - **Validates: Requirements 1.1**

- [x] 5. Implement file discovery




  - Implement `discover_files()` method to scan directory and list files
  - Sort files by numeric order using `extract_numeric_order()`
  - _Requirements: 1.3, 2.4_

- [ ]* 5.1 Write property test for valid folder processing
  - **Property 2: Valid folder processing**
  - **Validates: Requirements 1.3**

- [ ]* 5.2 Write property test for numeric order preservation
  - **Property 7: Numeric order preservation**
  - **Validates: Requirements 2.4**


- [x] 6. Implement rename planning



  - Implement `generate_rename_plan()` method to create old-to-new filename mappings
  - Apply naming pattern "photo{n}.{ext}" with sequential numbering
  - Use `normalize_extension()` for each file
  - Handle conflicts using `handle_name_conflict()`
  - _Requirements: 2.1, 2.2, 2.3, 3.3, 4.1_

- [ ]* 6.1 Write property test for naming pattern compliance
  - **Property 3: Naming pattern compliance**
  - **Validates: Requirements 2.1**

- [ ]* 6.2 Write property test for sequential numbering
  - **Property 4: Sequential numbering**
  - **Validates: Requirements 2.2**

- [ ]* 6.3 Write property test for extension type preservation
  - **Property 6: Extension type preservation**
  - **Validates: Requirements 3.3**

- [x] 7. Implement preview display





  - Implement `preview_changes()` method to display rename operations
  - Show current filename and proposed new filename for each file
  - Display total count of files to be processed
  - _Requirements: 5.1, 5.2_

- [ ]* 7.1 Write property test for preview completeness
  - **Property 11: Preview completeness**
  - **Validates: Requirements 5.1**

- [ ]* 7.2 Write property test for count display accuracy
  - **Property 12: Count display accuracy**
  - **Validates: Requirements 5.2**


- [x] 8. Implement rename execution




  - Implement `execute_renames()` method to perform actual file renaming
  - Track success/failure for each operation
  - Return `RenameResult` with statistics
  - Handle and report errors for failed operations
  - _Requirements: 4.2, 4.3_

- [ ]* 8.1 Write property test for error reporting accuracy
  - **Property 9: Error reporting accuracy**
  - **Validates: Requirements 4.2**

- [ ]* 8.2 Write property test for success count accuracy
  - **Property 10: Success count accuracy**
  - **Validates: Requirements 4.3**

- [x] 9. Implement main execution flow





  - Implement `run()` method that orchestrates the full pipeline
  - Call validation, discovery, planning, preview, and execution in sequence
  - Handle errors at each stage gracefully
  - _Requirements: 1.1, 1.2, 1.3, 5.3_

- [x] 10. Create command-line interface




  - Add argument parsing for folder path input
  - Add main entry point with `if __name__ == "__main__"`
  - Display final results and statistics
  - _Requirements: 1.1, 4.3_

- [ ]* 11. Write integration tests
  - Test end-to-end workflow with temporary test directories
  - Test error handling scenarios
  - Test edge cases (empty folder, permission errors, etc.)

- [x] 12. Checkpoint - Ensure all tests pass







  - Ensure all tests pass, ask the user if questions arise.
