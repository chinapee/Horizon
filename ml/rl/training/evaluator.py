#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

import logging
logger = logging.getLogger(__name__)


def test_values_from_timeline(discount_factor, reward_timeline):
    result = 0
    for time, reward in reward_timeline.items():
        result += (discount_factor**time) * reward
    return result


class Evaluator(object):
    def __init__(self, trainer, discount_factor):
        self._trainer = trainer
        self._discount_factor = discount_factor
        self.mc_loss = []
        self.td_loss = []

    def report(self, reward_timelines, predictions, td_loss):
        ground_truth = np.array(
            [
                test_values_from_timeline(self._discount_factor, rt)
                for rt in reward_timelines
            ]
        ).reshape(-1, 1)
        mc_loss = float(np.mean(np.abs(ground_truth - predictions)))
        td_loss_mean = float(np.mean(td_loss))
        self.mc_loss.append(mc_loss)
        self.td_loss.append(td_loss_mean)
        logger.info(
            "MC LOSS: {0:.3f} TD LOSS: {1:.3f}".format(mc_loss, td_loss_mean)
        )

    def get_recent_td_loss(self):
        begin = max(0, len(self.td_loss) - 100)
        return np.mean(np.array(self.td_loss[begin:]))

    def get_recent_mc_loss(self):
        begin = max(0, len(self.mc_loss) - 100)
        return np.mean(np.array(self.mc_loss[begin:]))
