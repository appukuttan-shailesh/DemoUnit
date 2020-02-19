import sciunit
from typing import Dict, List

#==============================================================================

class SomaReceivesStepCurrent(sciunit.Capability):
    """Enables injecting step current stimulus to soma"""

    def inject_soma_square_current(self, current):
        """Model should implement this method such as to inject the specified
        current stimulus into the soma of the neuron.

        Input current is specified in the form of a dict with keys:
            'delay'     : (value in ms),
            'duration'  : (value in ms),
            'amplitude' : (value in nA)

        Example of current stimulus:

        .. code-block:: python

            current = {'delay'    : 10.0,
                       'duration' : 50.0,
                       'amplitude': 1.0  }
        """
        raise NotImplementedError()

class SomaProducesMembranePotential(sciunit.Capability):
    """Enables recording membrane potential from soma """

    def get_soma_membrane_potential(self, tstop: float):
        """Run simulation for time 'tstop', specified in ms, while recording the somatic membrane potential.
        Must return a list of the form:

        |    [ list1, list2 ] where,
        |        list1 = time series (in ms)
        |        list2 = membrane potential series (in mV)
        """
        raise NotImplementedError()

    def get_soma_membrane_potential_eFEL_format(self, tstop: float, start: float, stop: float) -> Dict[str, List[float]]:
        """Calls :meth:`get_soma_membrane_potential` and reformats
        its output structure into format accepted by eFEL library.


        Example of output format:

        .. code-block:: python

            efel_trace = {'T' : [time series in ms],
                          'V' : [somatic potential series in mv],
                          'stim_start' : [stimulus start time in ms],
                          'stim_end'   : [stimulus end time in ms]   }
        """
        traces = self.get_soma_membrane_potential(tstop)
        efel_trace = {'T' : traces[0],
                      'V' : traces[1],
                      'stim_start' : [start],
                      'stim_end'   : [stop]}
        return efel_trace
