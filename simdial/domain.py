# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
from simdial.database import Database
import numpy as np
from simdial.agent.core import BaseSysSlot
import logging


class DomainSpec(object):
    """
    Abstract specification template.
    
    :cvar usr_slots: [(slot_name, slot_description, dim) ...]
    :cvar sys_slots: [(slot_name, slot_description, dim) ...]
    :cvar nlg_spec: {slot_type -> {inform: [], request: [], yn_question: [(utt, target)]}}
    :cvar db_size: the size of database
    """
    nlg_spec = None
    usr_slots = None
    sys_slots = None
    db_size = None
    name = None
    greet = None

    def to_dict(self):
        return {'nlg_spec': self.nlg_spec,
                'usr_slots': self.usr_slots,
                'sys_slots': self.sys_slots,
                'db_size': self.db_size,
                'name': self.name,
                'greet': self.greet}


class Slot(object):
    """
    Class for sys/usr slot
    """
    def __init__(self, name, description, vocabulary):
        self.name = name
        self.description = description
        self.vocabulary = vocabulary
        self.dim = len(vocabulary)
        self.requests = []
        self.informs = []
        self.yn_questions = {}

    def sample_request(self):
        if self.requests:
            return np.random.choice(self.requests)
        else:
            raise ValueError("Sample from empty request_utt pool")

    def sample_inform(self):
        if self.informs:
            return np.random.choice(self.informs)
        else:
            raise ValueError("Sample from empty inform_utt pool")

    def sample_yn_question(self, expect_val):
        questions = self.yn_questions.get(expect_val, [])
        if questions:
            return np.random.choice(questions)
        else:
            raise ValueError("Sample from empty yn_questions pool")

    def sample_different(self, value):
        if value is None:
            return np.random.randint(0, self.dim)
        else:
            return np.random.choice([None] + [i for i in range(self.dim) if i != value])


class Domain(object):
    """
    A class that contains sufficient info about a slot-filling domain. Including:
    
    :ivar db: table with N items, each has I+R attributes
    :ivar sys_slots: a list of that the system can tell the users. Each slot is a dictionary 
    that contains slot_name, slot_description, dimension
    :ivar usr_slots: a list of slots that users can impose a constrains. Each slot is a dictionary 
    that contains slot_name, slot_description, dimension
    """

    logger = logging.getLogger(__name__)

    def __init__(self, domain_spec):
        """
        :param domain_spec: an implementation of DomainSpec
        """
        self.name = domain_spec.name
        self.greet = domain_spec.greet
        self.usr_slots = [Slot("#"+name, desc, vocab) for name, desc, vocab in domain_spec.usr_slots]
        self.sys_slots = [Slot("#"+name, desc, vocab) for name, desc, vocab in domain_spec.sys_slots]
        self.sys_slots.insert(0, Slot(BaseSysSlot.DEFAULT, "", [str(i) for i in range(domain_spec.db_size)]))

        for slot_name, slot_nlg in domain_spec.nlg_spec.items():
            slot_name = "#"+slot_name
            slot = self.get_usr_slot(slot_name) if self.is_usr_slot(slot_name) else self.get_sys_slot(slot_name)
            if slot:
                slot.informs.extend(slot_nlg['inform'])
                slot.requests.extend(slot_nlg['request'])
                slot.yn_questions = slot_nlg.get('yn_question', {})
            else:
                raise Exception("Fail to align %s nlg spec with the rest of domain" % slot_name)
        usr_slot_priors = [np.ones(s.dim) for s in self.usr_slots]  # we assume a uniform prior
        # we left out DEFAULT from prior since it'e KEY
        sys_slot_priors = [np.ones(s.dim) for s in self.sys_slots[1:]]

        self.db = Database(usr_slot_priors, sys_slot_priors, num_rows=domain_spec.db_size)
        self.db.pprint()

    def get_usr_slot(self, slot_name, return_idx=False):
        """
        :param slot_name: the target slot name
        :param return_idx: True/False to return slot index
        :return: slot, (index) or None if it's not user slot
        """
        for s_id, s in enumerate(self.usr_slots):
            if s.name == slot_name:
                if return_idx:
                    return s, s_id
                else:
                    return s
        return None

    def get_sys_slot(self, slot_name, return_idx=False):
        """
        :param slot_name: the target slot name
        :param return_idx: True/False to return slot index
        :return: slot, (index) or None if it's not system slot
        """
        for s_id, s in enumerate(self.sys_slots):
            if s.name == slot_name:
                if return_idx:
                    return s, s_id
                else:
                    return s
        return None

    def is_usr_slot(self, query_name):
        """
        :param query_name: a slot name
        :return: True if slot_name is user slot, False o/w
        """
        return query_name in [s.name for s in self.usr_slots]
