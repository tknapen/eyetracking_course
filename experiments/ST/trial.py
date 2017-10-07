from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class STTrial(Trial):

    def __init__(self, ti, config, stimulus=None, *args, **kwargs):

        self.ID = ti

        phase_durations = [config['fixation_time'], config['stimulus_time']]

        super(
            STTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

        self.image_stim = self.session.image_stims[self.parameters['stimulus']]
        size_fixation_pix = self.session.deg2pix(config['size_fixation_deg'])

        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0)

    def draw(self, *args, **kwargs):

        if self.phase == 0:
            self.fixation.draw()
        elif self.phase == 1:
            self.image_stim.draw()
            # self.fixation.draw()

        super(STTrial, self).draw()

    def event(self):

        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.events.append(
                        [-99, self.session.clock.getTime() - self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                if ev in ['space', ' ']:
                    if self.phase == 0:
                        self.phase_forward()
                    elif self.phase == 1:
                        self.stopped = True

            super(STTrial, self).key_event(ev)
