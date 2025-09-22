# Air Quality Forecasting using ARIMA

This project forecasts hourly air pollutant concentrations for the next 48 hours based on the Air Quality UCI dataset.

---

##  Problem Statement
The goal is to build a time series model that accurately predicts various air quality metrics and environmental factors. Model performance is evaluated using the Root Mean Square Error (RMSE) on the final 48 hours of the dataset.

---

##  Model Used
The project utilizes a univariate **ARIMA (Autoregressive Integrated Moving Average)** model. A separate, optimized ARIMA model is trained for each of the 13 target variables in the dataset.

---

##  Tech Stack
* **Python 3.x**
* **Pandas**: For data manipulation and cleaning.
* **Statsmodels**: For ARIMA model implementation.
* **Scikit-learn**: For feature scaling (`MinMaxScaler`) and performance evaluation (`mean_squared_error`).
* **Numpy**: For numerical operations.

---

##  Improvements
The original model was enhanced to improve its accuracy and robustness:

* **Hyperparameter Tuning**: Instead of using a static `ARIMA(1,1,1)` order, a grid search is now performed for each time series to find the optimal `(p, d, q)` parameters. The best model order is selected based on the lowest **Akaike Information Criterion (AIC)**, which ensures a balance between model fit and complexity.

* **Feature Scaling**: A `MinMaxScaler` is applied to scale all time series data to a `[0, 1]` range before training. This improves the numerical stability of the model during the optimization process. Forecasts are then inverse-transformed back to their original scale for accurate RMSE evaluation.

---
