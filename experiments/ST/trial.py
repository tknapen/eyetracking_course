from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class STTrial(Trial):

    def __init__(self, ti, config, stimulus=None, *args, **kwargs):

        self.ID = ti

        phase_durations = [config['fixation_time'], config['target_time'], config['target_distractor_time'], config['target_post_time']]

        super(
            STTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

        size_fixation_pix = self.session.deg2pix(config['size_fixation_deg'])

        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0)

        self.distractor = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0)

    def draw(self, *args, **kwargs):

        if self.phase == 0:
            self.session.fixation.draw()
        elif self.phase == 1:
            # update fixation position
            self.session.fixation.setPos((self.parameters['fix_x'], self.parameters['fix_x']))
            self.session.fixation.draw()
        elif self.phase == 2:
           # update distractor position
            self.session.fixation.setPos((self.parameters['distractor_x'], self.parameters['distractor_x']))
            self.session.fixation.draw()
            self.session.distractor.draw()
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
                    elif self.phase == 1:
                        self.stopped = True

            super(STTrial, self).key_event(ev)
