from exptools.core import Session
from trial import BinocularDotsTrial
from psychopy import clock
import os
import exptools
import json


class BinocularSession(Session):

    def __init__(self, *args, **kwargs):

        super(BinocularSession, self).__init__(*args, **kwargs)

        self.create_screen(full_screen=False, engine='psychopy')

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.binocular_config = config

        self.stopped = False

    def run(self):
        """docstring for fname"""
        # cycle through trials

        trial_idx = 0

        while not self.stopped:

            color = ['r', 'b'][trial_idx % 2]
            trial = BinocularDotsTrial(trial_idx,
                                       config=self.binocular_config,
                                       screen=self.screen,
                                       session=self,
                                       color=color)
            print "running %s" % trial_idx
            trial.run()
            trial_idx += 1

        self.close()
