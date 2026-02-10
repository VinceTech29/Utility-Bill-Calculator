# Utility Bill Calculator

A **Python PyQt6 desktop application** to calculate electricity bills and additional utility charges, generate a detailed receipt, and save it as an image. Designed for households, renters, or small communities.

## Features

- **Electricity Bill Calculation**: Computes the bill based on previous and current meter readings.  
- **Additional Bills**: Add multiple dynamic utility charges like water, internet, or garbage fees.  
- **Receipt Generation**: Generates a neatly formatted receipt showing all charges, totals, and date/time.  
- **Save as Image**: Export the receipt as a PNG file for printing or sharing.  
- **User-Friendly Interface**: Intuitive layout with scrollable area for multiple bills.  
- **Error Handling**: Validates inputs and prevents negative electricity consumption or invalid amounts.

## Dependencies

This application requires Python 3.10+ and the following packages:
PyQt6
pyinstaller if you want to package the app as a standalone executable

Install all dependencies:
pip install PyQt6
pip install pyinstaller

Or, if using requirements.txt:

PyQt6>=6.5
pyinstaller>=5.13
