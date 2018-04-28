from exptools.core.session import EyelinkSession
from trial import MSTrial
from psychopy import clock
from psychopy.visual import ImageStim, MovieStim
import numpy as np
import os
import exptools
import json
import glob


class MSSession(EyelinkSession):

    def __init__(self, *args, **kwargs):

        super(MSSession, self).__init__(*args, **kwargs)

        # self.create_screen(full_screen=True, engine='pygaze')

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.config = config
        self.create_trials()

        self.stopped = False

    def create_trials(self):
        """creates trials by loading a list of jpg files from the img/ folder"""

        if self.index_number == 1:
            self.movies = [0,1]
        elif self.index_number == 2:
            self.movies = [2,3]
        elif self.index_number == 3:
            self.movies = [4,5]        
        elif self.index_number == 4:
            self.movies = [6,7]        
        elif self.index_number == 5:
            self.movies = [8,9]

        movie_files = [os.path.join(os.path.abspath(os.getcwd()), 'imgs', 'fn_output_%s_%i_ss_pcm.avi'%(self.config['language'], m)) for m in self.movies]

        self.movie_stims = [MovieStim(self.screen, filename=imf, size=self.screen.size) for imf in movie_files]
        self.trial_order = np.arange(len(self.movie_stims))


    def run(self):
        """docstring for fname"""
        # cycle through trials

        for ti in np.arange(len(self.movie_stims)):

            parameters = {'stimulus': self.trial_order[ti], 'movie':self.movies[self.trial_order[ti]]}

            parameters.update(self.config)
            
            trial = MSTrial(ti=ti,
                           config=self.config,
                           screen=self.screen,
                           session=self,
                           parameters=parameters,
                           tracker=self.tracker)
            trial.run()

            if self.stopped == True:
                break

        self.close()
