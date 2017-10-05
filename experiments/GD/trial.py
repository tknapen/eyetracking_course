from exptools.core.trial import Trial
from stim import BinocularDotStimulus
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class BinocularDotsTrial(Trial):

    def __init__(self, trial_idx, config, color='r', *args, **kwargs):

        self.ID = trial_idx
        self.color = color

        print "YOOOO %s" % color

        phase_durations = [config['fixation_time'], config['stimulus_time']]

        super(
            BinocularDotsTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

        self.dot_stimulus = BinocularDotStimulus(screen=self.screen,
                                                 trial=self,
                                                 config=config,
                                                 color=self.color,
                                                 session=self.session)

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
            self.dot_stimulus.draw()
            self.fixation.draw()

        super(BinocularDotsTrial, self).draw()

    def run(self):
        super(BinocularDotsTrial, self).run()

        while not self.stopped:

            if self.phase == 0:
                if self.session.clock.getTime() - \
                        self.start_time > self.phase_times[0]:
                    self.phase_forward()

            if self.phase == 1:
                if self.session.clock.getTime() - \
                        self.start_time > self.phase_times[1]:
                    self.phase_forward()

            if self.phase == 2:
                self.stopped = True

            # events and draw
            self.event()
            self.draw()

        self.stop()

    def stop(self):
        super(BinocularDotsTrial, self).stop()

        if self.color == 'r':
            self.session.binocular_config['red_intensity'] = self.dot_stimulus.element_master.color[0]
        elif self.color == 'b':
            self.session.binocular_config['blue_intensity'] = self.dot_stimulus.element_master.color[2]

        print self.color, self.session.binocular_config

    def event(self):

        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.events.append(
                        [-99, self.session.clock.getTime() - self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                if ev in ['a', 's']:

                    if self.color == 'r':
                        delta = np.array([0.025, 0, 0])
                    elif self.color == 'b':
                        delta = np.array([0, 0, 0.025])

                    if ev == 'a':
                        self.dot_stimulus.element_master.color += delta
                    else:
                        self.dot_stimulus.element_master.color -= delta

            super(BinocularDotsTrial, self).key_event(ev)
