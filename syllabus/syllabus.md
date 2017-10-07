# Syllabus

**The eye is the window to the brain: as researchers, we can tell a lot from where, and how, people look around. Recently, there has been an uptick in interest in what the pupil's fluctuations can tell us about the state of people's brains. But how can you make sure that you're doing the right experiment to answer your research question?**

In this two-day course we will teach you the ins and outs of eye tracking. At the end of the course, you will be able to devise and perform a 'valid' eyetracking experiment, and perform basic analyses on the resulting data. That is, we will teach you about all the things you can do with eye tracking and how to do them, with a focus on saccadic eye movements and pupil responses. 

The course is short, so our goal is to give you an idea of the possibilities and pitfalls, in order to give you a solid foundation for further learning. In the course, we'll be using an SR Research EyeLink system, but the skills learned in this course will translate easily to other eye tracking systems. Furthermore, we will use only open-source tools that are available in online repositories, supporting your future experiments. We expect students to have affinity, if limited, with programming. Python is an easy language to learn, so it doesn't matter much what language you have experience in. 

### Where?
Practicals will be at the VU, rooms to be disclosed. [Lab website](tknapen.github.io)

### A Broad Timeline for the Course
|              |            **Day 1**                                         |
| ------------ | :-----------------------------------------------------------------|
|      *When?*      |      *What?*                        |
| **Morning** |  **Lectures:** |
|                   | Eye movements: Types of eye movements, brain areas involved in eye movements, clinical uses of eye movements. |
|  | Fixation, Saccades, MicroSaccades, Opto-Kinetic Nystagmus and Smooth Pursuit. |
|  | The visuomotor hierarchy: from brain stem, through Superior Colliculus and Thalamus, to Frontal Cortex. |
|  | What does an eye movement look like? Kinematics of Eye Movements. |
|  | How to record eye movements: Eye Tracking. |
|  **Afternoon** |      **Recording Practical:**                       |
|  | Perform your choice of a set of simple eye movement experiments in the lab |
|  | How to work the machine: EyeLink Calibration and Operation |
|  **Afternoon** |      **Analysis Practical:**                       |
|  | First look at the data from our own experiment: analysis environment. |
|  | How to detect different types of eye movements in our data. |
|  | Different types of data analysis on eye tracking data: Gaze position heat maps, saccade velocity traces, saccade curvature, etc. |


|              |            **Day 2**                                         |
| ------------ | :-----------------------------------------------------------------|
|      *When?*      |      *What?*                        |
| **Morning** |  **Lectures:** |
|                   | Eye tracking: Pupil Size Measurements |
|  | What can the pupil tell us about brain state? |
|  | How to record pupil size, and how not: How to tailor your experiment to get sensible pupil size recordings. |
|  **Afternoon** |      **Recording Practical:**                      |
|  | Perform second experiment focused on your choice of eye movements and/or pupil responses. |
|  **Afternoon** |      **Analysis Practical:**                       |
|  | Preprocessing of eye tracking data, with a focus on pupil size signals. |
|  | How to analyze pupil size fluctuations |
|  | Continue from Day 1, Eye Movements. |

### The tools that you will learn to use
In our lab, we use Python for all our own data analysis. During this course, we will use Python to perform experiments, and to analyze our data. This means that the practicals are implemented in [iPython Notebooks](https://nbviewer.jupyter.org/github/ipython/ipython/blob/4.0.x/examples/IPython%20Kernel/Plotting%20in%20the%20Notebook.ipynb), a convenient way of performing data analysis / programming in a browser window. You will learn to leverage several state-of-the-art Python packages for data analysis. We will post all the materials used in the course in the course's own [GitHub repository](https://github.com/tknapen/eyetracking_course), also for future reference.

Our first tutorial will rehash those parts of Python/Numpy that we'll really need to use a lot for our data analysis. It makes sense to dive into this a bit in order to prepare for the course. To do this, consult these tutorials:

- [Basic Python Tutorial](https://github.com/jrjohansson/scientific-python-lectures/blob/master/Lecture-1-Introduction-to-Python-Programming.ipynb), part of a set of scientific python lectures.
- [Numpy Introduction](https://github.com/jrjohansson/scientific-python-lectures/blob/master/Lecture-2-Numpy.ipynb)

![Python makes you fly](https://imgs.xkcd.com/comics/python.png "Python makes you fly") 



## Detailed list of topics

- The eye: anatomy of eye muscles and degrees of freedom of eye movements
- Geometry of eye movements: Listing's law
- Motor control of the eye: Different types of eye movements:
    + Optokinetic Nystagmus
    + Vestibulo-Ocular Reflex
    + Saccades, MicroSaccades and the Main Sequence
    + Smooth Pursuit
    + Vergence
- From the ocular muscles up into the brain:
    + Brainstem structures involved in oculomotor control
        * Motor commands that the brian stem sends to the ocular muscles
        * Translation of Space into Time
    + Superior Colliculus:
        * Retinotopic Map of the Colliculus, Laminar Structure
    + Thalamus, Basal Ganglia & Substantia Nigra
    + Cerebellum
    + Cortical control of Eye Movements:
        * V1 in vergence
        * MT/MST in smooth pursuit
        * Parietal Cortex
        * Frontal Eye Fields
            - Movement Neurons
            - Visual Neurons
- Corrollary Discharge - the Efference Copy
    + Visual Stability, or the interaction between Sensation and Action
    + Effects of Eye Movements on Vision
- The Guidance of Eye Movements: Salience and Target Selection
- Eye Tracking
    + Different Apparatuses for Eye Tracking
    + Video-based eye trackers
    + Eyelink Explanation:
        * Software, how to operate
            - Different Settings
        * Calibration, Validation

- the Pupil
    + Innervation, Dilation (Myosis) and Constriction (Mydriasis)
    + Luminance Responses
    + Neurotransmitters: Central Influences on Pupil Size
    


