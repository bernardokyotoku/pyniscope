# PyNiScope 
provides a Python package niscope that wraps the NI-SCOPE driver software for Python using ctypes.
The package is tested with NI-SCOPE library version 3.3.2 using PCI-5122 cards Windows XP, and PXI-5114 on Windows 7.

## Basic usage
``` import matplotlib.pyplot as plt import niScope

scope = niScope.Scope() scope.ConfigureHorizontalTiming() scope.ConfigureVertical() scope.ConfigureTrigger("Edge",TRIGGER_SOURCE.EXTERNAL,2.5,SLOPE.POSITIVE,0,0) scope.InitiateAcquisition() raw_input("Enter") data = scope.Fetch() scope.close() plt.plot(data) plt.show() ```

## Requirements
The national instruments NI-Scope drivers are required. If you do not have a physical NI scope, it is possible to test pyniscope by installing a simulated instrument in the NI Measurement & Automation Explorer.

[Search ni.com for NI-SCOPE|http://search.ni.com/nisearch/app/main/p/bot/no/ap/tech/lang/en/pg/1/sn/ssnav:dwl/q/ni-scope/]
On linux pyniscope was origionaly tested with NI-SCOPE 3.1, NI-KAL 2.1, and NI-VISA 5.0.
