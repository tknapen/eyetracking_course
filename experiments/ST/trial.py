from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class STTrial(Trial):

    def __init__(self, ti, config, stimulus=None, parameters=None, *args, **kwargs):

        self.ID = ti

        phase_durations = [parameters['fixation_time'], parameters['target_time'], parameters['target_distractor_time'], parameters['target_post_time']]

        super(
            STTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

        self.parameters = parameters

    def draw(self, *args, **kwargs):

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.session.instruction.draw()
        if self.phase == 0:
            self.session.fixation.draw()
        elif self.phase == 1:
            # update fixation position
            self.session.fixation.setPos((self.parameters['fix_x'], self.parameters['fix_y']))
            self.session.fixation.draw()
        elif self.phase == 2:
           # update distractor position
            self.session.distractor.setPos((self.parameters['distractor_x'], self.parameters['distractor_y']))
            self.session.distractor.draw()
            self.session.fixation.draw()
        elif self.phase == 3:
            self.session.fixation.draw()

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
                    elif self.phase == 3:
                        self.stopped = True

            super(STTrial, self).key_event(ev)
