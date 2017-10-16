from psychopy.visual import DotStim
import numpy as np
from psychopy.tools.attributetools import attributeSetter, setAttribute


class VonMisesDotStim(DotStim):

    def __init__(self, screen, kappa=1, *args, **kwargs):

        self.kappa = kappa
        super(VonMisesDotStim, self).__init__(screen, *args, **kwargs)
        
    @attributeSetter
    def coherence(self, coherence):   
        self._signalDots = np.ones(self.nDots, dtype=bool)

    @attributeSetter
    def dir(self, dir):
        self.__dict__['dir'] = dir / 180 * np.pi
        self._dotsDir = np.random.vonmises(self.dir, self.kappa, self.nDots)


    def _update_dotsXY(self):

        # Get dead dots
        if self.dotLife > 0:  # if less than zero ignore it
            # decrement. Then dots to be reborn will be negative
            self._dotsLife -= 1
            dead = (self._dotsLife <= 0.0)
            self._dotsLife[dead] = self.dotLife
        else:
            dead = np.zeros(self.nDots, dtype=bool)

        
        # update dead dots
        if sum(dead):
            self._verticesBase[dead, :] = self._newDotsXY(sum(dead))
            self._dotsDir[dead] = np.random.vonmises(self.dir, self.kappa, sum(dead))


        cosDots = np.cos(self._dotsDir)
        sinDots = np.sin(self._dotsDir)

        self._verticesBase[:, 0] += self.speed * cosDots
        self._verticesBase[:, 1] += self.speed * sinDots

        # find Out-of-bounds dots
        if self.fieldShape in (None, 'square', 'sqr'):
            out0 = (np.abs(self._verticesBase[:, 0]) > 0.5*self.fieldSize[0])
            out1 = (np.abs(self._verticesBase[:, 1]) > 0.5*self.fieldSize[1])
            outofbounds = out0 + out1

        elif self.fieldShape == 'circle':
            normXY = self._verticesBase / 0.5 / self.fieldSize
            outofbounds = (np.hypot(normXY[:, 0], normXY[:, 1]) > 1)   

        # update any out of bound dots dots
        if sum(outofbounds):
            self._verticesBase[outofbounds, :] = self._newDotsXY(sum(outofbounds))
            self._dotsDir[outofbounds] = np.random.vonmises(self.dir, self.kappa, sum(outofbounds))

        # update the pixel XY coordinates in pixels (using _BaseVisual class)
        self._updateVertices()
