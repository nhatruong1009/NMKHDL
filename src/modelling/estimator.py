from sklearn.base import BaseEstimator, RegressorMixin
from statsmodels.tsa.api import SARIMAX
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense 
from sklearn.linear_model import LinearRegression

class SarimaxEstimator(BaseEstimator, RegressorMixin):
    def __init__(self, order=(5,1,0), seasonal_order=(1,1,1,12)):
        self.order = order
        self.seasonal_order = seasonal_order
    def fit(self, X, y):
        return self
    def predict(self, X):
        pred = []
        for i in range(X.shape[0]):
            self.model = SARIMAX(X[i], order=self.order, seasonal_order=self.seasonal_order)
            self.model_fit = self.model.fit()
            pred.append(self.model_fit.forecast()[0])
        return pred
    
class LinearRegressionEstimator(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.model = LinearRegression()
    def fit(self, X, y):
        self.model.fit(X.reshape(X.shape[0],X.shape[1]), y)
        return self
    def predict(self, X):
        return self.model.predict(X.reshape(X.shape[0],X.shape[1]))

    
class LSTMEstimator(BaseEstimator, RegressorMixin):
    def __init__(self, epochs=5, batch_size=32, neurons=200):
        self.epochs = epochs
        self.batch_size = batch_size
        self.neurons = neurons
    def fit(self, X, y):
        self.model = Sequential()
        self.model.add(LSTM(self.neurons, return_sequences=True, input_shape=(X.shape[1], 1)))
        self.model.add(LSTM(self.neurons, return_sequences=False))
        self.model.add(Dense(100))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(X, y, batch_size=self.batch_size, epochs=self.epochs)
        return self
    def predict(self, X):
        return self.model.predict(X)
    

class Estimator(BaseEstimator):
    def __init__(self, estimator = LinearRegression()):
        self.estimator = estimator

    def fit(self, X, y=None, **kwargs):
        self.estimator.fit(X, y)
        return self

    def predict(self, X, y=None):
        return self.estimator.predict(X)