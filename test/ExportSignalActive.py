from builtins import input
import niscope
from nidaqmx import AnalogOutputTask
import numpy as np

scope = niscope.Scope("Dev4")
task = AnalogOutputTask()
task.create_voltage_channel("Dev3/ao3")
task.configure_timing_sample_clock(source="RTSI0")
data = np.sin(0.5 * np.pi * np.arange(10000))**2
task.write(data)
scope.ConfigureHorizontalTiming(sampleRate=30000, numPts=1000000)
scope.ConfigureVertical()
scope.ConfigureTrigger("Edge")
scope.ExportSignal(signal=4, outputTerminal='VAL_RTSI_0')
input("signal exported")
scope.Commit()
input("committed")
scope.InitiateAcquisition()
input("Acquisition initiated")
