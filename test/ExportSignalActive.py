import niScope

scope = niScope.Scope("Dev4")
scope.ConfigureHorizontalTiming()
scope.ConfigureVertical()
scope.ConfigureTrigger()
scope.ExportSignal(signal=4, outputTerminal='VAL_RTSI_0')
raw_input("signal exported")
scope.Commit()
raw_input("committed")
scope.InitiateAcquistion()
raw_input("Acquisition initiated")
