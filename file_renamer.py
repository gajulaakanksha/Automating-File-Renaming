"""
File Renamer - A utility to rename files in a directory with a consistent naming pattern.

This tool processes files in a specified folder and renames them according to a
sequential pattern (e.g., photo1.png, photo2.png, etc.).
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict


@dataclass
class RenameOperation:
    """Represents a single file rename operation."""
    source: Path
    target: Path
    status: str
    error: Optional[str] = None


@dataclass
class RenameResult:
    """Statistics about the renaming operation."""
    total_files: int
    successful: int
    failed: int
    skipped: int
    errors: List[str]


def normalize_extension(ext: str) -> str:
    """
    Convert file extension to lowercase.
    
    Args:
        ext: File extension (with or without leading dot)
        
    Returns:
        Lowercase extension with leading dot
        
    Examples:
        >>> normalize_extension('.PNG')
        '.png'
        >>> normalize_extension('PNG')
        '.png'
        >>> normalize_extension('.JpG')
        '.jpg'
    """
    # Ensure extension has a leading dot
    if not ext.startswith('.'):
        ext = '.' + ext
    return ext.lower()


def extract_numeric_order(filename: str) -> int:
    """
    Extract numeric value from filename for sorting purposes.
    
    Args:
        filename: The filename to extract number from
        
    Returns:
        Integer value extracted from filename, or 0 if no number found
        
    Examples:
        >>> extract_numeric_order('1.PNG')
        1
        >>> extract_numeric_order('10.PNG')
        10
        >>> extract_numeric_order('photo5.jpg')
        5
        >>> extract_numeric_order('noNumber.txt')
        0
    """
    import re
    # Extract all numeric sequences from the filename
    numbers = re.findall(r'\d+', filename)
    if numbers:
        # Return the first number found
        return int(numbers[0])
    return 0


def handle_name_conflict(target_path: Path) -> Path:
    """
    Resolve filename conflicts by appending a suffix.
    
    If the target path already exists, append _1, _2, etc. until
    a non-existing filename is found.
    
    Args:
        target_path: The desired target path
        
    Returns:
        A Path object that doesn't conflict with existing files
        
    Examples:
        If 'photo1.png' exists, returns 'photo1_1.png'
        If 'photo1_1.png' also exists, returns 'photo1_2.png'
    """
    if not target_path.exists():
        return target_path
    
    # Split the filename into stem and suffix
    stem = target_path.stem
    suffix = target_path.suffix
    parent = target_path.parent
    
    # Try appending _1, _2, _3, etc. until we find a non-existing filename
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


class FileRenamer:
    """
    Main class that orchestrates the file renaming process.
    
    This class handles validation, file discovery, rename planning,
    preview display, and execution of file renaming operations.
    """
    
    def __init__(self, folder_path: str, pattern: str = "photo{n}"):
        """
        Initialize the FileRenamer with a folder path and naming pattern.
        
        Args:
            folder_path: Path to the folder containing files to rename
            pattern: Naming pattern template (default: "photo{n}")
                    {n} will be replaced with sequential numbers
        
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> renamer = FileRenamer("./images", "image{n}")
        """
        self.folder_path = Path(folder_path)
        self.pattern = pattern
        self.rename_operations: List[RenameOperation] = []
    
    def validate_folder(self) -> bool:
        """
        Validate that the input folder exists.
        
        Returns:
            True if the folder exists and is a directory, False otherwise
            
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> renamer.validate_folder()
            True
            >>> renamer = FileRenamer("./nonexistent")
            >>> renamer.validate_folder()
            False
        """
        return self.folder_path.exists() and self.folder_path.is_dir()
    
    def discover_files(self) -> List[Path]:
        """
        Scan the directory and identify files to rename.
        
        This method lists all files in the folder (excluding subdirectories)
        and sorts them by numeric order extracted from their filenames.
        
        Returns:
            List of Path objects representing files, sorted by numeric order
            
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> files = renamer.discover_files()
            >>> # Returns files sorted: 1.PNG, 2.PNG, ..., 10.PNG
        """
        # Get all items in the folder
        all_items = list(self.folder_path.iterdir())
        
        # Filter to only include files (not directories)
        files = [item for item in all_items if item.is_file()]
        
        # Sort files by numeric order using extract_numeric_order
        files.sort(key=lambda f: extract_numeric_order(f.name))
        
        return files
    
    def generate_rename_plan(self) -> List[RenameOperation]:
        """
        Generate a plan for renaming files based on the naming pattern.
        
        This method creates a mapping of old filenames to new filenames,
        applying sequential numbering and normalizing extensions. It also
        handles potential filename conflicts.
        
        Returns:
            List of RenameOperation objects representing the rename plan
            
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> plan = renamer.generate_rename_plan()
            >>> # Returns operations like: 1.PNG -> photo1.png, 2.PNG -> photo2.png
        """
        # Discover files to rename
        files = self.discover_files()
        
        operations = []
        
        # Generate new filenames with sequential numbering
        for index, file_path in enumerate(files, start=1):
            # Get the file extension and normalize it
            extension = normalize_extension(file_path.suffix)
            
            # Apply the naming pattern (replace {n} with the sequential number)
            new_name = self.pattern.replace("{n}", str(index)) + extension
            
            # Create the target path in the same directory
            target_path = self.folder_path / new_name
            
            # Handle potential filename conflicts
            target_path = handle_name_conflict(target_path)
            
            # Create a RenameOperation for this file
            operation = RenameOperation(
                source=file_path,
                target=target_path,
                status='pending',
                error=None
            )
            
            operations.append(operation)
        
        # Store the operations for later use
        self.rename_operations = operations
        
        return operations
    
    def preview_changes(self) -> None:
        """
        Display the planned rename operations to the user.
        
        This method shows the current filename and proposed new filename
        for each file, along with the total count of files to be processed.
        It provides a preview before any actual renaming occurs.
        
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> renamer.generate_rename_plan()
            >>> renamer.preview_changes()
            # Displays:
            # Preview of rename operations:
            # 1.PNG -> photo1.png
            # 2.PNG -> photo2.png
            # ...
            # Total files to be processed: 10
        """
        if not self.rename_operations:
            print("No rename operations planned. Run generate_rename_plan() first.")
            return
        
        print("\nPreview of rename operations:")
        print("-" * 60)
        
        # Display each rename operation
        for operation in self.rename_operations:
            current_name = operation.source.name
            new_name = operation.target.name
            print(f"{current_name} -> {new_name}")
        
        print("-" * 60)
        # Display total count
        total_count = len(self.rename_operations)
        print(f"Total files to be processed: {total_count}")
        print()
    
    def execute_renames(self) -> RenameResult:
        """
        Execute the planned rename operations.
        
        This method performs the actual file renaming, tracking success and
        failure for each operation. It handles errors gracefully and returns
        detailed statistics about the operation.
        
        Returns:
            RenameResult object containing statistics about the operation
            
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> renamer.generate_rename_plan()
            >>> result = renamer.execute_renames()
            >>> print(f"Successfully renamed {result.successful} files")
        """
        if not self.rename_operations:
            # No operations to execute
            return RenameResult(
                total_files=0,
                successful=0,
                failed=0,
                skipped=0,
                errors=[]
            )
        
        successful_count = 0
        failed_count = 0
        skipped_count = 0
        error_messages = []
        
        # Execute each rename operation
        for operation in self.rename_operations:
            try:
                # Check if source file still exists
                if not operation.source.exists():
                    operation.status = 'failed'
                    error_msg = f"Source file not found: {operation.source.name}"
                    operation.error = error_msg
                    error_messages.append(error_msg)
                    failed_count += 1
                    continue
                
                # Check if source and target are the same (no rename needed)
                if operation.source == operation.target:
                    operation.status = 'skipped'
                    skipped_count += 1
                    continue
                
                # Perform the rename operation
                operation.source.rename(operation.target)
                operation.status = 'success'
                successful_count += 1
                
            except PermissionError as e:
                # Handle permission errors
                operation.status = 'failed'
                error_msg = f"Permission denied for {operation.source.name}: {str(e)}"
                operation.error = error_msg
                error_messages.append(error_msg)
                failed_count += 1
                
            except OSError as e:
                # Handle other OS-level errors
                operation.status = 'failed'
                error_msg = f"Failed to rename {operation.source.name}: {str(e)}"
                operation.error = error_msg
                error_messages.append(error_msg)
                failed_count += 1
                
            except Exception as e:
                # Catch any unexpected errors
                operation.status = 'failed'
                error_msg = f"Unexpected error renaming {operation.source.name}: {str(e)}"
                operation.error = error_msg
                error_messages.append(error_msg)
                failed_count += 1
        
        # Create and return the result
        total_files = len(self.rename_operations)
        result = RenameResult(
            total_files=total_files,
            successful=successful_count,
            failed=failed_count,
            skipped=skipped_count,
            errors=error_messages
        )
        
        return result
    
    def run(self) -> None:
        """
        Main entry point that orchestrates the full file renaming pipeline.
        
        This method executes the complete workflow:
        1. Validates the input folder
        2. Discovers files to rename
        3. Generates the rename plan
        4. Displays a preview of changes
        5. Executes the rename operations
        6. Reports the results
        
        Errors at each stage are handled gracefully with appropriate messages.
        
        Examples:
            >>> renamer = FileRenamer("./photos")
            >>> renamer.run()
            # Executes the full pipeline and displays results
        """
        print("=" * 60)
        print("File Renamer - Starting Process")
        print("=" * 60)
        
        # Step 1: Validate folder
        print(f"\n[1/5] Validating folder: {self.folder_path}")
        if not self.validate_folder():
            print(f"ERROR: Folder does not exist or is not a directory: {self.folder_path}")
            print("Process aborted.")
            return
        print("✓ Folder validation successful")
        
        # Step 2: Discover files
        print(f"\n[2/5] Discovering files in folder...")
        try:
            files = self.discover_files()
            if not files:
                print("No files found in the folder.")
                print("Process completed - nothing to rename.")
                return
            print(f"✓ Found {len(files)} file(s)")
        except PermissionError:
            print(f"ERROR: Permission denied when accessing folder: {self.folder_path}")
            print("Process aborted.")
            return
        except Exception as e:
            print(f"ERROR: Failed to discover files: {str(e)}")
            print("Process aborted.")
            return
        
        # Step 3: Generate rename plan
        print(f"\n[3/5] Generating rename plan...")
        try:
            operations = self.generate_rename_plan()
            print(f"✓ Generated rename plan for {len(operations)} file(s)")
        except Exception as e:
            print(f"ERROR: Failed to generate rename plan: {str(e)}")
            print("Process aborted.")
            return
        
        # Step 4: Preview changes
        print(f"\n[4/5] Previewing changes...")
        try:
            self.preview_changes()
        except Exception as e:
            print(f"ERROR: Failed to display preview: {str(e)}")
            print("Process aborted.")
            return
        
        # Step 5: Execute renames
        print(f"[5/5] Executing rename operations...")
        try:
            result = self.execute_renames()
            
            # Report results
            print("\n" + "=" * 60)
            print("Rename Operation Complete")
            print("=" * 60)
            print(f"Total files processed: {result.total_files}")
            print(f"Successfully renamed: {result.successful}")
            print(f"Skipped (no change): {result.skipped}")
            print(f"Failed: {result.failed}")
            
            # Display errors if any
            if result.errors:
                print("\nErrors encountered:")
                for error in result.errors:
                    print(f"  - {error}")
            else:
                print("\n✓ All operations completed successfully!")
            
            print("=" * 60)
            
        except Exception as e:
            print(f"ERROR: Failed during execution: {str(e)}")
            print("Process aborted.")
            return


def main():
    """
    Main entry point for the command-line interface.
    
    Parses command-line arguments and executes the file renaming process.
    """
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='File Renamer - Rename files in a directory with a consistent naming pattern',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python file_renamer.py ./photos
  python file_renamer.py "C:\\Users\\Documents\\photos"
  python file_renamer.py ./images --pattern "image{n}"
        """
    )
    
    # Add folder path argument (required)
    parser.add_argument(
        'folder',
        type=str,
        help='Path to the folder containing files to rename'
    )
    
    # Add optional pattern argument
    parser.add_argument(
        '--pattern',
        type=str,
        default='photo{n}',
        help='Naming pattern template (default: photo{n}). Use {n} for sequential numbers.'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create FileRenamer instance and run
    renamer = FileRenamer(args.folder, args.pattern)
    renamer.run()


if __name__ == "__main__":
    main()
