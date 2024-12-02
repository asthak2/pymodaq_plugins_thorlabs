import numpy as np
# from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
from pymodaq_plugins_thorlabs.hardware.ccsxxx import CCSXXX


# DK - we created this in hardware/ccsxxx.py
# class PythonWrapperOfYourInstrument:
#     #  TODO Replace this fake class with the import of the real python wrapper of your instrument
#     pass

# TODO:
# (1) change the name of the following class to DAQ_1DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_1Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_1D
class DAQ_1DViewer_CCSXXX(DAQ_Viewer_base):
    """ Instrument plugin class for a 1D viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    # DK - add integration_time parameter (done)
    params = comon_parameters+[
        {'title': 'Integration time', 'name': 'integration_time', 'type': 'float', 'value': 10.0e-3},
        {'title': 'Resource Name:', 'name': 'resource_name', 'type': 'str', 'value': b'USB0::0x1313::0x8087::M00934802::RAW'}      # {DK - add resource_name},

        ## TODO for your custom plugin
        # elements to be added here as dicts in order to control your custom stage
        ############
        ]
    # integration time

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: CCSXXX = None

        # TODO declare here attributes you want/need to init with a default value

        self.x_axis = None

    # DK - change settings
    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "integration_time":
           self.controller.set_integration_time(self.settings['integration_time'])
#        elif ...
        ##

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        # raise NotImplemented  # TODO when writing your own plugin remove this line and modify the one below
        self.ini_detector_init(slave_controller=controller)

        if self.is_master:

            self.controller = CCSXXX(self.settings['resource_name'])  #instantiate you driver with whatever arguments are needed
            self.controller.connect() # call eventual methods

        ## TODO for your custom plugin
        # get the x_axis (you may want to to this also in the commit settings if x_axis may have changed
        data_x_axis = self.controller.get_wavelength_data()  # if possible
        self.x_axis = Axis(data=data_x_axis, label='wavelength', units='nm', index=0)

        # TODO for your custom plugin. Initialize viewers pannel with the future type of data
        self.dte_signal_temp.emit(DataToExport(name='myplugin',
                                               data=[DataFromPlugins(name='Mock1',
                                                                     data=np.zeros((3648)),  # for example
                                                                     dim='Data1D', labels=['Spectrum'],
                                                                     axes=[self.x_axis])]))

        info = "Whatever info you want to log"
        initialized = True
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
         # when writing your own plugin remove this line
        self.controller.close()
        #  self.controller.your_method_to_terminate_the_communication()  # when writing your own plugin replace this line

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following

        ##synchrone version (blocking function)
        self.controller.start_scan()
        data_tot = self.controller.get_scan_data()
        self.dte_signal.emit(DataToExport('myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data1D', labels=['dat0', 'data1'],
                                                                axes=[self.x_axis])]))

        ##asynchrone version (non-blocking function with callback)
        # self.controller.start_scan(self.callback)



    # def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        # data_tot = self.controller.get_scan_data()
        # self.dte_signal.emit(DataToExport('myplugin',
        #                               data=[DataFromPlugins(name='Mock1', data=data_tot,
        #                                                        dim='Data1D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        self.controller.close()  # when writing your own plugin replace this line
        # self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        # ##############################
        return ''


if __name__ == '__main__':
    main(__file__)