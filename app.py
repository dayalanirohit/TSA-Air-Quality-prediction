import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import streamlit as st

# Function to train ARIMA model for a specific column and make predictions for the next 48 hours
def train_arima_predict(data, col_name):
    train_data = data[col_name][:-48]  # Use all but the last 48 hours for training
    model = ARIMA(train_data, order=(1, 1, 1))
    model_fit = model.fit()
    
    # Make predictions for the next 48 hours
    forecast = model_fit.forecast(steps=48)
    
    return model_fit, forecast

# Streamlit app
st.title('Air Pollution Prediction Using ARIMA Model')

# File uploader for the dataset
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

    # Rename columns for clarity if needed
    data.columns = ['Date', 'Time', 'CO_true', 'PT08_S1', 'NMHC_true', 'Benzene_true', 'PT08_S2', 
                    'NOx_true', 'PT08_S3', 'NO2_true', 'PT08_S4', 'PT08_S5', 'Temperature', 'RH', 'AH']

    # Drop original Date and Time columns
    data.drop(['Date', 'Time'], axis=1, inplace=True)

    # Handle missing values
    data.replace(-200, np.nan, inplace=True)
    data.fillna(method='ffill', inplace=True)

    # List of columns to iterate through
    columns_to_forecast = ['CO_true', 'PT08_S1', 'NMHC_true', 'Benzene_true', 'PT08_S2', 
                           'NOx_true', 'PT08_S3', 'NO2_true', 'PT08_S4', 'PT08_S5', 'Temperature', 'RH', 'AH']

    # Create a DataFrame to store predictions
    predictions_df = pd.DataFrame(columns=columns_to_forecast)

    st.write("## Predictions and RMSE for each pollutant")
    
    # Loop through columns and train ARIMA models with different orders
    for col in columns_to_forecast:
        model_fit, forecast = train_arima_predict(data, col)
        
        # Append predictions to the DataFrame
        predictions_df[col] = forecast

        # Calculate RMSE for the forecast
        test_data = data[col][-48:]  # Last 48 hours data for testing
        rmse = np.sqrt(mean_squared_error(test_data, forecast))
        
        st.write(f"### {col} column:")
        st.write(f"RMSE: {rmse}")
        
        forecast_df = pd.DataFrame({
            'Prediction': forecast
        })
        st.write(forecast_df)

    # Save predictions to a new Excel file
    predictions_df.to_excel('predictions.xlsx', index=False)
    st.write("Predictions saved to 'predictions.xlsx'")
else:
    st.write("Please upload an Excel file to proceed.")
