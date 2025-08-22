#!/usr/bin/env python3
"""
Codebase Cleanup Script for AI Career Mentor Hackathon Project
Removes unnecessary files after Django + RAG implementation
"""

import os
import shutil
from pathlib import Path

def cleanup_codebase():
    """Remove unnecessary files from the codebase"""
    
    # Files to remove
    files_to_remove = [
        # Streamlit files (replaced by Django)
        "src/app.py",
        "src/app_simple.py", 
        "src/test_app.py",
        "src/config.py",
        
        # Terminal/development files
        "career_mentor.py",
        "test_simple.py",
        
        # Test files (development artifacts)
        "tests/test_resume_parser.py",
        "tests/interactive_test.py", 
        "tests/test_vector_store.py",
        "tests/test_retriever.py",
        "tests/test_app.py",
        "tests/test_chatbot.py",
        
        # Jupyter notebooks (development)
        "notebooks/data_exploration.ipynb",
        "notebooks/rag_experiments.ipynb", 
        "notebooks/embeddings_test.ipynb",
        
        # Old chatbot files (replaced by RAG)
        "src/chatbot/career_bot.py",
        "src/chatbot/prompts.py",
        
        # Duplicate resume
        "tests/Resume.pdf",
    ]
    
    # Directories to remove
    dirs_to_remove = [
        "src/__pycache__",
        "tests/__pycache__", 
        "src/chatbot/__pycache__",
        "src/rag/__pycache__",
        "src/utils/__pycache__",
        ".idea",  # IDE files
    ]
    
    print("🧹 AI Career Mentor - Codebase Cleanup")
    print("=" * 50)
    
    # Remove files
    removed_files = []
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                removed_files.append(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
        else:
            print(f"⚠️  Not found: {file_path}")
    
    # Remove directories
    removed_dirs = []
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                removed_dirs.append(dir_path)
                print(f"✅ Removed directory: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to remove directory {dir_path}: {e}")
        else:
            print(f"⚠️  Directory not found: {dir_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Cleanup Summary:")
    print(f"   Files removed: {len(removed_files)}")
    print(f"   Directories removed: {len(removed_dirs)}")
    
    if removed_files:
        print(f"\n🗑️  Removed files:")
        for file in removed_files:
            print(f"   - {file}")
    
    if removed_dirs:
        print(f"\n🗑️  Removed directories:")
        for dir in removed_dirs:
            print(f"   - {dir}")
    
    print(f"\n✅ Your codebase is now clean!")
    print(f"📁 Essential files kept:")
    print(f"   - Django app (career_mentor_web/, career_advisor/)")
    print(f"   - RAG pipeline (src/rag/, src/utils/)")
    print(f"   - Templates and static files")
    print(f"   - Requirements and documentation")
    
    # Calculate space saved
    total_size = 0
    for file in removed_files:
        try:
            total_size += os.path.getsize(file)
        except:
            pass
    
    if total_size > 0:
        print(f"\n💾 Space saved: {total_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    # Ask for confirmation
    print("This script will remove unnecessary files from your AI Career Mentor project.")
    print("These files are no longer needed after implementing the Django + RAG solution.")
    print("\nFiles to be removed include:")
    print("- Old Streamlit apps")
    print("- Development test files") 
    print("- Jupyter notebooks")
    print("- Terminal-based career mentor")
    print("- Python cache directories")
    print("- IDE files")
    
    response = input("\nDo you want to proceed with cleanup? (y/N): ")
    if response.lower() in ['y', 'yes']:
        cleanup_codebase()
    else:
        print("Cleanup cancelled.") 