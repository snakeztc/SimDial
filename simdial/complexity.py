# -*- coding: utf-8 -*-
# Author: Tiancheng Zhao
# Date: 9/13/17


class ComplexitySpec(object):
    """
    Base class of complexity specification
    
    :cvar environment: configs for environmental noise
    :cvar propostion: configs for propositional noise
    :cvar interaction: configs for interactional noise
    :cvar social: configs for social noise
    """
    environment = None
    proposition = None
    interaction = None
    social = None


class Complexity(object):
    """
    Complexity object used to decides the task difficulities
    
    :ivar asr_acc: the mean value of asr confidence
    :ivar asr_std: the std of asr confidence distribution
    :ivar yn_question: the chance the user will ask yn_question
    :ivar reject_stype: the distribution over different rejection style
    :ivar multi_slots: the distriibution over how many slots in a inform
    :ivar multi_goals: the distribution over how many goals in a dialog
    :ivar dont_care: the chance that user dont are about a slot
    :ivar hesitation: the chance that user will hesitate in an utterance
    :ivar self_restart: the chance that user will restart
    :ivar self_correct: the chance that user will correct itself in an utterance.
    :ivar self_discloure: the chance that system will do self discloure
    :ivar ref_shared: the chacne that system will do refernece 
    :ivar violation_sn: the chance that system will do VSN
    """

    def __init__(self, complexity_spec):
        # environment
        self.asr_acc = complexity_spec.environment['asr_acc']
        self.asr_std = complexity_spec.environment['asr_std']

        # propositional
        self.yn_question = complexity_spec.proposition['yn_question']
        self.reject_style = complexity_spec.proposition['reject_style']
        self.multi_slots = complexity_spec.proposition['multi_slots']
        self.multi_goals = complexity_spec.proposition['multi_goals']
        self.dont_care = complexity_spec.proposition['dont_care']

        # interactional
        self.hesitation = complexity_spec.interaction['hesitation']
        self.self_restart = complexity_spec.interaction['self_restart']
        self.self_correct = complexity_spec.interaction['self_correct']

        # social
        self.self_disclosure = complexity_spec.social['self_disclosure']
        self.ref_shared = complexity_spec.social['ref_shared']
        self.violation_sn = complexity_spec.social['violation_sn']

    def get_name(self):
        return self.__class__.__name__


class MixSpec(ComplexitySpec):
    """
    An example spec for the easy setting
    """

    environment = {'asr_acc': 0.7,
                   'asr_std': 0.15}

    proposition = {'yn_question': 0.4,
                   'reject_style': {'reject': 0.5, 'reject+inform': 0.5},
                   'multi_slots': {1: 0.7, 2: 0.3},
                   'dont_care': 0.1,
                   'multi_goals': {1: 0.6, 2: 0.4},
                   }

    interaction = {'hesitation': 0.4,
                   'self_restart': 0.1,
                   'self_correct': 0.2}

    social = {'self_disclosure': None,
              'ref_shared': None,
              'violation_sn': None}


class PropSpec(ComplexitySpec):
    """
    An example spec for the easy setting
    """

    environment = {'asr_acc': 1.0,
                   'asr_std': 0.0}

    proposition = {'yn_question': 0.4,
                   'reject_style': {'reject': 0.5, 'reject+inform': 0.5},
                   'multi_slots': {1: 0.7, 2: 0.3},
                   'dont_care': 0.1,
                   'multi_goals': {1: 0.7, 2: 0.3},
                   }

    interaction = {'hesitation': 0.0,
                   'self_restart': 0.0,
                   'self_correct': 0.0}

    social = {'self_disclosure': None,
              'ref_shared': None,
              'violation_sn': None}


class EnvSpec(ComplexitySpec):
    """
    An example spec for the easy setting
    """

    environment = {'asr_acc': 0.7,
                   'asr_std': 0.2}

    proposition = {'yn_question': 0.0,
                   'reject_style': {'reject': 1.0, 'reject+inform': 0.0},
                   'multi_slots': {1: 1.0, 2: 0.0},
                   'dont_care': 0.0,
                   'multi_goals': {1: 1.0, 2: 0.0},
                   }

    interaction = {'hesitation': 0.0,
                   'self_restart': 0.0,
                   'self_correct': 0.0}

    social = {'self_disclosure': None,
              'ref_shared': None,
              'violation_sn': None}


class InteractSpec(ComplexitySpec):
    """
    An example spec for the easy setting
    """

    environment = {'asr_acc': 1.0,
                   'asr_std': 0.0}

    proposition = {'yn_question': 0.0,
                   'reject_style': {'reject': 1.0, 'reject+inform': 0.0},
                   'multi_slots': {1: 1.0, 2: 0.0},
                   'dont_care': 0.0,
                   'multi_goals': {1: 1.0, 2: 0.0},
                   }

    interaction = {'hesitation': 0.4,
                   'self_restart': 0.1,
                   'self_correct': 0.2}

    social = {'self_disclosure': None,
              'ref_shared': None,
              'violation_sn': None}


class CleanSpec(ComplexitySpec):
    """
    An example spec for the easy setting
    """

    environment = {'asr_acc': 1.0,
                   'asr_std': 0.0}

    proposition = {'yn_question': 0.0,
                   'reject_style': {'reject': 1.0, 'reject+inform': 0.0},
                   'multi_slots': {1: 1.0, 2: 0.0},
                   'dont_care': 0.0,
                   'multi_goals': {1: 1.0, 2: 0.0},
                   }

    interaction = {'hesitation': 0.0,
                   'self_restart': 0.0,
                   'self_correct': 0.0}

    social = {'self_disclosure': None,
              'ref_shared': None,
              'violation_sn': None}