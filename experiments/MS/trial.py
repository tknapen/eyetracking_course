from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class MSTrial(Trial):

    def __init__(self, ti, config, stimulus=None, *args, **kwargs):

        self.ID = ti
        if self.ID == 0:
            phase_durations = [1800, config['fixation_time'], config['stimulus_time'], config['fixation_time']]
        else:
            phase_durations = [-0.001, config['fixation_time'], config['stimulus_time'], config['fixation_time']]

        super(
            MSTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

        self.movie_stim = self.session.movie_stims[self.parameters['stimulus']]
        size_fixation_pix = self.session.deg2pix(config['size_fixation_deg'])

        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0)

    def draw(self, *args, **kwargs):

        if self.phase in  (0,1,3):
            self.fixation.draw()
        elif self.phase == 2:
            self.movie_stim.draw()


        super(MSTrial, self).draw()

    def event(self):

        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.events.append(
                        [-99, self.session.clock.getTime() - self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                if ev in ['space', ' ', 't']:
                    if (self.phase == 0) and (self.ID == 0):
                        self.phase_forward()

            super(MSTrial, self).key_event(ev)
