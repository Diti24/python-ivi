"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2016-2018 Dietrich Pescoller

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

from .. import ivi
from .. import scope
from .. import scpi
from .. import extra

AcquisitionTypeMapping = {
        'normal': 'norm',
        'peak_detect': 'peak',
        'high_resolution': 'hres',
        'average': 'aver'}
VerticalCoupling = set(['ac', 'dc'])
TriggerTypeMapping = {
        'edge': 'edge',
        'width': 'glit',
        'glitch': 'glit',
        'tv': 'tv',
        #'immediate': '',
        'ac_line': 'edge',
        'pattern': 'patt',
        'can': 'can',
        'duration': 'dur',
        'i2s': 'i2s',
        'iic': 'iic',
        'eburst': 'ebur',
        'lin': 'lin',
        'm1553': 'm1553',
        'sequence': 'seq',
        'spi': 'spi',
        'uart': 'uart',
        'usb': 'usb',
        'flexray': 'flex'}
TriggerCouplingMapping = {
        'ac': ('ac', 0, 0),
        'dc': ('dc', 0, 0),
        'hf_reject': ('dc', 0, 1),
        'lf_reject': ('lfr', 0, 0),
        'noise_reject': ('dc', 1, 0),
        'hf_reject_ac': ('ac', 0, 1),
        'noise_reject_ac': ('ac', 1, 0),
        'hf_noise_reject': ('dc', 1, 1),
        'hf_noise_reject_ac': ('ac', 1, 1),
        'lf_noise_reject': ('lfr', 1, 0)}
TVTriggerEventMapping = {'field1': 'fie1',
        'field2': 'fie2',
        'any_field': 'afi',
        'any_line': 'alin',
        'line_number': 'lfi1',
        'vertical': 'vert',
        'line_field1': 'lfi1',
        'line_field2': 'lfi2',
        'line': 'line',
        'line_alternate': 'lalt',
        'lvertical': 'lver'}
TVTriggerFormatMapping = {'generic': 'gen',
        'ntsc': 'ntsc',
        'pal': 'pal',
        'palm': 'palm',
        'secam': 'sec',
        'p480l60hz': 'p480',
        'p480': 'p480',
        'p720l60hz': 'p720',
        'p720': 'p720',
        'p1080l24hz': 'p1080',
        'p1080': 'p1080',
        'p1080l25hz': 'p1080l25hz',
        'p1080l50hz': 'p1080l50hz',
        'p1080l60hz': 'p1080l60hz',
        'i1080l50hz': 'i1080l50hz',
        'i1080': 'i1080l50hz',
        'i1080l60hz': 'i1080l60hz'}
PolarityMapping = {'positive': 'pos',
        'negative': 'neg'}
GlitchConditionMapping = {'less_than': 'less',
        'greater_than': 'gre'}
WidthConditionMapping = {'within': 'rang'}
SampleModeMapping = {'real_time': 'rtim',
        'equivalent_time': 'etim',
        'segmented': 'segm'}
SlopeMapping = {
        'positive': 'pos',
        'negative': 'neg',
        'either': 'eith',
        'alternating': 'alt'}
MeasurementFunctionMapping = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'voltage_rms': 'vrms display',
        'voltage_peak_to_peak': 'vpp',
        'voltage_max': 'vmax',
        'voltage_min': 'vmin',
        'voltage_high': 'vtop',
        'voltage_low': 'vbase',
        'voltage_average': 'vaverage display',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle',
        'amplitude': 'vamplitude',
        'voltage_cycle_rms': 'vrms cycle',
        'voltage_cycle_average': 'vaverage cycle',
        'overshoot': 'overshoot',
        'preshoot': 'preshoot',
        'ratio': 'vratio',
        'phase': 'phase',
        'delay': 'delay'}
MeasurementFunctionMappingDigital = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle'}
ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmp8bit',
        'png': 'png',
        'png24': 'png'}
TimebaseModeMapping = {
        'main': 'main',
        'window': 'wind',
        'xy': 'xy',
        'roll': 'roll'}
TimebaseReferenceMapping = {
        'left': 'left',
        'center': 'cent',
        'right': 'righ'}
TriggerModifierMapping = {'none': 'normal', 'auto': 'auto'}


class hmo1002(scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
                       scpi.common.SelfTest, scpi.common.Memory,
                       scope.Base, scope.TVTrigger,
                       scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger,
                       scope.WaveformMeasurement, scope.MinMaxWaveform,
                       scope.ContinuousAcquisition, scope.AverageAcquisition,
                       scope.SampleMode, scope.TriggerModifier, scope.AutoSetup,
                       extra.common.SystemSetup, extra.common.Screenshot,
                       ivi.Driver):
    "HMO 1002 Series generic IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 2
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_scale = list()
        self._channel_trigger_level = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_bw_limit = list()

        super(hmo1002, self).__init__(*args, **kwargs)

        self._self_test_delay = 40
        self._memory_size = 10

        self._analog_channel_name = list()
        self._analog_channel_count = 2
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9

        self._horizontal_divisions = 10
        self._vertical_divisions = 8

        self._acquisition_segmented_count = 2
        self._acquisition_segmented_index = 1
        self._timebase_mode = 'main'
        self._timebase_reference = 'center'
        self._timebase_position = 0.0
        self._timebase_range = 1e-3
        self._timebase_scale = 100e-6
        self._timebase_window_position = 0.0
        self._timebase_window_range = 5e-6
        self._timebase_window_scale = 500e-9
        self._display_screenshot_image_format_mapping = ScreenshotImageFormatMapping
        self._display_vectors = True
        self._display_labels = True

        self._identity_description = "HMO 1002 generic IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Rohde Schwarz Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['HMO1002']

        self._add_property('channels[].scale',
                        self._get_channel_scale,
                        self._set_channel_scale,
                        None,
                        ivi.Doc("""
                        Specifies the vertical scale, or units per division, of the channel.  Units
                        are volts.
                        """))
        self._add_property('timebase.position',
                        self._get_timebase_position,
                        self._set_timebase_position,
                        None,
                        ivi.Doc("""
                        Sets the time interval between the trigger event and the display reference
                        point on the screen. The display reference point is either left, right, or
                        center and is set with the timebase.reference property. The maximum
                        position value depends on the time/division settings.
                        """))
        self._add_property('timebase.range',
                        self._get_timebase_range,
                        self._set_timebase_range,
                        None,
                        ivi.Doc("""
                        Sets the full-scale horizontal time in seconds for the main window. The
                        range is 10 times the current time-per-division setting.
                        """))
        self._add_property('timebase.scale',
                        self._get_timebase_scale,
                        self._set_timebase_scale,
                        None,
                        ivi.Doc("""
                        Sets the horizontal scale or units per division for the main window.
                        """))
        self._add_method('passfail.clear',
                        self._passfail_clear,
                        ivi.Doc("""
                        Clears the pass fail counter
                        """))
        self._add_method('passfail.start',
                        self._passfail_start,
                        ivi.Doc("""
                        start the pass fail test
                        """))
        self._add_method('passfail.stop',
                        self._passfail_stop,
                        ivi.Doc("""
                        stops the pass fail test
                        """))
        self._add_property('passfail.total',
                        self._get_passfail_total,
                        None,
                        None,
                        ivi.Doc("""
                        Returns number of perfomed test
                        """))
        self._add_property('passfail.failed',
                        self._get_passfail_failed,
                        None,
                        None,
                        ivi.Doc("""
                        Returns number of failed test
                        """))
        self._add_property('passfail.passed',
                        self._get_passfail_passed,
                        None,
                        None,
                        ivi.Doc("""
                        Returns number of passed test
                        """))
        self._init_channels()

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        "Opens an I/O session to the instrument."

        self._channel_count = self._analog_channel_count + self._digital_channel_count

        super(hmo1002, self)._initialize(resource, id_query, reset, **keywargs)

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

    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _init_channels(self):
        try:
            super(hmo1002, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_scale = list()
        self._channel_trigger_level = list()
        self._channel_bw_limit = list()

        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("channel%d" % (i + 1))
            self._channel_label.append("%d" % (i + 1))
            self._analog_channel_name.append("channel%d" % (i + 1))
            self._channel_probe_skew.append(0)
            self._channel_scale.append(1.0)
            self._channel_trigger_level.append(0.0)
            self._channel_invert.append(False)
            self._channel_probe_id.append("NONE")
            self._channel_bw_limit.append(False)

        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("digital%d" % i)
                self._channel_label.append("D%d" % i)
                self._digital_channel_name.append("digital%d" % i)

            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1

        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)

    def _system_fetch_setup(self):
        if self._driver_operation_simulate:
            return b''

        self._write_raw(b'SYST:SET?')

        return self._read_ieee_block()

    def _system_load_setup(self, data):
        if self._driver_operation_simulate:
            return

        self._write_ieee_block(data, 'SYST:SET ')

        self.driver_operation.invalidate_all_attributes()

    def _get_timebase_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_position = float(self._ask("timebase:position?"))
            self._set_cache_valid()
        return self._timebase_position

    def _set_timebase_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:position %e" % value)
        self._timebase_position = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'timebase_window_position')

    def _get_timebase_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_range = float(self._ask("timebase:range?"))
            self._timebase_scale = self._timebase_range / self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_scale')
        return self._timebase_range

    def _set_timebase_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:range %e" % value)
        self._timebase_range = value
        self._timebase_scale = value / self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_scale')
        self._set_cache_valid(False, 'timebase_window_scale')
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_timebase_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask("timebase:scale?"))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_range')
        return self._timebase_scale

    def _set_timebase_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:scale %e" % value)
        self._timebase_scale = value
        self._timebase_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_range')
        self._set_cache_valid(False, 'timebase_window_scale')
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_range[index] = float(self._ask(":%s:range?" % self._channel_name[index]))
            self._channel_scale[index] = self._channel_range[index] / self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_scale", index)
        return self._channel_range[index]

    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:range %e" % (self._channel_name[index], value))
        self._channel_range[index] = value
        self._channel_scale[index] = value / self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_scale", index)
        self._set_cache_valid(False, "channel_offset", index)

    def _get_channel_scale(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_scale[index] = float(self._ask(":%s:scale?" % self._channel_name[index]))
            self._channel_range[index] = self._channel_scale[index] * self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_range", index)
        return self._channel_scale[index]

    def _set_channel_scale(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:scale %e" % (self._channel_name[index], value))
        self._channel_scale[index] = value
        self._channel_range[index] = value * self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_range", index)
        self._set_cache_valid(False, "channel_offset", index)

    def _get_measurement_status(self):
        return self._measurement_status

    def _measurement_auto_setup(self):
        if not self._driver_operation_simulate:
            self._write(":autoscale")

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write('*rst')

    def _passfail_clear(self):
        if not self._driver_operation_simulate:
            self._write('mask:res:coun')

    def _passfail_start(self):
        if not self._driver_operation_simulate:
            self._write('mask:test run')

    def _passfail_stop(self):
        if not self._driver_operation_simulate:
            self._write('mask:test stop')

    def _get_passfail_total(self):
        if not self._driver_operation_simulate:
            value = int(self._ask(":mask:coun?"))
            return value
        else:
            return 0

    def _get_passfail_failed(self):
        if not self._driver_operation_simulate:
            value = int(self._ask(":mask:vco?"))
            return value
        else:
            return 0

    def _get_passfail_passed(self):
        return self._get_passfail_total() - self._get_passfail_failed()
