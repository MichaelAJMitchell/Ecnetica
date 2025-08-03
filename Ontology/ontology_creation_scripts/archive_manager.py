#!/usr/bin/env python3
"""
Archive Manager for Mathematical Concept Scraper

Handles archiving of existing knowledge graph files before creating new ones.
"""

import os
import shutil
import glob
from datetime import datetime
from typing import List

def archive_existing_files(ontology_dir: str, archive_dir: str) -> str:
    """
    Archive existing knowledge graph CSV files to a timestamped folder.
    
    Args:
        ontology_dir: Path to the Ontology directory
        archive_dir: Path to the ontology_archive directory
        
    Returns:
        Path to the created archive folder
    """
    # Create timestamp for the archive folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_folder = os.path.join(archive_dir, f"archive_{timestamp}")
    
    # Create the archive folder
    os.makedirs(archive_folder, exist_ok=True)
    
    # Find CSV files with 'concepts' or 'relationships' in the name
    csv_files = []
    
    # Search for concept files
    concept_pattern = os.path.join(ontology_dir, "*concepts*.csv")
    csv_files.extend(glob.glob(concept_pattern))
    
    # Search for relationship files
    relationship_pattern = os.path.join(ontology_dir, "*relationships*.csv")
    csv_files.extend(glob.glob(relationship_pattern))
    
    # Remove duplicates
    csv_files = list(set(csv_files))
    
    if not csv_files:
        print("No existing knowledge graph files found to archive.")
        return archive_folder
    
    print(f"Found {len(csv_files)} existing knowledge graph files to archive:")
    
    # Move files to archive folder
    for file_path in csv_files:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            archive_path = os.path.join(archive_folder, filename)
            
            try:
                shutil.move(file_path, archive_path)
                print(f"  ✓ Archived: {filename}")
            except Exception as e:
                print(f"  ✗ Failed to archive {filename}: {str(e)}")
    
    print(f"Files archived to: {archive_folder}")
    return archive_folder

def ensure_archive_directory(archive_dir: str) -> None:
    """
    Ensure the archive directory exists.
    
    Args:
        archive_dir: Path to the archive directory
    """
    os.makedirs(archive_dir, exist_ok=True) 