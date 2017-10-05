from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class GDTrial(Trial):

    def __init__(self, ti, config, stimulus=None, *args, **kwargs):

        self.ID = ti

        phase_durations = [config['fixation_time'], config['stimulus_time']]

        super(
            GDTrial,
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

        super(GDTrial, self).draw()

    def run(self):
        super(GDTrial, self).run()

        while not self.stopped:

            self.check_phase_time()
            # if self.phase == 0:
            #     self.phase_times[self.phase] = self.session.clock.getTime()
            #     if self.phase_times[self.phase] - \
            #             self.start_time > self.phase_durations[self.phase]:
            #         self.phase_forward()

            # if self.phase == 1:
            #     self.phase_times[self.phase] = self.session.clock.getTime()
            #     if self.phase_times[self.phase] - \
            #             self.phase_times[self.phase - 1] > self.phase_durations[self.phase]:
            #         self.stopped = True

            # events and draw
            self.event()
            self.draw()

        super(GDTrial, self).stop()

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
                        print 'phase 0 skipped'
                        self.phase_forward()
                    elif self.phase == 1:
                        print 'phase 1 skipped'
                        self.stopped = True

            super(GDTrial, self).key_event(ev)
