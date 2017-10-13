from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np


class SPTrial(Trial):

    def __init__(self, ti, config, stimulus=None, *args, **kwargs):

        self.ID = ti

        shell()

        super(
            SPTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)

    def update_fix_pos(self,time):

        amplitude = self.parameters['sp_path_amplitude']*self.session.pixels_per_degree/2
        f = self.parameters['sp_path_temporal_frequency']/self.parameters['TR']
        x_pos = amplitude * np.sin(2*np.pi*f*time) 
        y_pos = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        self.session.fixation.setPos([x_pos,y_pos])

    def draw(self):

        """docstring for draw"""
        # the position of the dot is determined based
        # on the session time
        if (self.phase == 0) * (self.ID == 0):
            draw_time = 0         
        else:
            draw_time = self.session.clock.getTime() - self.session.start_time

        self.update_fix_pos(draw_time)

        self.session.fixation.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.instruction.draw()
        # phase 2 starts with the presentation of the first stimulus
        elif self.phase == 2:
            if self.stim1_drawn == False:
                self.session.test_stim_1.draw()
                self.stim1_drawn = True
        # phase 3 starts with the presentation of the second stimulus
        elif self.phase == 3:
            if self.stim2_drawn == False:
                self.session.test_stim_2.draw()
                self.stim2_drawn = True    

        super(SPTrial, self).draw() # flip

    def event(self):

        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.events.append(
                        [-99, self.session.clock.getTime() - self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                if ev in ['space', ' ','t']:
                    if self.phase == 0:
                        self.phase_forward()
                    elif self.phase == 1:
                        self.stopped = True

            super(SPTrial, self).key_event(ev)

    def run(self, ID = 0):
        self.ID = ID
        super(SPTrial, self).run()

        fp_y = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        target_y_offset = self.parameters['y_order']*self.parameters['test_stim_y_offset']*self.session.pixels_per_degree
      
        x_pos_1 = self.parameters['x_pos_1']*self.session.pixels_per_degree
        y_pos_1 = fp_y + target_y_offset
        self.session.test_stim_1.setPos([x_pos_1,y_pos_1 ])

        x_pos_2 = self.parameters['x_pos_2']*self.session.pixels_per_degree
        y_pos_2 = fp_y - target_y_offset
        self.session.test_stim_2.setPos([x_pos_2,y_pos_2 ])

        if self.ID != 0:
            self.trial_onset_time = self.session.cumulative_phase_durations[self.ID,0] + self.session.start_time

        while not self.stopped:
            # Only in trial 1, phase 0 represents the instruction period.
            # After the first trial, this phase is skipped immediately
            if (self.phase == 0) * (self.ID != 0):
                self.phase_forward()
            # determine run_time 
            # phase 1 is the smooth pursuit 'rest period'
            if self.phase == 1:
                self.phase_1_time = self.session.clock.getTime()
                if ( self.phase_1_time  - self.trial_onset_time ) > self.phase_durations[1]:
                    self.phase_forward()
            # phase 2 starts with the presentation of the first stimulus
            if self.phase == 2:
                self.phase_2_time = self.session.clock.getTime()
                if ( self.phase_2_time  - self.phase_1_time ) > self.phase_durations[2]:
                    self.phase_forward()
            # phase 3 starts with the presentation of the second stimulus
            if self.phase == 3:
                self.phase_3_time = self.session.clock.getTime()
                if ( self.phase_3_time  - self.phase_2_time ) > self.phase_durations[3]:
                    self.stopped = True

            # events and draw
            self.event()
            self.draw()
    
        self.stop()
