# go_outdoors_learning

This GitHub repository contains the code needed to quickly create plots measuring a student's before and after knowledge and interest gained from an excel file. The output is a plot for each topic that has a knowledge before and after questions and an interest question.

## Getting Started

First, make sure you have Git installed. If you don't have git installed, you can download it from the official Git website.
Note: If you are experienced with Git and Github, feel free to skip to the requirements section after cloning the repository.
If you are on Mac or Linux, open a new terminal, navigate to the folder where you want to have the repository, and clone the repository using:

```shell
git clone https://github.com/marshallyale/go_outdoors_learning.git
```

If you are on Windows, you should install Windows Subsystem for Linux from the Microsoft Store, open up a WSL terminal, navigate to the folder where you want the repository, and clone the repository using:

```shell
git clone https://github.com/marshallyale/go_outdoors_learning.git
```

## Requirements

You should have Python3 >= 3.7
After cloning:

```shell
cd go_outdoors_learning
pip install -r requirements.txt
```

## Usage

Make sure you are in the same directory as the script. Then run the script using:

```shell
python3 outreach_plot_generator.py -f <path_to_csv_file>
```

Note: You must specify the correct relative or full path to the csv file and the file MUST be a csv file

You can also run the command with the -s flag which will use the scale (e.g. 1=Nothing, 2=A little, etc.) internal to Python to create the plots instead of trying to find the scale from the csv file. 
```shell
python3 outreach_plot_generator.py -f <path_to_csv_file> -s
```

## Results

Each plot will be saved inside the plots folder.
