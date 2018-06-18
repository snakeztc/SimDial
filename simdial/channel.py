# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
import numpy as np
from simdial.agent.core import UserAct, BaseUsrSlot
import copy


class AbstractNoise(object):
    def __init__(self, domain, complexity):
        self.complexity = complexity
        self.domain = domain

    def transmit(self, actions):
        raise NotImplementedError

    def transmit_words(self, utt):
        pass


class EnvironmentNoise(AbstractNoise):
    def __init__(self, domain, complexity):
        super(EnvironmentNoise, self).__init__(domain, complexity)
        self.dim_map = {slot.name: slot.dim for slot in domain.usr_slots}

    def transmit(self, actions):
        conf = np.random.normal(self.complexity.asr_acc, self.complexity.asr_std)
        conf = np.clip(conf, 0.1, 0.99)
        noisy_actions = []
        # check has yes no
        has_confirm = False
        for a in actions:
            if a.act in [UserAct.DISCONFIRM, UserAct.CONFIRM]:
                has_confirm = True
                break
        if has_confirm:
            conf = np.clip(conf+0.1, 0.1, 0.99)

        for a in actions:
            if a.act == UserAct.CONFIRM:
                if np.random.rand() > conf:
                    a.act = UserAct.DISCONFIRM
            elif a.act == UserAct.DISCONFIRM:
                if np.random.rand() > conf:
                    a.act = UserAct.CONFIRM
            elif a.act == UserAct.INFORM:
                if np.random.rand() > conf:
                    slot, value = a.parameters[0]
                    choices = range(self.dim_map[slot]) + [None]
                    a.parameters[0] = (slot, np.random.choice(choices))

            noisy_actions.append(a)

        return noisy_actions, conf


class InteractionNoise(AbstractNoise):

    def transmit(self, actions):
        return self.add_self_correct(actions)

    def transmit_words(self, utt):
        # hesitation
        utt = self.add_hesitation(utt)

        # self-restart
        return self.add_self_restart(utt)

    def add_hesitation(self, utt):
        tokens = utt.split(" ")
        if len(tokens) > 4 and  np.random.rand() < self.complexity.hesitation:
            pos = np.random.randint(1, len(tokens)-1)
            tokens.insert(pos, np.random.choice(["hmm", "uhm", "hmm ...",]))
            return " ".join(tokens)
        return utt

    def add_self_restart(self, utt):
        tokens = utt.split(" ")
        if len(tokens) > 4 and np.random.rand() < self.complexity.self_restart:
            length = np.random.randint(1, 3)
            tokens = tokens[0:length] + ["uhm yeah"] + tokens
            return " ".join(tokens)
        return utt

    def add_self_correct(self, actions):
        for a in actions:
            if a.act == UserAct.INFORM and np.random.rand() < self.complexity.self_correct:
                a.parameters.append((BaseUsrSlot.SELF_CORRECT, True))
        return actions


class SocialNoise(AbstractNoise):
    def transmit(self, actions):
        return actions


# Channels at action-level and word-level

class ActionChannel(object):
    """
    A class to simulate the complex behviaor of human-computer conversation.
    """

    def __init__(self, domain, complexity):
        self.environment = EnvironmentNoise(domain, complexity)
        self.interaction = InteractionNoise(domain, complexity)
        self.social = SocialNoise(domain, complexity)

    def transmit2sys(self, actions):
        """
        Given a list of action from a user to a system, add noise to the actions.

        :param actions: a list of clean action from the user to the system
        :return: a list of corrupted actions.
        """
        action_copy = [copy.deepcopy(a) for a in actions]
        noisy_actions = self.interaction.transmit(action_copy)
        noisy_actions = self.social.transmit(noisy_actions)
        noisy_actions, conf = self.environment.transmit(noisy_actions)
        return noisy_actions, conf


class WordChannel(object):
    """
    A class to simulate the complex behviaor of human-computer conversation.
    """

    def __init__(self, domain, complexity):
        self.interaction = InteractionNoise(domain, complexity)

    def transmit2sys(self, utt):
        """
        Given a list of action from a user to a system, add noise to the actions.

        :param actions: a list of clean action from the user to the system
        :return: a list of corrupted actions.
        """
        return self.interaction.transmit_words(utt)