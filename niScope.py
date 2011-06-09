__all__ = []

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

	def ConfigureHorizontalTiming(self,
			sampleRate	= 20000000,
			numPts		= 1000,
			refPositioin	= 0.5,
			numRecords	= 1,
			enforceRealtime	= True):
		status = self.CALL('ConfigureHorizontalTiming',self,
				ViReal64(sampleRate),
				ViInt32(numPts),
				ViReal64(refPositioin),
				ViInt32(numRecords),
				ViBoolean(enforceRealtime))
		return 
		
		
	def ConfigureVertical(self,
		channelList="0",
		range=10,
		offset=0,
		coupling=COUPLING.DC,
		probeAttenuation=1,
		enabled=True):
		"""
		dfs
		"""
		status = self.CALL("ConfigureVertical",self,
			ViConstString(channelList),
			ViReal64(range),
			ViReal64(offset),
			ViInt32(coupling),
			ViReal64(probeAttenuation),
			ViBoolean(enabled))
		return status
	
	def ConfigureTrigger(self,trigger_type='Immediate',*settings):
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
		}[trigger_type](*settings)
		status = self.CALL("ConfigureTrigger"+trigger_type,self,*args)
		
	def InitiateAcquisition(self):
		status = self.CALL("InitiateAcquisition",self)
		
	def Abort(self):
		status = self.CALL("Abort",self)
		
	def AcquisitionStatus(self):
		status = self.CALL("AcquisitionStatus",self,
			byref(ViInt32(acq_status)))
		return acq_status.value
		
	def Commit(self):
		status = self.CALL("Commit",self)
	
	def Fetch(self	                   ,
		channelList  = "0"             ,
		data = zeros((1000,1),dtype=float64),
		timeout      = 1	      	   ,):
		
		data_type = {
			numpy.float64 	:''	        ,
			numpy.int8  	:'Binary8'  ,
			numpy.int16	:'Binary16' ,
			numpy.int32 	:'Binary32' }[data.dtype.type]

		numSamples = data.shape[0]
		numRec = data.shape[1]
		numWfms = self.ActualNumWfms(channelList)
		recLength = self.ActualRecordLength
		assert recLength == numSamples
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
		chan = ViConstString(channelList)
		numWfms = ViInt32()
		self.CALL("ActualNumWfms",self,chan,byref(numWfms))
		return numWfms.value
		

		
	def TranferDataTo(self,data,channel_list = "0",timeout=1):
		"""
		Parameters	
		
		channel_list	The channel you will acquire data from; it may 
				be a single channel, such as "0" or "1", or a
				list of channels such as "0,1".
		
		timeout 	The time to wait in seconds for data to be 
				acquired; using 0 for this parameter tells 
				NI-SCOPE to fetch whatever is currently 
				available.
		"""
		data_type = {
			'float64':''	    ,
			'int8'   :'Binary8' ,
			'int16'  :'Binary16',
			'int32'  :'Binary32' }[data.dtype.__str__()]	
		numSamples = max(data.shape)
		self.CALL("Fetch"+data_type,self,
			ViConstString(channel_list),
			ViReal64(timeout),
			ViInt32(numSamples),
			data.ctypes.data,#_as(ctypes.POINTER(ViReal64)),
			byref(self.info)
			)
			
	
	def read(self):
		self.ConfigureHorizontalTiming()
		self.ConfigureVertical()
		self.ConfigureTrigger()
		self.InitiateAcquisition()
		data = self.Fetch()
		self.close()
		return data
	
	def close(self):
		status = self.CALL("close",self)

# not implemented
#ViStatus _VI_FUNC niScope_FetchComplex ( ViSession vi,
#                                         ViConstString channelList,
#                                         ViReal64 timeout,
#                                         ViInt32 numSamples,
#                                         NIComplexNumber* wfm,
#                                         struct niScope_wfmInfo* wfmInfo);
#
#										 
# ViStatus _VI_FUNC niScope_FetchComplexBinary16 ( ViSession vi,
                                                 # ViConstString channelList,
                                                 # ViReal64 timeout,
                                                 # ViInt32 numSamples,
                                                 # NIComplexI16* wfm,
                                                 # struct niScope_wfmInfo* wfmInfo);

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
		IVI_MAX_MESSAGE_BUF_SIZE = IVI_MAX_MESSAGE_LEN + 1
		errorMessage = create_string_buffer(IVI_MAX_MESSAGE_BUF_SIZE)
