#! /bin/sh

if [ -f "pyenv" ]; then
    echo "Stack Visualizer has already been set up"
    exit 1
fi

python3 -m venv pyenv
# shellcheck disable=SC3046
# shellcheck disable=SC1091
source pyenv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install pygame-ce