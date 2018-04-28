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

        phase_durations = [parameters['wait_duration'],
                        parameters['fixation_duration'], 
                        parameters['stimulus_duration'],
                        parameters['iti']]
                           
        super(
            LR_IMTrial,
            self).__init__(
            phase_durations=phase_durations,
            parameters = parameters,
            *args,
            **kwargs)

        self.parameters['answer'] = -1
        self.parameters['rt'] = -1

    def draw(self, *args, **kwargs):
        if (self.phase == 0 ) and (self.ID == 0):
            self.session.instruction.draw()

        elif self.phase == 2:
            x_position = self.parameters['side'] * self.session.deg2pix(self.parameters['shape_ecc'])
            self.session.shape_stims[self.parameters['shape']].setPos((x_position,0))
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
                    if (self.phase == 0) and (self.ID == 0):
                        self.phase_forward()                    
                    elif self.phase == 3 and ev in ('b','r'):
                        self.parameters['answer'] = ['b','r'].index(ev)
                        self.parameters['rt'] = self.session.clock.getTime() - self.phase_times[self.phase-1]

            super(LR_IMTrial, self).key_event(ev)

