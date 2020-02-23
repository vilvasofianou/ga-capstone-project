# -*- coding: utf-8 -*-
import numpy as np


def FtoC(temp_in_F):
    return (temp_in_F - 32) * (5 / 9)


def MtoK(dist_in_M):
    return dist_in_M * 1.609


def to_float(string):
    try:
        return float(string)
    except:
        return np.nan
