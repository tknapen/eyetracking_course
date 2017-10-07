from exptools.core.session import EyelinkSession
from trial import STTrial
from psychopy import clock
from psychopy.visual import ImageStim
import numpy as np
import os
import exptools
import json
import glob


class STSession(EyelinkSession):

    def __init__(self, *args, **kwargs):

        super(STSession, self).__init__(*args, **kwargs)

        # self.create_screen(full_screen=True, engine='pygaze')

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.config = config
        self.create_trials()

        self.stopped = False

    def create_trials(self):
        """creates trials by loading a list of jpg files from the img/ folder"""

        self.saccade_directions = np.random.rand(config['n_trials']) * 2.0 * np.pi
        saccade_amplitude_pix = self.deg2pix(config['saccade_amplitude'])

        saccade_path_d = np.array([np.sin(self.saccade_directions)*saccade_amplitude_pix, np.cos(self.saccade_directions)*saccade_amplitude_pix])
        np.cumsum(saccade_path_d, axis=1)
        

        size_fixation_pix = self.deg2pix(config['size_fixation_deg'])
        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0)

    def run(self):
        """docstring for fname"""
        # cycle through trials

        for ti in np.arange(len(self.image_stims)):

            parameters = {'stimulus': self.trial_order[ti]}

            trial = STTrial(ti=ti,
                           config=self.config,
                           screen=self.screen,
                           session=self,
                           parameters=parameters,
                           tracker=self.tracker)
            trial.run()

            if self.stopped == True:
                break

        self.close()
