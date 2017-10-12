from exptools.core.session import EyelinkSession
from trial import PRTrial
from psychopy import visual, clock
import numpy as np
import os
import exptools
import json
import glob


class PRSession(EyelinkSession):

    def __init__(self, *args, **kwargs):

        super(PRSession, self).__init__(*args, **kwargs)

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.config = config
        self.create_trials()
        self.setup_stimuli()

        self.stopped = False


    def create_trials(self):
        """creates trials by creating a restricted random walk through the display from trial to trial"""

        self.trial_parameters = [{'fixation_duration': 1.0,
                                  'random_dots1_duration' : 2.0,
                                  'coherent_dots_duration': 2.0,
                                  'random_dots2_duration': 2.0,
                                  }]

    def setup_stimuli(self):
        size_fixation_pix = self.deg2pix(self.config['size_fixation_deg'])
        size_dotfield_pix = self.deg2pix(self.config['diameter_dotcloud_deg'])
        size_dot_pix = self.deg2pix(self.config['size_dot_deg'])
        speed_dot_pix = self.deg2pix(self.config['speed_dot_deg'])

        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='red',
                                           sf=0)

        self.dots = visual.DotStim(self.screen, 
                                   fieldSize=size_dotfield_pix,
                                   fieldShape='circle',
                                   speed=speed_dot_pix,
                                   dotSize=size_dot_pix,
                                   nDots=self.config['nDots'], 
                                   noiseDots=self.config['noiseDots'],
                                   coherence=0.0)

        print self.config

    def run(self):
        """run the session"""
        # cycle through trials

        print self.trial_parameters

        for trial_id, parameters in enumerate(self.trial_parameters):
            trial = PRTrial(ti=trial_id,
                           config=self.config,
                           screen=self.screen,
                           session=self,
                           parameters=parameters,
                           tracker=self.tracker)
            trial.run()

            if self.stopped == True:
                break

        self.close()
