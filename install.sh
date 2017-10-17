#!/usr/bin/env bash

# script to update/install all necessary prerequisites for our eyetracking course
pip install hedfpy==0.0.dev3 fir mne lmfit 
conda install seaborn pytables
# conda install -c conda-forge nbgrader
# jupyter nbextension enable nbgrader --py --sys-prefix

mkdir Downloads
cd Downloads 
wget https://github.com/git-lfs/git-lfs/releases/download/v2.3.3/git-lfs-linux-amd64-2.3.3.tar.gz
tar xvzf git-lfs-linux-amd64-2.3.3.tar.gz
cd git-lfs-2.3.3/

mkdir ~/bin
cp git-lfs ~/bin
export PATH=$HOME/bin:$PATH
git install git-lfs

git clone https://github.com/tknapen/eyetracking_course.git
cd eyetracking_course
git lfs fetch --all