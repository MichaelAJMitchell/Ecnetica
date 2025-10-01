def process_directory(self, directory_path: str, output_file: str):
    """Process all supported files in a directory."""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    supported_files = []
    for root, dirs, files in os.walk(directory_path):
        # Sort directories for consistent traversal order
        dirs.sort()
        # Sort files for consistent processing order
        files.sort()
        
        for file in files:
            file_path = os.path.join(root, file)
            if self.file_processor.is_supported(file_path):
                supported_files.append(file_path)
    
    # Sort the final list for completely predictable order
    supported_files.sort()
    
    print(f"Found {len(supported_files)} supported files to process")
    
    for file_path in supported_files:
        try:
            self.process_file(file_path, output_file)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue