from exptools.core.session import EyelinkSession
from trial import GDTrial
from psychopy import clock
from psychopy.visual import ImageStim
import numpy as np
import os
import exptools
import json
import glob


class GDSession(EyelinkSession):

    def __init__(self, *args, **kwargs):

        super(GDSession, self).__init__(*args, **kwargs)

        # self.create_screen(full_screen=True, engine='pygaze')

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.config = config
        self.create_trials()

        self.stopped = False

    def create_trials(self):
        """creates trials by loading a list of jpg files from the img/ folder"""

        image_files = sorted(glob.glob(os.path.join(os.path.abspath(os.getcwd()), 'imgs', '*.jpg')))

        self.image_stims = [ImageStim(self.screen, image=imf) for imf in image_files]
        self.trial_order = np.random.permutation(len(self.image_stims))


    def run(self):
        """docstring for fname"""
        # cycle through trials

        for ti in np.arange(len(self.image_stims)):

            parameters = {'stimulus': self.trial_order[ti]}

            trial = GDTrial(ti=ti,
                           config=self.config,
                           screen=self.screen,
                           session=self,
                           parameters=parameters,
                           tracker=self.tracker)
            trial.run()

            if self.stopped == True:
                break

        self.close()
