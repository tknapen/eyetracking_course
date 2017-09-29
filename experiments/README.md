# Experiments
We've made some experiments that will get us started during the course. The experiments are simple designs, implemented in [our own little experimental tools](https://github.com/Gilles86/exp_tools). This little package makes it easy to leverage [pygaze](www.pygaze.org) and [psychopy](http://www.psychopy.org) with as little code as possible, while making sure that our eye tracking data remains simple and easily analyzable.  In a brief course like this, we don't want to get bogged down in menial things like fixing how we read in data.

## What does an experiment look like?
An experiment consists of a `Session` class, and a(t least one) `Trial` class. The `Session` class, for example named `SPSession`, for *smooth pursuit session*, inherits eye tracking and display capabilities from the `EyelinkSession` defined in our `exp_tools`. Similarly, our `SPTrial` class inherits from the `exp_tools` `Trial` class. This way, our experimental implementation is minimal, but broad functionality is ensured and shared between experiments. 


# List of Experiments
- [Smooth Pursuit Experiment](smooth_pursuit)
- [Saccade Trajectory Experiment](saccade_trajectory)
- [Saccade Adaptation Experiment](saccade_adaptation)
- [Pupil Response Experiment](pupil_response)
- [Gaze Density Experiment](gaze_density)