# -*- coding: utf-8 -*-
# author: Tiancheng Zhao

import logging
import copy


class Agent(object):
    """
    Abstract class for Agent (user or system)
    """

    def __init__(self, domain, complexity):
        self.domain = domain
        self.complexity = complexity

    def step(self, *args, **kwargs):
        """
        Given the new inputs, generate the next response
        
        :return: reward, terminal, response 
        """
        raise NotImplementedError("Implement step function is required")


class Action(dict):
    """
    A generic class that corresponds to a discourse unit. An action is made of an Act and a list of parameters.
    
    :ivar act: dialog act String
    :ivar parameters: [{slot -> usr_constrain}, {sys_slot -> value}] for INFORM, and [(type, value)...] for other acts. 
    
    """

    def __init__(self, act, parameters=None):
        self.act = act
        if parameters is None:
            self.parameters = []
        elif type(parameters) is not list:
            self.parameters = [parameters]
        else:
            self.parameters = parameters
        super(Action, self).__init__(act=self.act, parameters=self.parameters)

    def add_parameter(self, type, value):
        self.parameters.append((type, value))

    def dump_string(self):
        str_paras = []
        for p in self.parameters:
            if type(p) is not str:
                str_paras.append(str(p))
            else:
                str_paras.append(p)
        str_paras = "-".join(str_paras)
        return "%s:%s" % (self.act, str_paras)


class State(object):
    """
    The base class for a dialog state
    
    :ivar history: a list of turns
    :cvar USR: user name
    :cvar SYS: system name
    :cvar LISTEN: the agent is waiting for other's input
    :cvar SPEAK: the agent is generating it's output
    :cvar EXT: the agent leaves the session
    """

    USR = "usr"
    SYS = "sys"

    LISTEN = "listen"
    SPEAK = "speak"
    EXIT = "exit"

    def __init__(self):
        self.history = []

    def yield_floor(self, *args, **kwargs):
        """
        Base function that decides if the agent should yield the conversation floor
        """
        raise NotImplementedError("Yield is required")

    def is_terminal(self, *args, **kwargs):
        """
        Base function decides if the agent is left
        """
        raise NotImplementedError("is_terminal is required")

    def last_actions(self, target_speaker):
        """
        Search in the dialog hisotry given a speaker.
        
        :param target_speaker: the target speaker
        :return: the last turn produced by the given speaker. None if not found.
        """
        for spk, utt in self.history[::-1]:
            if spk == target_speaker:
                return utt
        return None

    def update_history(self, speaker, actions):
        """
        Append the new turn into the history
        
        :param speaker: SYS or USR
        :param actions: a list of Action
        """
        # make a deep copy of actions
        self.history.append((speaker, copy.deepcopy(actions)))


class SystemAct(object):
    """
    :cvar IMPLICIT_CONFIRM: you said XX
    :cvar EXPLICIT_CONFIRM: do you mean XX
    :cvar INFORM: I think XX is a good fit
    :cvar REQUEST: which location?
    :cvar GREET: hello
    :cvar GOODBYE: goodbye
    :cvar CLARIFY: I think you want either A or B. Which one is right?
    :cvar ASK_REPHRASE: can you please say it in another way?
    :cvar ASK_REPEAT: what did you say?
    """

    IMPLICIT_CONFIRM = "implicit_confirm"
    EXPLICIT_CONFIRM = "explicit_confirm"
    INFORM = "inform"
    REQUEST = "request"
    GREET = "greet"
    GOODBYE = "goodbye"
    CLARIFY = "clarify"
    ASK_REPHRASE = "ask_rephrase"
    ASK_REPEAT = "ask_repeat"
    QUERY = "query"


class UserAct(object):
    """
    :cvar CONFIRM: yes
    :cvar DISCONFIRM: no
    :cvar YN_QUESTION: Is it going to rain?
    :cvar INFORM: I like Chinese food.
    :cvar REQUEST: find me a place to eat.
    :cvar GREET: hello
    :cvar NEW_SEARCH: I have a new request.
    :cvar GOODBYE: goodbye
    :cvar CHAT: how is your day
    """
    GREET = "greet"
    INFORM = "inform"
    REQUEST = "request"
    YN_QUESTION = "yn_question"
    CONFIRM = "confirm"
    DISCONFIRM = "disconfirm"
    GOODBYE = "goodbye"
    NEW_SEARCH = "new_search"
    CHAT = "chat"
    SATISFY = "satisfy"
    MORE_REQUEST = "more_request"
    KB_RETURN = "kb_return"


class BaseSysSlot(object):
    """
    :cvar DEFAULT: the db entry
    :cvar PURPOSE: what's the purpose of the system
    """

    PURPOSE = "#purpose"
    DEFAULT = "#default"


class BaseUsrSlot(object):
    """
    :cvar NEED: what user want
    :cvar HAPPY: if user is satisfied about system's results
    :cvar AGAIN: the user rephrase the same sentence.
    :cvar SELF_CORRECT: the user correct itself.
    """
    NEED = "#need"
    HAPPY = "#happy"
    AGAIN = "#again"
    SELF_CORRECT = "#self_correct"
