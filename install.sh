#!/usr/bin/env bash

# script to update/install all necessary prerequisites for our eyetracking course
conda install seaborn pytables
pip install hedfpy==0.0.dev3 fir==0.1 mne lmfit 

git clone https://github.com/tknapen/eyetracking_course.git
cd eyetracking_course
git lfs fetch --all