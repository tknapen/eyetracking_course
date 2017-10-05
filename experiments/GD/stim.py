from psychopy.visual import DotStim
from psychopy import logging, visual
import numpy
import json

import numpy as np

import exptools


class DotSlave(DotStim):

    def __init__(self, win, master, *args, **kwargs):
        self.master = master

        for attribute in [
            'nDots',
            'fieldSize',
            'dotSize',
            'color',
                'colorSpace']:
            kwargs[attribute] = kwargs.get(
                attribute, getattr(self.master, attribute))

        super(DotSlave, self).__init__(win, *args, **kwargs)

    def _update_dotsXY(self):
        self._verticesBase = self.master._verticesBase
        self._updateVertices()
        logging.debug('Updating _verticesBase: %s' % self._verticesBase)

    def _new_dotsXY(self):
        self._verticesBase = self.master._verticesBase
        logging.debug('New _verticesBase: %s' % self._verticesBase)


class BinocularDotStimulus(object):

    def __init__(
            self,
            screen,
            trial,
            session,
            config,
            color='r',
            coherence=0.5):  # ,task):

        assert(color in ['r', 'b'])

        if color == 'r':
            color = [config['red_intensity'], -1, -1]
        if color == 'b':
            color = [-1, -1, config['blue_intensity']]

        self.screen = screen
        self.trial = trial
        self.session = session

        # Get dimensions of bars
        square_size_pix = self.session.deg2pix(config['square_size_deg'])
        height_hbar_squares = int(config['thickness_bars'])
        width_hbar_squares = int(
            self.session.deg2pix(
                config['width_barsquare']) /
            square_size_pix)
        height_vbar_squares = int(
            self.session.deg2pix(
                config['height_barsquare']) /
            square_size_pix -
            2 *
            config['thickness_bars'])
        width_vbar_squares = int(config['thickness_bars'])

        # **** Set up bars ***
        bar_matrix1 = (
            np.random.random(
                (height_hbar_squares,
                 width_hbar_squares)) > 0.5) * 2 - 1
        bar_matrix2 = (
            np.random.random(
                (height_vbar_squares,
                 width_vbar_squares)) > 0.5) * 2 - 1
        bar_matrix3 = (
            np.random.random(
                (height_hbar_squares,
                 width_hbar_squares)) > 0.5) * 2 - 1
        bar_matrix4 = (
            np.random.random(
                (height_vbar_squares,
                 width_vbar_squares)) > 0.5) * 2 - 1

        width_hbar_pix = width_hbar_squares * square_size_pix
        height_hbar_pix = height_hbar_squares * square_size_pix
        width_vbar_pix = width_vbar_squares * square_size_pix
        height_vbar_pix = height_vbar_squares * square_size_pix

        bar1 = visual.ImageStim(
            self.screen, bar_matrix1, size=(
                width_hbar_pix, height_hbar_pix), pos=(
                0, self.session.deg2pix(
                    config['height_barsquare']) / 2.))

        bar2 = visual.ImageStim(
            self.screen, bar_matrix2, size=(
                width_vbar_pix, height_vbar_pix), pos=(
                self.session.deg2pix(
                    config['width_barsquare']) / 2., 0))

        bar3 = visual.ImageStim(
            self.screen, bar_matrix3, size=(
                width_hbar_pix, height_hbar_pix), pos=(
                0, -self.session.deg2pix(
                    config['height_barsquare']) / 2.))

        bar4 = visual.ImageStim(self.screen,
                                bar_matrix4,
                                size=(width_vbar_pix, height_vbar_pix),
                                pos=(-self.session.deg2pix(config['width_barsquare']) / 2., 0))

        self.bars = [bar1, bar2, bar3, bar4]

        # Set up the Random dot motion
        dotsize_pix = self.session.deg2pix(config['dotsize_deg'])
        fieldsize_pix = self.session.deg2pix(config['fieldsize_deg'])

        self.element_master = visual.GratingStim(win=self.screen,
                                                 tex='sin',
                                                 size=dotsize_pix,
                                                 sf=0,
                                                 mask='circle',
                                                 color=color,)

        self.dots = visual.DotStim(win=self.screen,
                                   nDots=config['n_dots'],
                                   element=self.element_master,
                                   fieldSize=fieldsize_pix,
                                   coherence=config['coherence'],
                                   speed=config['speed'],
                                   dotLife=1e6,
                                   fieldShape='circle')

    def draw(self):

        for bar in self.bars:
            bar.draw()

        self.dots.draw()
