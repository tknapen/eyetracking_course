from exptools.core.trial import Trial
import os
import exptools
import json
from psychopy import logging, visual, event
import numpy as np

from IPython import embed as shell


class SPTrial(Trial):

    def __init__(self,i, parameters,phase_durations, stimulus=None, *args, **kwargs):


        super(
            SPTrial,
            self).__init__(
            phase_durations=phase_durations,
            *args,
            **kwargs)
        self.ID = i
        self.parameters = parameters

        self.stim1_drawn = False
        self.stim2_drawn = False


    def update_fix_pos(self,time):

        amplitude = self.parameters['sp_path_amplitude']*self.session.pixels_per_degree/2
        f = self.parameters['sp_path_temporal_frequency']/self.parameters['TR']
        x_pos = amplitude * np.sin(2*np.pi*f*time) 
        y_pos = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        self.session.fixation.setPos([x_pos,y_pos])

    def create_stimuli(self):
        """create_stimuli updates positions of tests"""
        # determine location of flash stimuli
        fp_y = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        target_y_offset = self.parameters['y_order']*self.parameters['test_stim_y_offset']*self.session.pixels_per_degree
      
        x_pos_1 = self.parameters['x_pos_1']*self.session.pixels_per_degree
        y_pos_1 = fp_y + target_y_offset
        self.session.test_stim_1.setPos([x_pos_1,y_pos_1 ])

        x_pos_2 = self.parameters['x_pos_2']*self.session.pixels_per_degree
        y_pos_2 = fp_y - target_y_offset
        self.session.test_stim_2.setPos([x_pos_2,y_pos_2 ])

    def draw(self):
        """docstring for draw"""

        # the position of the dot is determined based
        # on the session time
        if (self.phase == 0) * (self.ID == 0):
            draw_time = 0         
        else:
            draw_time = self.session.clock.getTime() - self.session.start_time

        self.update_fix_pos(draw_time)
        # self.session.fixation_outer_rim.draw()
        # self.session.fixation_rim.draw()
        self.session.fixation.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.session.instruction.draw()
        # phase 2 starts with the presentation of the first stimulus
        elif self.phase == 2:
            if self.stim1_drawn == False:
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.session.test_stim_1.draw()
                self.stim1_drawn = True
        # phase 3 starts with the presentation of the second stimulus
        elif self.phase == 3:
            if self.stim2_drawn == False:
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.session.test_stim_2.draw()
                self.stim2_drawn = True    

        super(SPTrial, self).draw() # flip

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                # it handles both numeric and lettering modes 
                # elif ev == ' ': # TR pulse
                #     print('space bar presssed')

                elif ev in ('f','j'):
                    if (self.phase == 0) * (self.ID == 0):
                        print('fj presssed in ID and phase 00')
                        self.session.start_time = self.session.clock.getTime()
                        self.start_time = self.session.clock.getTime()
                        self.trial_onset_time = self.session.cumulative_phase_durations[self.ID,0] + self.session.start_time
                        self.phase_forward()                    
                    else:
                        self.parameters['answer'] = ['f','j'].index(ev)
        
            super(SPTrial, self).key_event(ev)

        