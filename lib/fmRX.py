#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flowgraphs.fmRX import fmRX as GeneratedFmRX


class fmRX(GeneratedFmRX):
    def __init__(self, control):
        self.ctl = control
        super().__init__()

    def set_swap__(self, swap__):
        self.swap__ = swap__
        if swap__ == 1:
            self.ctl.switch_to_tx(self)
