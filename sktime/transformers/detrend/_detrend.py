#!/usr/bin/env python3 -u
# coding: utf-8

__all__ = [
    "ResidualDetrender"
]
__author__ = ["Markus Löning"]

from sklearn.base import clone
from sktime.forecasting._base import MetaForecasterMixin
from sktime.transformers.detrend._base import BaseSeriesToSeriesTransformer
from sktime.utils.validation.forecasting import check_y


class ResidualDetrender(MetaForecasterMixin, BaseSeriesToSeriesTransformer):

    def __init__(self, forecaster):
        self.forecaster = forecaster
        self.forecaster_ = None
        super(ResidualDetrender, self).__init__()

    def fit(self, y_train, X_train=None):
        forecaster = clone(self.forecaster)
        self.forecaster_ = forecaster.fit(y_train, X_train=X_train)
        self._is_fitted = True
        return self

    def transform(self, y, X=None):
        self._check_is_fitted()
        y = check_y(y)
        fh = self._get_relative_fh(y)
        y_pred = self.forecaster_.predict(fh=fh, X=X)
        return y - y_pred

    def inverse_transform(self, y, X=None):
        self._check_is_fitted()
        y = check_y(y)
        fh = self._get_relative_fh(y)
        y_pred = self.forecaster_.predict(fh=fh, X=X)
        return y + y_pred

    def _get_relative_fh(self, y):
        return y.index.values - self.forecaster_.cutoff
