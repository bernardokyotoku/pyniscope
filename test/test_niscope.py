from __future__ import print_function
# from builtins import object
import niscope
import unittest

class TestNIScope(unittest.TestCase):
    def setUp(self):
        self.scope = niscope.Scope("Dev4")

    def tearDown(self):
        self.scope.close()

    def test_load(self):
        pass

    def test_acquisition(self):
        self.scope.ConfigureHorizontalTiming()
        self.scope.ConfigureVertical(channelList="0")
        self.scope.ConfigureTrigger('Immediate')
        self.scope.InitiateAcquisition()

    def test_acquisition_2channels(self):
        self.scope.ConfigureHorizontalTiming()
        self.scope.ConfigureVertical(channelList="0")
        self.scope.ConfigureVertical(channelList="1")
        self.scope.ConfigureTrigger('Immediate')
        self.scope.InitiateAcquisition()
        import numpy
        data = numpy.zeros((1000, 2), dtype=numpy.float64)
        self.scope.Fetch("0,1", data)

    def test_acquisition_2channels_uninitialized_buffer(self):
        self.scope.ConfigureHorizontalTiming()
        self.scope.ConfigureVertical(channelList="0")
        self.scope.ConfigureVertical(channelList="1")
        self.scope.ConfigureTrigger('Immediate')
        self.scope.InitiateAcquisition()
        import numpy
        data = self.scope.Fetch("0,1")

    def test_acquisition_2channels_2records(self):
        self.scope.ConfigureHorizontalTiming(numRecords=2)
        self.scope.ConfigureVertical(channelList="0")
        self.scope.ConfigureVertical(channelList="1")
        self.scope.ConfigureTrigger('Immediate')
        self.scope.InitiateAcquisition()
        import numpy
        data = numpy.zeros((1000, 4), dtype=numpy.float64)
        self.scope.Fetch("0,1", data)
        for info in self.scope.info:
            print("relativeInitialX=", info.relativeInitialX)
            print("absoluteInitialX", info.absoluteInitialX)
            print("xIncrement", info.xIncrement)
            print("actualSamples", info.actualSamples)
            print("gain", info.gain)
            print("offset", info.offset)
        del data

    def test_autosetup(self):
        self.scope.AutoSetup()

    def test_configure_acquisition(self):
        self.scope.ConfigureAcquisition()

    def test_configure_chan_characteristics(self):
        self.scope.ConfigureChanCharacteristics("0", 1000000, 20)

    def test_set_attribute(self):
        self.scope.SetAttribute(
            niscope.NISCOPE_ATTR_ACQUISITION_TYPE,
            niscope.VAL.NORMAL, "")

    def test_get_attribute(self):
        value = self.scope.GetAttribute(
            niscope.NISCOPE_ATTR_ACQUISITION_TYPE,
            niscope.ViInt32)
        assert value == niscope.VAL.NORMAL

    def test_check_attribute(self):
        self.scope.CheckAttribute("",
                                  niscope.NISCOPE_ATTR_ACQUISITION_TYPE,
                                  niscope.VAL.NORMAL)

    def test_ActualSamplingRate(self):
        self.scope.ConfigureHorizontalTiming()
        self.scope.ActualSamplingRate

    def test_AcquistionStatus(self):
        assert self.scope.AcquisitionStatus() == 1

    def test_ExportSignal(self):
        assert self.scope.ExportSignal() == 0

    def test_NumRecords_getter(self):
        self.scope.ConfigureHorizontalTiming(numRecords=2)
        assert self.scope.NumRecords == 2

    def test_NumRecords_setter(self):
        self.scope.ConfigureHorizontalTiming(numRecords=2)
        self.scope.NumRecords = 3
        assert self.scope.NumRecords == 3
