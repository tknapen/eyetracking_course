from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class LR_IMTrial(Trial):

    def __init__(self, ti, config, parameters, *args, **kwargs):

        self.ID = ti
        # self.parameters = parameters

        phase_durations = [parameters['fixation_duration'], 
                           parameters['stimulus_duration'],
                           parameters['iti']]
                           
        super(
            LR_IMTrial,
            self).__init__(
            phase_durations=phase_durations,
            parameters = parameters,
            *args,
            **kwargs)



    def draw(self, *args, **kwargs):

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.session.instruction.draw()

        elif self.phase == 1:
            self.session.shape_stims[self.parameters['shape']].draw()

        self.session.fixation.draw()

        super(LR_IMTrial, self).draw()

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.events.append(
                        [-99, self.session.clock.getTime() - self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'

                elif ev in ('b','r','t'):
                    if (self.phase == 0) * (self.ID == 0):
                        self.phase_forward()                    
                    elif self.phase == 2 and ev in ('b','r'):
                        self.parameters['answer'] = ['b','r'].index(ev)

            super(LR_IMTrial, self).key_event(ev)

