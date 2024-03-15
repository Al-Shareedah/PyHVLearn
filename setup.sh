#!/bin/bash

# Check for Homebrew, install if we don't have it
if test ! $(which brew); then
    echo "Installing homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Update Homebrew
brew update

# Install Python3 if not already installed
if test ! $(which python3); then
    echo "Installing Python 3..."
    brew install python
fi

# Install Graphviz for visualize_automaton (if aalpy or your code uses it)
echo "Installing Graphviz..."
brew install graphviz

# Create a virtual environment in the current directory
echo "Setting up virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install numpy
pip install aalpy
pip install matplotlib # If you're using it for visualization

echo "Setup complete! Virtual environment is ready."
echo "To activate the virtual environment, run 'source venv/bin/activate' in this directory."