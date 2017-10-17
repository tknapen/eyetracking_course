from exptools.core.session import EyelinkSession
from trial import SPTrial
from psychopy import clock
from psychopy.visual import ImageStim, PatchStim, Rect, TextStim
import numpy as np
import os
import exptools
import json
import glob

from IPython import embed as shell

class SPSession(EyelinkSession):

    def __init__(self, *args, **kwargs):

        super(SPSession, self).__init__(*args, **kwargs)

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.config = config
        self.create_trials()

        # define the effective screen dimensions for stimulus presentation
        self.ywidth = (1-config['sp_path_elevation'])*self.screen.size[1]*2


        self.stopped = False

    def create_trials(self):
        """creates trials"""

        this_instruction_string = """Determine whether the second flash is more left or right of the first.\nPress 'f' for left and 'j' for right. \nPress either key to start."""
        self.instruction = TextStim(self.screen, 
            text = this_instruction_string, 
            font = 'Helvetica Neue',
            pos = (0, 0),
            italic = True, 
            height = 20, 
            alignHoriz = 'center',
            color=self.config['stim_color'])
        self.instruction.setSize((1200,50))

        # combining all 5 positions gives 5x5=25 possible location combinations
        x_test_positions = np.array(np.meshgrid(self.config['test_stim_positions'], self.config['test_stim_positions'])).T.reshape((-1,2))
        # x1, x2 = x_test_positions[:,0], x_test_positions[:,1]
        x1, x2 = np.zeros_like(x_test_positions[:,0]), x_test_positions[:,1]

        # y position is above or below fp
        # y_test_positions = np.concatenate((-1 * np.ones(x_test_positions.shape[0]), np.ones(x_test_positions.shape[0])))
        y_test_positions = np.concatenate((-1*np.ones(x_test_positions.shape[0]), -1*np.ones(x_test_positions.shape[0])))

        # tile them 4 times, so that we have 25*4=100 trials
        x_test_positions_tiled = np.array([np.tile(x1, 4), np.tile(x2, 4)]).T
        y_test_positions_tiled = np.tile(y_test_positions, 2)

        # all combinations of parameters are now repeated twice, so we add the eye dir to first 50 and last 50
        eye_dir = np.concatenate([np.ones(x_test_positions_tiled.shape[0]/2),np.zeros(x_test_positions_tiled.shape[0]/2)])

        # now let's create a random trial order 
        self.trial_order = np.arange(eye_dir.shape[0])
        np.random.shuffle(self.trial_order)

        # and apply
        x_test_positions_tiled_shuffled = x_test_positions_tiled[self.trial_order]
        y_test_positions_tiled_shuffled = y_test_positions_tiled[self.trial_order]
        eye_dir_shuffled = eye_dir[self.trial_order]

        ITIs = np.zeros(len(self.trial_order))
        # and here's the distribution of ITIs:
        # unique_ITIs = {
        # 1: 37,
        # 2: 22,
        # 3: 15,
        # 4: 10,
        # 5: 7,
        # 6: 4,
        # 7: 3,
        # 8: 2
        # }

        unique_ITIs = {
        1: 50,
        2: 50
        }

        # randomly distribute ITI's over the trial combinations:
        ITI_order = np.arange(len(ITIs))
        np.random.shuffle(ITI_order)        
        k = 0
        for this_ITI in unique_ITIs.keys():
            ITIs[ITI_order[k:k+unique_ITIs[this_ITI]]] = this_ITI
            k += unique_ITIs[this_ITI]

        # and add or subtract 1 when a switch in eye dir is required:
        n_switches = 0
        for ti, this_eye_dir in enumerate(eye_dir_shuffled):
            ITI_cumsum = np.cumsum(ITIs)[ti]
            current_direction = ITI_cumsum%2
            if current_direction != this_eye_dir:
                ITIs[ti] += [-1,1][n_switches%2]
                n_switches += 1

        ITIs += self.config['minimal_iti']
       
        # the total number of TRs can now be either 661 or 662, depending on whether there even or even n_switches
        # thus add 1 TR when n_switches are uneven:
        padd_TR = n_switches%2

        # now add the first and last empty trials:
        x_test_positions_tiled_shuffled = np.vstack([[-1e3,-1e3],x_test_positions_tiled_shuffled,[-1e3,-1e3]]) #-1e3 means off the screen)
        y_test_positions_tiled_shuffled = np.hstack([-1e3,y_test_positions_tiled_shuffled,-1e3]) #-1e3 means off the screen)
        ITIs = np.hstack([self.config['warming_up_n_TRs'],ITIs,self.config['warming_up_n_TRs']+padd_TR])
        eye_dir_shuffled = np.hstack([0,eye_dir_shuffled,0])

        # define all durations per trial
        self.phase_durations = np.array([[
            10, # instruct time, skipped in all trials but the first (wait for t)
            ITI * self.config['TR'], # smooth pursuit before stim
            self.config['TR'], # smooth pursuit after stim 1
            self.config['TR'] # smooth pursuit after stim 2
            ] for ITI in ITIs] )    
        
        self.fixation = PatchStim(self.screen,
            mask='raisedCos',
            tex=None, 
            size=self.config['sp_target_size']*self.pixels_per_degree, 
            pos = np.array((0.0,self.config['sp_target_size']*self.pixels_per_degree)), 
            color = self.config['stim_color'], 
            opacity = 1.0, 
            maskParams = {'fringeWidth':0.4})

        # now define the test stim sizes dependent on screen size available:
        if self.config['test_stim_height'] == 0:
            self.config['test_stim_height'] = self.ywidth/4/self.pixels_per_degree
        if self.config['test_stim_y_offset'] == 0:
            self.config['test_stim_y_offset'] = self.ywidth/4/self.pixels_per_degree
        self.test_stim_1 = Rect(self.screen, 
                            width = self.config['test_stim_width']*self.pixels_per_degree,  
                            height = self.config['test_stim_height']*self.pixels_per_degree, 
                            lineColor = self.config['stim_color'],
                            fillColor = self.config['stim_color'])

        self.test_stim_2 = Rect(self.screen, 
                            width = self.config['test_stim_width']*self.pixels_per_degree, 
                            height = self.config['test_stim_height']*self.pixels_per_degree, 
                            lineColor = self.config['stim_color'],
                            fillColor = self.config['stim_color'])

        self.start_time = 0.0
        self.cumulative_phase_durations = np.cumsum(np.r_[0,self.phase_durations[:,1:].ravel()][:-1]).reshape((self.phase_durations.shape[0], -1))

        self.all_trials = []
        for i in range(len(eye_dir_shuffled)):#self.trial_order:

            this_trial_parameters={
                                    # trial varying params:
                                    'x_pos_1': x_test_positions_tiled_shuffled[i,0],
                                    'x_pos_2': x_test_positions_tiled_shuffled[i,1], 
                                    'y_order': y_test_positions_tiled_shuffled[i],
                                    'eye_dir': eye_dir_shuffled[i],
                                    'ITI': ITIs[i], # this should not be _shuffled

                                    # these params don't vary over trials:
                                    'TR': self.config['TR'],
                                    'sp_path_amplitude':self.config['sp_path_amplitude'],
                                    'test_stim_y_offset':self.config['test_stim_y_offset'],
                                    'sp_path_elevation':self.config['sp_path_elevation'],
                                    'sp_path_temporal_frequency':self.config['sp_path_temporal_frequency'],
                                    'warming_up_n_TRs':self.config['warming_up_n_TRs']
                                    }

            self.all_trials.append(SPTrial(i,this_trial_parameters, self.phase_durations[i], session = self, screen = self.screen, tracker = self.tracker))

    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i, trial in enumerate(self.all_trials):
            # run the prepared trial
            trial.run()
            if self.stopped == True:
                break
        self.close()
    
