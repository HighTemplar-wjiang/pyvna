# pyvna
A python library to make your life easier when using VNA.

## Features
- Acquiring S-parameters from VNA, plotting and dumping to csv file.
- Measurement port conversion.

## Dependencies
- Python3 
- Numpy
- Matplotlib
- pyvisa (also make sure VISA library is installed.)

## Usage
### Acquiring data from VNA.
#### Preparing
1. Make sure your VNA is connected to your PC (via USB is recommended.)
1. Set up measurement parameters (stimulus frequencies, measurement power, measurement bandwidth, etc.) in VNA, **EXCEPT** traces.
1. In your console (CMD in Windows, terminal in Linux/Unix), run *python sparamreader.py*, parameter traces (e.g., S11, S12, S21, S22) will be configured and displayed in VNA.
1. Check if the traces are correctly displayed in your VNA. If not, make sure there is no command error, and your configurations are correct.
1. Select **Goto Local** in your VNA, finish the calibration process.

#### Measuring
1. Connect your hardware to be measured. Wait util the measurement process to finish.
1. Go back to your console, press Enter to continue. Measurement data will be downloaded from VNA.
1. Enter the filename you wish for saving the data. Figures for the acquired data will show on the screen after then.
1. Close all figures for another measurement.

### Data processing
Using Jupyter for data processing is recommended, please refer to process_data_example.ipynb. All data files (csv format) are in the ./data directory.
#### Data format
- First line is the head.
- Data start at the second line.
- First column is the stimulus frequency, measurement data are in the following columns (e.g., S11_real, S11_imag, etc.).

## Hacking
You may edit the scripts by yourself, I have added doc strings for most methods (following [Google python style guide](https://google.github.io/styleguide/pyguide.html#Comments)).
