#!/usr/bin/env python3
"""
Example 1: List Atom Types

This script demonstrates how to list all atom types in the MeTTa space.
"""

from hyperon import MeTTa
from connect import load_all, print_atom_types

def main():
    print("=" * 60)
    print("Example 1: List Atom Types")
    print("=" * 60)
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("\nLoading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # List atom types (use verify_existence=False to avoid panics)
    print_atom_types(interp, verify_existence=False)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()

