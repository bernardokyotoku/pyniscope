__all__ = []

from ordered_symbols import *
import os
import sys
import textwrap
import numpy 
from numpy import ctypeslib,zeros,float64
from ctypes import create_string_buffer,byref,util
import ctypes
import ctypes.util
import warnings
from niScopeTypes import *
from niScopeTypes import ViInt32


libname = 'niScope_32'
#    include_niScope_h = os.environ['NIIVIPATH']+'Include\\niScope.h'
lib = util.find_library(libname)
if lib is None:
	if os.name=='posix':
		print 'libniScope_32.so not found, is NI-SCOPE installed?'
	if os.name=='nt':
		print 'niScope.dll not found'
if os.name=='posix':
	libniScope = ctypes.cdll.LoadLibrary(lib)
if os.name=='nt':
	libniScope = ctypes.windll.LoadLibrary(lib)
		
class Scope(ViSession):
		
	def CALL(self,name, *args):
		"""
		Calls libniScope function "name" and arguments "args".
		"""
		funcname = 'niScope_' + name
		func = getattr(libniScope, funcname)
		new_args = []
		for a in args:
			if isinstance (a, unicode):
				print name, 'argument',a, 'is unicode'
				new_args.append (str (a))
			else:
				new_args.append (a)
		status = func(*new_args)
		if status is not 0:
			message = self.errorHandler(status)
			raise Exception(message)
		return status
		
	def __init__(self,resourceName="Dev1",IDQuery=False,resetDevice=False):
		self.info = wfmInfo()
		ViSession.__init__(self,0)
		status = self.CALL('init',
				ViRsrc(resourceName),
				ViBoolean(IDQuery),
				ViBoolean(resetDevice),
				byref(self))
		return None

	def AutoSetup(self):
		"""
		Automatically configures the instrument. When you call this 
		function, the digitizer senses the input signal and automati-
		cally configures many of the instrument settings. If no signal 
		is found on any analog input channel, a warning is returned, and
		all channels are enabled. A channel is considered to have a 
		signal present if the signal is at least 10% of the smallest 
		vertical range available for that channel. 
		"""
		status = self.CALL("AutoSetup",self)
		return status

	def ConfigureAcquisition(self,acqType=VAL.NORMAL):
		"""
		Configures how the digitizer acquires data and fills the wave-
		form record.
		"""
		acquisitionType = ViInt32(acqType)
		status = self.CALL("ConfigureAcquisition",self,acquisitionType)

	def ConfigureHorizontalTiming(self,
			sampleRate	= 20000000,
			numPts		= 1000,
			refPosition	= 0.5,
			numRecords	= 1,
			enforceRealtime	= True):
		"""
		Configures the common properties of the horizontal subsystem for
		a multirecord acquisition in terms of minimum sample rate.
		"""
		status = self.CALL('ConfigureHorizontalTiming',self,
				ViReal64(sampleRate),
				ViInt32(numPts),
				ViReal64(refPosition),
				ViInt32(numRecords),
				ViBoolean(enforceRealtime))
		return 
		
	def ConfigureChanCharacteristics(self,chanList,impedance,maxFrequency):
		"""
		Configures the attributes that control the electrical character-
		istics of the channel the input impedance and the bandwidth.
		"""
		status = self.CALL("ConfigureChanCharacteristics",self,
				ViConstString(chanList),
				ViReal64(impedance),
				ViReal64(maxFrequency))
		return status
		
	def ConfigureVertical(self,
		channelList="0",
		voltageRange=10,
		offset=0,
		coupling=COUPLING.DC,
		probeAttenuation=1,
		enabled=True):
		"""
		Configures the most commonly configured attributes of the digi-
		tizer vertical subsystem, such as the range, offset, coupling, 
		probe attenuation, and the channel.
		"""
		status = self.CALL("ConfigureVertical",self,
			ViConstString(channelList),
			ViReal64(voltageRange),
			ViReal64(offset),
			ViInt32(coupling),
			ViReal64(probeAttenuation),
			ViBoolean(enabled))
		return status
	
	def ConfigureTrigger(self,trigger_type='Immediate',**settings):
		"""
		Configures scope trigger type and settings. For each trigger 
		type distinct settings must be defined.
		
		Parameter		Valid Values
		
		trigger_type		'Edge'
					'Hysteresis'
					'Window'
					'Window'
					'Software'
					'Immediate'
					'Digital'
					'Video'
	
	
		Trigger Type	Settings	Default Value	
		
		'Immediate'	N/A
		
		'Edge'		triggerSource 	TRIGGER_SOURCE.EXTERNAL
				level 		0
				slope 		SLOPE.POSITIVE
				triggerCoupling COUPLING.DC
				holdoff		0
				delay 		0
		
		'Hysteresis'	triggerSource  '0'
				level 	 	0
				hysteresis	0.05
				slope		SLOPE.POSITIVE
				triggerCoupling	COUPLING.DC
				holdoff		0
				delay		0
			
		'Window'	triggerSource	'0'	               
		                lowLevel	0                       
		                highLevel	0.1		               					windowMode	TRIGGER_WINDOW.ENTERING_WINDOW	
				triggerCoupling	COUPLING.DC         	
				holdoff		0
				delay		0		
				
		'Software'	holdoff		0
				delay		0	
		
		'Digital'	triggerSource	'0'
				slope		SLOPE.POSITIVE
				holdoff		0
				delay 		0
		
		'Video'		triggerSource	'0'
				enableDCRestore False								signalFormat	TV_TRIGGER_SIGNAL_FORMAT.VAL_PAL				event		TV_TRIGGER_EVENT.FIELD1	
				lineNumber	0
				polarity	TV_TRIGGER_POLARITY.TV_POSITIVE
				triggerCoupling	COUPLING.DC
				holdoff		0
				delay           0 
		"""
		args = {
		'Edge':lambda 
			triggerSource 	= TRIGGER_SOURCE.EXTERNAL ,
			level 		= 0                       ,
			slope 		= SLOPE.POSITIVE          ,
			triggerCoupling = COUPLING.DC     ,
			holdoff 	= 0                       ,
			delay 		= 0
				:(					
			ViConstString	(triggerSource	),
			ViReal64	(level			),
			ViInt32		(slope			),
			ViInt32		(triggerCoupling),
			ViReal64	(holdoff		),
			ViReal64	(delay			)
			),
		'Hysteresis':lambda
			triggerSource   = '0'                 ,
			level  		= 0	              ,
			hysteresis	= 0.05                ,
			slope		= SLOPE.POSITIVE      ,
			triggerCoupling = COUPLING.DC         ,
			holdoff		= 0                   ,
			delay		= 0
			:(
			ViConstString 	(triggerSource	),
			ViReal64	(level		),
			ViReal64 	(hysteresis	),
			ViInt32		(slope		),
			ViInt32		(triggerCoupling),
			ViReal64	(holdoff	),
			ViReal64	(delay		)
			),
		'Window':lambda
			triggerSource = '0'	           ,
			lowLevel = 0                ,
			highLevel = 0.1		   ,
			windowMode = TRIGGER_WINDOW.ENTERING_WINDOW,
			triggerCoupling	= COUPLING.DC      ,
			holdoff		= 0	           ,
			delay		= 0		
			:(
			ViConstString 	(triggerSource		),
			ViReal64	(lowLevel		),
			ViReal64 	(highLevel		),
			ViInt32 	(windowMode		),
			ViInt32 	(triggerCoupling	),
			ViReal64 	(holdoff		),
			ViReal64 	(delay			)
			),
		'Software':lambda
			holdoff	= 0,
			delay	= 0	
			:(
			ViReal64 	(holdoff	),
			ViReal64	(delay		)
			),
		'Immediate':lambda:(),
		'Digital':lambda 
			triggerSource	= '0'           ,
			slope		= SLOPE.POSITIVE,
			holdoff		= 0             ,
			delay 		= 0
			:(
			ViConstString 	(triggerSource	),
			ViInt32		(slope		),
			ViReal64 	(holdoff	),
			ViReal64 	(delay		)
			),
		'Video':lambda
			triggerSource	= '0'	                  	,
			enableDCRestore = False           		,
			signalFormat	= TV_TRIGGER_SIGNAL_FORMAT.VAL_PAL,
			event		= TV_TRIGGER_EVENT.FIELD1	,
			lineNumber	= 0				,
			polarity	= TV_TRIGGER_POLARITY.POSITIVE	, 
			triggerCoupling	= COUPLING.DC			,
			holdoff		= 0				,
			delay           = 0
			:(				
			ViConstString 		(triggerSource		),
			ViBoolean 		(enableDCestore		),
			ATTR_TV_TRIGGER_SIGNAL_FORMAT	(signalFormat	),
			ViInt32 		(event			),	
			ViInt32 		(lineNumber		),
			ViInt32 		(polarity		),
			ViInt32 		(triggerCoupling	),
			ViReal64 		(holdoff		),	
			ViReal64 		(delay			)
			),
		}[trigger_type](**settings)
		status = self.CALL("ConfigureTrigger"+trigger_type,self,*args)

	def ExportSignal(self,signal=NISCOPE_VAL_REF_TRIGGER
			,outputTerminal=NISCOPE_VAL_RTSI_0
			,signalIdentifier=""):
		"""
Configures the digitizer to generate a signal that other devices can detect when
configured for digital triggering or sharing clocks. The signal parameter speci-
fies what condition causes the digitizer to generate the signal. The 
outputTerminal parameter specifies where to send the signal on the hardware 
(such as a PFI connector or RTSI line).

In cases where multiple instances of a particular signal exist, use the 
signalIdentifier input to specify which instance to control. For normal signals,
only one instance exists and you should leave this parameter set to the empty 
string. You can call this function multiple times and set each available line to
a different signal.

To unprogram a specific line on device, call this function with the signal you 
no longer want to export and set outputTerminal to NISCOPE_VAL_NONE.
		"""

		status = self.CALL("ExportSignal",self,
				ViInt32(signal),
				ViConstString(signalIdentifier),
				ViConstString(outputTerminal))
		return status
		
	def InitiateAcquisition(self):
		"""
		Initiates a waveform acquisition.

		After calling this function, the digitizer leaves the Idle state
		and waits for a trigger. The digitizer acquires a waveform for 
		each channel you enable with ConfigureVertical.
		"""
		status = self.CALL("InitiateAcquisition",self)
		
	def Abort(self):
		"""
		Aborts an acquisition and returns the digitizer to the Idle 
		state. Call this function if the digitizer times out waiting for
		a trigger.
		"""
		status = self.CALL("Abort",self)
		return status
		
	def AcquisitionStatus(self):
		"""
		Returns status information about the acquisition to the status 
		output parameter.
		"""
		status = self.CALL("AcquisitionStatus",self,
			byref(ViInt32(acq_status)))
		return status.value
		
	def Commit(self):
		"""
		Commits to hardware all the parameter settings associated with 
		the task. Use this function if you want a parameter change to be
		immediately reflected in the hardware. This function is support-
		ed for the NI 5122/5124 only.
		"""
		status = self.CALL("Commit",self)

	def GetAttribute(self, attribute, attrType, channelList=""):
		"""
		Queries the value of an attribute. You can use this 
		function to get the values of instrument-specific attributes and
		inherent IVI attributes. If the attribute represents an instru-
		ment state, this function performs instrument I/O in the follow-
		ing cases:

		State caching is disabled for the entire session or for the par-
		ticular attribute.
		State caching is enabled and the currently cached value is inva-
		lid.
		"""
		var = attrType()
		self.CALL("GetAttribute"+attrType.__name__,
				self,
				ViConstString(channelList),
				ViAttr(attribute),
				byref(var))
		return var.value

	def SetAttribute(self, attribute, value, channelList=""):
		"""
		Sets the value an attribute. This is a low-level function that 
		you can use to set the values of instrument-specific attributes 
		and inherent IVI attributes. If the attribute represents an 
		instrument state, this function performs instrument I/O in the 
		following cases:

		State caching is disabled for the entire session or for the par-
		ticular attribute.
		State caching is enabled and the currently cached value is inva
		lid or is different than the value you specify.
		"""
		attrType = { 	float:ViReal64,
				int:ViInt32,
				long:ViInt32,
				bool:ViBoolean,
				Scope:ViSession,
				str:ViString,
				} [type(value)]
		status = self.CALL("SetAttribute"+attrType.__name__,
				self,
				ViConstString(channelList),
				ViAttr(attribute),
				attrType(value))
		return status

	def CheckAttribute(self, channelList, attribute, value):
		"""
		Verifies the validity of a value you specify for an attribute.
		"""
		attrType = { 	float:ViReal64,
				int:ViInt32,
				long:ViInt32,
				bool:ViBoolean,
				Scope:ViSession,
				str:ViString,
				} [type(value)]
		status = self.CALL("CheckAttribute"+attrType.__name__,
				self,
				ViConstString(channelList),
				ViAttr(attribute),
				attrType(value))
		return status

	def Fetch(self,
		channelList="0",
		data=zeros((1000,1),order="F",dtype=float64),
		timeout=1,):
		"""
		Returns the waveform from a previously initiated acquisition 
		that the digitizer acquires for the specified channel. 
		
		numpy array needs to be Fortran ordered.
		"""
		
		data_type = {
			numpy.float64 	:''	        ,
			numpy.int8  	:'Binary8'  ,
			numpy.int16	:'Binary16' ,
			numpy.int32 	:'Binary32' }[data.dtype.type]

		numSamples = data.shape[0]
		numRec = data.shape[1]
		numWfms = self.ActualNumWfms(channelList)
		recLength = self.ActualRecordLength
		assert numWfms == numRec
		wfmInfoArray = wfmInfo*numWfms
		self.info = wfmInfoArray()
        
		status = self.CALL("Fetch"+data_type,self,
			ViConstString(channelList),
			ViReal64(timeout),
			ViInt32(numSamples),
			data.ctypes.data,
			byref(self.info)
			)
		return data

	@property
	def AllowMoreRecordsThanMemory(self):
		return self.SetAttribute(
				NISCOPE_ATTR_ALLOW_MORE_RECORDS_THAN_MEMORY,
				bool)
	
	@AllowMoreRecordsThanMemory.setter
	def AllowMoreRecordsThanMemory(self,value):
		self.SetAttribute(NISCOPE_ATTR_ALLOW_MORE_RECORDS_THAN_MEMORY,
				bool(value))

	@property
	def NumRecords(self):
		"""
Specifies the number of records to acquire. Can be used for multirecord acquisi-
tions and single record acquisitions. Setting this attribute to 1 indicates a 
single record acquisition.
		"""
		return self.GetAttribute(NISCOPE_ATTR_HORZ_NUM_RECORDS, ViInt32)

	@NumRecords.setter
	def NumRecords(self,value):
		self.SetAttribute(NISCOPE_ATTR_HORZ_NUM_RECORDS, int(value))

	@property
	def ActualRecordLength(self):
		"""
		Returns the actual number of points the digitizer acquires for
		each channel. After configuring the digitizer for an acquisition
		, call this function to determine the size of the waveforms that
		the digitizer acquires. The value is equal to or greater than 
		the minimum number of points specified in any of the Configure 
		Horizontal functions.

		Allocate a ViReal64 array of this size or greater to pass as the
		waveformArray of the ReadWaveform and FetchWaveform functions. 
		"""
		record = ViInt32()
		self.CALL("ActualRecordLength",self,byref(record))
		return record.value

	def ActualNumWfms(self,channelList = "0"):
		"""
		Helps you to declare appropriately sized waveforms. NI-SCOPE 
		handles the channel list parsing for you.
		"""
		chan = ViConstString(channelList)
		numWfms = ViInt32()
		self.CALL("ActualNumWfms",self,chan,byref(numWfms))
		return numWfms.value

	@property
	def ActualSamplingRate(self):
		return self.GetAttribute(NISCOPE_ATTR_HORZ_SAMPLE_RATE,ViReal64)

	def read(self):
		self.ConfigureHorizontalTiming()
		self.ConfigureVertical()
		self.ConfigureTrigger()
		self.InitiateAcquisition()
		data = self.Fetch()
		self.close()
		return data
	
	def close(self):
		"""
		When you are finished using an instrument driver session, you 
		must call this function to perform the following actions:
		"""
		status = self.CALL("close",self)

	def errorHandler (self,errorCode):
		MAX_FUNCTION_NAME_SIZE 	 = 55
		IVI_MAX_MESSAGE_LEN      = 255
		IVI_MAX_MESSAGE_BUF_SIZE = IVI_MAX_MESSAGE_LEN + 1
		MAX_ERROR_DESCRIPTION    = (IVI_MAX_MESSAGE_BUF_SIZE * 2 + MAX_FUNCTION_NAME_SIZE + 75)

		errorSource = create_string_buffer(MAX_FUNCTION_NAME_SIZE)
		errorDescription = create_string_buffer(MAX_ERROR_DESCRIPTION )
		self.CALL("errorHandler",self,
				ViInt32(errorCode),
				errorSource,
				errorDescription)
		return errorDescription.value
	
	def error_message (self,errorCode):
		IVI_MAX_MESSAGE_LEN      = 255

