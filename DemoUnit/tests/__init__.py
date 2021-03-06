import efel
import numpy
import sciunit
import DemoUnit.capabilities as cap
from typing import Dict, Optional

#===============================================================================

class RestingPotential(sciunit.Test):
    """Test the cell's resting membrane potential"""

    score_type: sciunit.scores = sciunit.scores.ZScore
    """specifies the type of score returned by the test"""

    description: str = ("Test the cell's resting membrane potential")
    """brief description of the test objective"""

    def __init__(self,
                 observation: Dict[str, float] = {'mean': None, 'std': None},
                 name: str = "Resting Membrane Potential Test") -> None:
        self.required_capabilities += (cap.SomaProducesMembranePotential,)
        sciunit.Test.__init__(self, observation, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation: Dict[str, float]) -> None:
        try:
            assert len(observation.keys()) == 2
            for key, val in observation.items():
                assert key in ["mean", "std"]
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'mean': NUM1, 'std': NUM2}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model: sciunit.Model, verbose: bool = False) -> float:
        trace = model.get_soma_membrane_potential(tstop=50.0)
        prediction = numpy.median(trace[1])
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation: Dict[str, float], prediction: float, verbose: bool = False) -> sciunit.scores.ZScore:
        # print ("observation = {}".format(observation))
        # print ("prediction = {}".format(prediction))
        score = sciunit.scores.ZScore.compute(observation, prediction)
        return score


#===============================================================================

class InputResistance(sciunit.Test):
    """Test the cell's input resistance"""

    score_type: sciunit.scores = sciunit.scores.ZScore
    """specifies the type of score returned by the test"""

    description = ("Test the cell's input resistance")
    """brief description of the test objective"""

    def __init__(self,
                 observation: Dict[str, float] = {'mean': None, 'std': None},
                 name: str = "Input Resistance Test") -> None:
        self.required_capabilities += (cap.SomaReceivesStepCurrent, cap.SomaProducesMembranePotential)
        sciunit.Test.__init__(self, observation, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation: Dict[str, float]) -> None:
        try:
            assert len(observation.keys()) == 2
            for key, val in observation.items():
                assert key in ["mean", "std"]
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'mean': NUM1, 'std': NUM2}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model: sciunit.Model, verbose: bool = False) -> float:
        efel.reset()
        stim_start = 10.0   # ms
        stim_dur   = 50.0   # ms
        stim_amp   = -1.0   # nA
        efel.setDoubleSetting('stimulus_current', stim_amp)
        model.inject_soma_square_current(current={'delay':stim_start,
                                                  'duration':stim_dur,
                                                  'amplitude':stim_amp})
        trace = model.get_soma_membrane_potential_eFEL_format(tstop=stim_start+stim_dur+stim_start,
                                                             start=stim_start,
                                                             stop =stim_start+stim_dur)
        prediction = efel.getFeatureValues([trace], ['ohmic_input_resistance_vb_ssse'])[0]["ohmic_input_resistance_vb_ssse"][0]
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation: Dict[str, float], prediction: float, verbose: bool = False) -> sciunit.scores.ZScore:
        # print ("observation = {}".format(observation))
        # print ("prediction = {}".format(prediction))
        score = sciunit.scores.ZScore.compute(observation, prediction)
        return score

#===============================================================================

class AP_Height(sciunit.Test):
    """Test the cell's AP height"""

    score_type: sciunit.scores = sciunit.scores.ZScore
    """specifies the type of score returned by the test"""

    description = ("Test the cell's AP height")
    """brief description of the test objective"""

    def __init__(self,
                 observation: Dict[str, float] = {'mean': None, 'std': None},
                 name: str = "Action Potential Height Test") -> None:
        self.required_capabilities += (cap.SomaReceivesStepCurrent, cap.SomaProducesMembranePotential)
        sciunit.Test.__init__(self, observation, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation: Dict[str, float]) -> None:
        try:
            assert len(observation.keys()) == 2
            for key, val in observation.items():
                assert key in ["mean", "std"]
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'mean': NUM1, 'std': NUM2}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model: sciunit.Model, verbose: bool = False) -> Optional[float]:
        efel.reset()
        stim_start = 10.0   # ms
        stim_dur   = 5.0    # ms
        stim_amp   = 15.0   # nA
        efel.setDoubleSetting('stimulus_current', stim_amp)
        model.inject_soma_square_current(current={'delay':stim_start,
                                                  'duration':stim_dur,
                                                  'amplitude':stim_amp})
        trace = model.get_soma_membrane_potential_eFEL_format(tstop=stim_start+stim_dur+stim_start,
                                                             start=stim_start,
                                                             stop =stim_start+stim_dur)
        output = efel.getFeatureValues([trace], ['AP_amplitude'])[0]["AP_amplitude"]
        prediction = output[0] if output else None
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation: Dict[str, float], prediction: Optional[float], verbose: bool = False) -> sciunit.scores.ZScore:
        if isinstance(prediction, type(None)):
            # score = sciunit.scores.InsufficientDataScore(None)
            score = sciunit.scores.ZScore(9999.99)
            # see: https://github.com/HumanBrainProject/hbp-validation-framework/issues/253
        else:
            score = sciunit.scores.ZScore.compute(observation, prediction)
        return score

#===============================================================================

class AP_HalfWidth(sciunit.Test):
    """Test the cell's AP half-width"""

    score_type: sciunit.scores = sciunit.scores.ZScore
    """specifies the type of score returned by the test"""

    description = ("Test the cell's AP half-width")
    """brief description of the test objective"""

    def __init__(self,
                 observation: Dict[str, float] = {'mean': None, 'std': None},
                 name: str = "Action Potential Half-Width Test") -> None:
        self.required_capabilities += (cap.SomaReceivesStepCurrent, cap.SomaProducesMembranePotential)
        sciunit.Test.__init__(self, observation, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation: Dict[str, float]) -> None:
        try:
            assert len(observation.keys()) == 2
            for key, val in observation.items():
                assert key in ["mean", "std"]
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'mean': NUM1, 'std': NUM2}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model: sciunit.Model, verbose: bool = False) -> Optional[float]:
        efel.reset()
        stim_start = 10.0   # ms
        stim_dur   = 5.0    # ms
        stim_amp   = 15.0   # nA
        efel.setDoubleSetting('stimulus_current', stim_amp)
        model.inject_soma_square_current(current={'delay':stim_start,
                                                  'duration':stim_dur,
                                                  'amplitude':stim_amp})
        trace = model.get_soma_membrane_potential_eFEL_format(tstop=stim_start+stim_dur+stim_start,
                                                             start=stim_start,
                                                             stop =stim_start+stim_dur)
        output = efel.getFeatureValues([trace], ['AP_duration_half_width'])[0]["AP_duration_half_width"]
        prediction = output[0] if output else None
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation: Dict[str, float], prediction: Optional[float], verbose: bool = False) -> sciunit.scores.ZScore:
        if isinstance(prediction, type(None)):
            # score = sciunit.scores.InsufficientDataScore(None)
            score = sciunit.scores.ZScore(9999.99)
            # see: https://github.com/HumanBrainProject/hbp-validation-framework/issues/253
        else:
            score = sciunit.scores.ZScore.compute(observation, prediction)
        return score