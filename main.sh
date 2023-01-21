#!/bin/bash

module="telethon"

# Check if module is installed
if python -c "import $module" ; then
    echo "Dependencies Found."
else
    echo "Installing Dependencies..."
    pip3 install -r requirements.txt
fi

# Run Python script
python3 run.py
