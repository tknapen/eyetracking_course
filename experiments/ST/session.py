from exptools.core.session import EyelinkSession
from trial import STTrial
from psychopy import visual, clock
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
        """creates trials by creating a restricted random walk through the display from trial to trial"""


        ##################################################################################
        ##
        ##  Calculate saccade path for all trials
        ##
        ##################################################################################

        saccade_amplitude_pix = self.deg2pix(self.config['saccade_amplitude'])
        max_eccentricity_pix = self.deg2pix(self.config['max_eccentricity'])
        
        # fixation positions
        present_pos = np.array([0, 0]) # center of screen?        
        trial_saccade_target_positions = [present_pos]

        trial_distractor_positions = [np.array([0, 0])]
        saccade_distractor_directions = [[0,0]]

        for t in range(self.config['n_trials']):
            saccade_direction = np.random.rand() * 2.0 * np.pi
            saccade_vector = np.array([np.sin(saccade_direction)*saccade_amplitude_pix, 
                                        np.cos(saccade_direction)*saccade_amplitude_pix])
            while np.linalg.norm(present_pos + saccade_vector) > max_eccentricity_pix:
                saccade_direction = np.random.rand() * 2.0 * np.pi
                saccade_vector = np.array([np.sin(saccade_direction)*saccade_amplitude_pix, 
                                            np.cos(saccade_direction)*saccade_amplitude_pix])

            which_distractor_direction = np.radians(np.random.choice([-self.config['distractor_deviation_angle'],0,self.config['distractor_deviation_angle']]))
            distractor_vector = np.array([np.sin(saccade_direction + which_distractor_direction)*saccade_amplitude_pix, 
                                            np.cos(saccade_direction + which_distractor_direction)*saccade_amplitude_pix])

            # store this information in list for later use
            trial_saccade_target_positions.append(present_pos + saccade_vector)
            trial_distractor_positions.append(present_pos + distractor_vector)
            saccade_distractor_directions.append([saccade_direction, which_distractor_direction])

            # update present fixation position at the end of the trial
            present_pos = present_pos + saccade_vector

        self.trial_saccade_target_positions = np.array(trial_saccade_target_positions)
        self.trial_distractor_positions = np.array(trial_distractor_positions)
        self.saccade_distractor_directions = np.array(saccade_distractor_directions)


        ##################################################################################
        ##
        ##  And, the stimuli
        ##
        ##################################################################################

        size_fixation_pix = self.deg2pix(self.config['size_fixation_deg'])
        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='red',
                                           sf=0,
                                           pos=(0,0))
        
        size_distractor_pix = self.deg2pix(self.config['size_distractor_deg'])
        self.distractor = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_distractor_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0,
                                           pos=(0,0))
    def run(self):
        """run the session"""
        # cycle through trials

        for ti in range(self.config['n_trials']):

            parameters = {
                'fix_x': self.trial_saccade_target_positions[ti,0],
                'fix_y': self.trial_saccade_target_positions[ti,1],
                'distractor_x': self.trial_distractor_positions[ti,0],
                'distractor_y': self.trial_distractor_positions[ti,1],
                'saccade_direction': self.saccade_distractor_directions[ti,0],
                'distractor_direction': self.saccade_distractor_directions[ti,1],
            }

            parameters.update(self.config)

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
