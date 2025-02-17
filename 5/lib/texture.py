# Library for texture synthesis, with various methods

from typing import Tuple, List
from array import ArrayType
import numpy as np
from itertools import repeat

from steerable import *
from mio import *
from histogram import *
from fft import *

# Texture synthesis using steerable pyramids
def texture_synthesis_steerable(_img: ArrayType, K: int, Q: int, _iter: int = 5, _shp: Tuple[int, int] = None) -> ArrayType:
    # Creating image steerable pyramids
    _p = pyramids_fast(_img, K, Q, _cvt=False)
    # Creating the noise
    _n = np.random.normal(0.5, 0.4, _img.shape) if _shp == None else np.random.normal(0.5, 0.4, _shp)
    # Matching the histogram
    _n = match_hist(_n, _img)
    # Loop
    for _ in range(_iter):
        # Creating the steerable pyramids
        _pn = pyramids_fast(_n, K, Q, _cvt=False)
        # Matching histograms
            # H0
        _pn[0][0] = match_hist(_pn[0][0], _p[0][0])
            # Final LOW
        _pn[-1][0] = match_hist(_pn[-1][0], _p[-1][0])
            # Orientations
        for i in range(K):
            for j in range(Q):
                _pn[i+1][j] = match_hist(_pn[i+1][j], _p[i+1][j])
        # Recreating the image
        _n = recreate_fast(_pn)
        # Matching the histograms
        _n = match_hist(_n, _img)
        # Writing
        write(f'iter_{_}.png', _n*255)
    # Return the image
    return _n

# Texture synthesis using steerable pyramids
def texture_synthesis_steerable_C(_imgF: ArrayType, K: int, Q: int, _iter: int = 5, _shp: Tuple[int, int] = None) -> ArrayType:
    _M = np.random.normal(0.5, 0.4, _imgF.shape[:2]) if _shp == None else np.random.normal(0.5, 0.4, _shp)
    _F = np.zeros(_imgF.shape) if _shp == None else np.zeros(list(_shp)+[3])
    for ii in [0,1,2]:
        _img = _imgF[:,:,ii]
        # Creating image steerable pyramids
        _p = pyramids_fast(_img, K, Q, _cvt=False)
        # Creating the noise
        _n = _M
        # Matching the histogram
        _n = match_hist(_n, _img)
        # Loop
        for _ in range(_iter):
            # Creating the steerable pyramids
            _pn = pyramids_fast(_n, K, Q, _cvt=False)
            # Matching histograms
                # H0
            _pn[0][0] = match_hist(_pn[0][0], _p[0][0])
                # Final LOW
            _pn[-1][0] = match_hist(_pn[-1][0], _p[-1][0])
                # Orientations
            for i in range(K):
                for j in range(Q):
                    _pn[i+1][j] = match_hist(_pn[i+1][j], _p[i+1][j])
            # Recreating the image
            _n = recreate_fast(_pn)
            # Matching the histograms
            _n = match_hist(_n, _img)
        _F[:,:,ii] = _n
    # Return the image
    return _F