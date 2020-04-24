# MIT License
#
# Copyright (C) IBM Corporation 2020
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This module implements a rounding to the classifier output.
"""
import logging

import numpy as np

from art.defences.postprocessor.postprocessor import Postprocessor

logger = logging.getLogger(__name__)


class Rounded(Postprocessor):
    """
    Implementation of a postprocessor based on rounding classifier output.
    """

    params = ["decimals"]

    def __init__(
        self, decimals: int = 3, apply_fit: bool = False, apply_predict: bool = True
    ) -> None:
        """
        Create a Rounded postprocessor.

        :param decimals: Number of decimal places after the decimal point.
        :param apply_fit: True if applied during fitting/training.
        :param apply_predict: True if applied during predicting.
        """
        super(Rounded, self).__init__()
        self._is_fitted = True
        self._apply_fit = apply_fit
        self._apply_predict = apply_predict
        self.set_params(decimals=decimals)

    @property
    def apply_fit(self) -> bool:
        return self._apply_fit

    @property
    def apply_predict(self) -> bool:
        return self._apply_predict

    def __call__(self, preds: np.ndarray) -> np.ndarray:
        """
        Perform model postprocessing and return postprocessed output.

        :param preds: model output to be postprocessed.
        :return: Postprocessed model output.
        """
        return np.around(preds, decimals=self.decimals)

    def fit(self, preds: np.ndarray, **kwargs) -> None:
        """
        No parameters to learn for this method; do nothing.
        """
        pass

    def set_params(self, **kwargs) -> bool:
        """
        Take in a dictionary of parameters and apply checks before saving them as attributes.

        :param decimals: Number of decimal places after the decimal point.
        :type decimals: `int`
        :return: `True` when parsing was successful.
        """
        # Save defence-specific parameters
        super(Rounded, self).set_params(**kwargs)

        if not isinstance(self.decimals, (int, np.int)) or self.decimals <= 0:
            raise ValueError("Number of decimal places must be a positive integer.")

        return True
