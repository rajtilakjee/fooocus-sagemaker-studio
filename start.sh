#!/bin/bash
# This script is a setup script for a project called Fooocus.

# Check if the directory "Fooocus" doesn't exist.
if [ ! -d "Fooocus" ]
then
  # If it doesn't exist, clone the Fooocus Git repository.
  git clone https://github.com/lllyasviel/Fooocus.git
  # Alternative Git clone commands (commented out).
  # git clone --depth 1 --branch V2 https://github.com/lllyasviel/Fooocus.git
  # Create the config file pointing the checkpoints to checkpoints-real-folder
fi

# Change the current working directory to "Fooocus" and update the local repository.
cd Fooocus
git pull

# Check if a symbolic link to "~/.conda/envs/fooocus" doesn't exist.
if [ ! -L ~/.conda/envs/fooocus ]
then
    # If it doesn't exist, create a symbolic link to "/tmp/fooocus".
    ln -s /tmp/fooocus ~/.conda/envs/
fi

# Set up conda environment in the current shell session.
eval "$(conda shell.bash hook)"

# Check if the directory "/tmp/fooocus" doesn't exist.
if [ ! -d /tmp/fooocus ]
then
    # If it doesn't exist, create the directory and set up the conda environment.
    mkdir /tmp/fooocus
    conda env create -f environment.yaml
    conda activate fooocus
    pwd
    ls
    # Install Python packages and dependencies.
    pip install -r requirements_versions.txt
    pip install torch torchvision --force-reinstall --index-url https://download.pytorch.org/whl/cu117
    pip install pyngrok
    conda install glib -y
    # Remove pip cache.
    rm -rf ~/.cache/pip
fi

# Set variables for current and model folders.
current_folder=$(pwd)
model_folder=${current_folder}/models/checkpoints-real-folder

# Check if the file "config.txt" doesn't exist.
if [ ! -e config.txt ]
then
  # If it doesn't exist, create a JSON string with the "path_checkpoints" set to "model_folder" and write it to "config.txt".
  json_data="{ \"path_checkpoints\": \"$model_folder\" }"
  echo "$json_data" > config.txt
  echo "JSON file created: config.txt"
else
  # If "config.txt" exists, update the "path_checkpoints" value in the JSON file using the "jq" tool.
  echo "Updating config.txt to use checkpoints-real-folder"
  jq --arg new_value "$model_folder" '.path_checkpoints = $new_value' config.txt > config_tmp.txt && mv config_tmp.txt config.txt
fi

# Check if the symbolic link to "models/checkpoints" doesn't exist.
if [ ! -L models/checkpoints ]
then
    # If it doesn't exist, move the "checkpoints" folder to "checkpoints-real-folder" and create a symbolic link.
    mv models/checkpoints models/checkpoints-real-folder
    ln -s models/checkpoints-real-folder models/checkpoints
fi

# Activate the "fooocus" conda environment and change the working directory to its parent.
conda activate fooocus
cd ..

# Check the number of command-line arguments.
if [ $# -eq 0 ]
then
  # If there are no arguments, run the "start-ngrok.py" Python script.
  python start-ngrok.py 
# Check if the first argument is "reset".
elif [ $1 = "reset" ]
then
  # If the first argument is "reset", run the "start-ngrok.py" script with the "--reset" option.
  python start-ngrok.py --reset 
fi
