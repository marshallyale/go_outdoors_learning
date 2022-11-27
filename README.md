# go_outdoors_learning

This GitHub repository contains the code needed to quickly create plots measuring a student's before and after knowledge and interest gained from an excel file. The output is a plot for each sheet in the excel file which corresponds to the name in the excel file

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
python3 outreach_plot_generator.py -f <path_to_excel_file>
```

Note: You must specify the correct relative or full path to the excel file

## Results

Each plot will be saved inside the plots folder. If you need to adjust the location of the titles of the plots, look at lines 91 and 92 inside the outreach_plot_generator.py file.
