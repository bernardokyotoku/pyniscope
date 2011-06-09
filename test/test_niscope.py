class test_niscope:
	def setUp(self):
		import niScope
		self.scope = niScope.Scope()
		
	def tearDown(self):
		self.scope.close()

	
	def test_load(self):
		pass

	def test_aquisition(self):
		self.scope.ConfigureHorizontalTiming()
		self.scope.ConfigureVertical(channelList="0")
		self.scope.ConfigureTrigger('Immediate')
		self.scope.InitiateAcquisition()

	def test_aquisition_2channels(self):
		self.scope.ConfigureHorizontalTiming()
		self.scope.ConfigureVertical(channelList="0")
		self.scope.ConfigureVertical(channelList="1")
		self.scope.ConfigureTrigger('Immediate')
		self.scope.InitiateAcquisition()
		import numpy
		data = numpy.zeros((1000,2),dtype=numpy.float64)
		self.scope.Fetch("0,1",data)

	def test_aquisition_2channels_2records(self):
		self.scope.ConfigureHorizontalTiming(numRecords	= 2)
		self.scope.ConfigureVertical(channelList="0")
		self.scope.ConfigureVertical(channelList="1")
		self.scope.ConfigureTrigger('Immediate')
		self.scope.InitiateAcquisition()
		import numpy
		data = numpy.zeros((1000,4),dtype=numpy.float64)
		self.scope.Fetch("0,1",data)
		for info in self.scope.info:
			print "relativeInitialX=",info.relativeInitialX
			print "absoluteInitialX",info.absoluteInitialX
			print "xIncrement",info.xIncrement
			print "actualSamples",info.actualSamples
			print "gain",info.gain
			print "offset",info.offset
		del data

	def test_autosetup(self):	
		self.scope.AutoSetup()
