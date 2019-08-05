"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2016 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import time
import struct
import numpy as np
import logging

from .. import ivi
from .. import dmm
from .. import scpi

logger = logging.getLogger(__name__)


MeasurementFunction = set(['dc_volts', 'ac_volts', 'dc_current', 'ac_current',
                'two_wire_resistance', 'four_wire_resistance',
                'ac_plus_dc_volts', 'ac_plus_dc_current', 'frequency',
                'period', 'temperature', 'sensor'])

MeasurementFunctionMapping = {
        'dc_volts': 'VOLTage:DC',
        'ac_volts': 'VOLTage:AC',
        'dc_current': 'CURRent:DC',
        'ac_current': 'CURRent:AC',
        'two_wire_resistance': 'RESistance',
        'four_wire_resistance': 'FRESistance',
        'frequency': 'FREQuency',
        'sensor': 'SENSor',
        'capacitance': 'CAPacitance',
        'continuity': 'CONTinuity',
        'diode': 'DIODe'}
        
MeasurementRangeMapping = {
        'dc_volts': 'SENSe:VOLTage:DC:RANGe',
        'ac_volts': 'SENSe:VOLTage:AC:RANGe',
        'dc_current': 'SENSe:CURRent:DC:RANGe',
        'ac_current': 'SENSe:CURRent:AC:RANGe',
        'two_wire_resistance': 'SENSe:RESistance:RANGe',
        'four_wire_resistance': 'SENSe:FRESistance:RANGe',
        'frequency': 'SENSe:FREQuency:VOLTage:RANGe',
        # 'period': 'per:range:lower',
        'capacitance': 'SENSe:CAPacitance:RANGe'}
        
MeasurementAutoRangeMapping = {
        'dc_volts': 'SENSe:VOLTage:DC:RANGe:AUTO',
        'ac_volts': 'SENSe:VOLTage:AC:RANGe:AUTO',
        'dc_current': 'SENSe:CURRent:DC:RANGe:AUTO',
        'ac_current': 'SENSe:CURRent:AC:RANGe:AUTO',
        'two_wire_resistance': 'SENSe:RESistance:RANGe:AUTO',
        'four_wire_resistance': 'SENSe:FRESistance:RANGe:AUTO',
        'capacitance': 'SENSe:CAPacitance:RANGe:AUTO'}
        
RangeVoltsAdmittedValues = [0.4, 4, 40, 400, 1000]

ADCRateAdmittedValues = ['SLOW', 'MED', 'FAST']

class hmc8012(scpi.dmm.Base):
    "R&S HMC8012 IVI DMM driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'HMC8012')
        
        super(hmc8012, self).__init__(*args, **kwargs)
        
        self._memory_size = 5
        
        self._identity_description = "R&S HMC8012 IVI DMM driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Rohde Schwarz Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['HMC8012']
        self._ADC_rate = 'FAST'
        
        self._add_method('memory.save',
                        self._memory_save)
        self._add_method('memory.recall',
                        self._memory_recall)
        self._add_method('memory.set_name',
                        self._set_memory_name)
        self._add_method('memory.get_name',
                        self._get_memory_name)
        self._add_property('ADC_rate',
                        self._get_ADC_rate,
                        self._set_ADC_rate)
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(hmc8012, self)._initialize(resource, id_query, reset, **keywargs)
        
        # interface clear
        if not self._driver_operation_simulate:
            self._clear()
        
        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)
        
        # reset
        if reset:
            self.utility.reset()
        
    
    
    
    def _memory_save(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % index)
    
    def _memory_recall(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % index)
    
    def _get_memory_name(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            return self._ask("memory:state:name? %d" % index).strip(' "')
    
    def _set_memory_name(self, index, value):
        index = int(index)
        value = str(value)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("memory:state:name %d, \"%s\"" % (index, value))
            
    def _get_ADC_rate(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("SENSe:ADCRate?").strip('"')
            self._ADC_rate = value
            self._set_cache_valid()
        return self._ADC_rate
    
    def _set_ADC_rate(self, value):
        if value.upper() not in ADCRateAdmittedValues:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("SENSe:ADCRate %s" % value.upper())
        self._measurement_function = value
        self._set_cache_valid()
        
    
    def _set_measurement_function(self, value):
        if value not in MeasurementFunctionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("SENSe:FUNCtion %s" % MeasurementFunctionMapping[value])
        self._measurement_function = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'range')
        self._set_cache_valid(False, 'auto_range')
        self._set_cache_valid(False, 'resolution')
        
    # def _configure(self, function, range):
    #     self._set_measurement_function(function)
    #     if range in Auto:
    #         self._set_auto_range(range)
    #     else:
    #         self._set_range(range)
        
    def _set_range(self, value):
        
        value = float(value)
        # round up to even power of 10
        if value not in RangeVoltsAdmittedValues:
            if value > RangeVoltsAdmittedValues[-1]:
                value = RangeVoltsAdmittedValues[-1]
                logger.warning('Range value exceeds the maximum admitted: set to %.1fV' %(RangeVoltsAdmittedValues[-1]))
            else:
                i = np.argmax(np.array(RangeVoltsAdmittedValues)> value)
                value = RangeVoltsAdmittedValues[i]
                logger.warning('Range value not admitted: set to %.1fV' %(RangeVoltsAdmittedValues[i]))
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                self._write("%s %g" % (cmd, value))
        self._range = value
        self._set_cache_valid()
    


