from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class PRTrial(Trial):

    def __init__(self, ti, config, parameters, *args, **kwargs):

        self.ID = ti

        phase_durations = [parameters['fixation_duration'], 
                           parameters['random_dots1_duration'],
                           parameters['coherent_dots_duration'],
                           parameters['random_dots2_duration']]

        super(
            PRTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

    def draw(self, *args, **kwargs):

        if self.phase == 0:
            self.session.fixation.draw()

        elif self.phase == 1:
            self.session.dots.coherence = 0.0
            self.session.fixation.draw()
            self.session.dots.draw()

        elif self.phase == 2:
            self.session.dots.coherence = 1.0
            self.session.fixation.draw()
            self.session.dots.draw()

        elif self.phase == 3:
            self.session.dots.coherence = 0.0
            self.session.fixation.draw()
            self.session.dots.draw()

        super(PRTrial, self).draw()

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.events.append(
                        [-99, self.session.clock.getTime() - self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'

            super(PRTrial, self).key_event(ev)
