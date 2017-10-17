**The eye is the window to the brain: as researchers, we can tell a lot from where, and how, people look around. Recently, there has been an uptick in interest in what the pupil's fluctuations can tell us about the state of people's brains. But how can you make sure that you're doing the right experiment to answer your research question?**

# Eyetracking Course
This repo contains the materials for a two-day eye-tracking course at the graduate level. For data files, it uses `git-lfs`, so this needs to be installed. 

We are at present developing the experiments and materials for the course. The first iteration of this course will be held on October 19-20 2017 at the Vrije Universiteit Amsterdam. The course is open to anyone, official [EPOS](https://www.eposgradnet.nl) credits can be received after succesful completion.

# Experiments
Some ready-made experiments will be available based on our own experiment backend. They are stored in the [notebooks](notebooks/README.md) folder. This will allow you to quickly acquire some data that is stored in a standard format. You are free to use our experimental examples as a basis for your own. 

# Conversion and preprocessing
We'll be using an [SR Research Eyelink 1000 eyetracker](http://www.sr-research.com/), which stores its data in the proprietary .edf format. We have created a package that takes these edf files and converts them into hdf5 files - a more open format. This package, [hedfpy](https://github.com/tknapen/hedfpy), requires some specific triggers so that data can be analyzed easily. Furthermore, it performs specific types of preprocessing which are especially suited for subsequent pupil dilation analyses. 

# Analysis
[Hedfpy](https://github.com/tknapen/hedfpy) allows easy access to raw and preprocessed eye tracking data. The analysis of gaze traces, for example, is then made a lot easier, meaning that we can show you how to analyze these data in the Jupyter Notebooks in the [notebooks](notebooks/README.md) folder. 

# Syllabus 

For more information on the first edition of this short course, please consult the [syllabus](syllabus/syllabus.md) (under construction).

# Install procedure
It may be necessary to perform these steps once the jupyterhub server goes down.

```
#!/usr/bin/env bash

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
```