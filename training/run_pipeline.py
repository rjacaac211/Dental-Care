#!/usr/bin/env python
import os
import sys

def main():
    print("Starting the pipeline...")

    # Determine the project root (assumes run_pipeline.py is at the project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, 'src')

    # Ensure the src directory is in sys.path so that we can import modules from it
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Import the main functions from each module
    try:
        from preprocess import main as preprocess_main
        from train import main as train_main
        from test import main as test_main
    except ImportError as e:
        print("Error importing modules from 'src'. Please ensure your module names and paths are correct.")
        raise e

    # Run data preprocessing
    print("\n[1/3] Running data preprocessing...")
    preprocess_main()
    print("Data preprocessing completed.\n")

    # Run model training
    print("[2/3] Running model training...")
    train_main()
    print("Model training completed.\n")

    # Run model testing/evaluation
    print("[3/3] Running model testing...")
    test_main()
    print("Model testing completed.\n")

    print("Pipeline execution finished successfully.")

if __name__ == '__main__':
    main()
