# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
from simdial.agent.core import Agent, Action, UserAct, SystemAct, BaseSysSlot, BaseUsrSlot, State
import logging
import numpy as np
import copy
from collections import OrderedDict


class User(Agent):
    """
    Basic user agent
    
    :ivar usr_constrains: a combination of user slots
    :ivar domain: the given domain
    :ivar state: the dialog state
    """

    logger = logging.getLogger(__name__)

    class DialogState(State):
        """
        The dialog state object for this user simulator
        
        :ivar history: a list of tuple [(speaker, actions) ... ]
        :ivar spk_state: LISTEN, SPEAK or EXIT
        :ivar goals_met: if the system propose anything that's in user's goal
        :ivar: input_buffer: a list of system action that is not being handled in this turn
        """
        def __init__(self, sys_goals):
            super(State, self).__init__()
            self.history = []
            self.spk_state = self.LISTEN
            self.input_buffer = []
            self.goals_met = OrderedDict([(g, False) for g in sys_goals])

        def update_history(self, speaker, actions):
            """
            :param speaker: SYS or USR
            :param actions: a list of Action
            """
            self.history.append((speaker, actions))

        def is_terminal(self):
            """
            :return: the user wants to terminate the session 
            """
            return self.spk_state == self.EXIT

        def yield_floor(self):
            """
            :return: True if user want to stop speaking 
            """
            return self.spk_state == self.LISTEN

        def unmet_goal(self):
            for k, v in self.goals_met.items():
                if v is False:
                    return k
            return None

        def update_goals_met(self, top_action):
            proposed_sys = top_action.parameters[1]
            completed_goals = []
            for goal in proposed_sys.keys():
                if goal in self.goals_met.keys():
                    self.goals_met[goal] = True
                    completed_goals.append(goal)
            return completed_goals

        def reset_goal(self, sys_goals):
            self.goals_met = {g: False for g in sys_goals}

    def __init__(self, domain, complexity):
        super(User, self).__init__(domain, complexity)
        self.goal_cnt = np.random.choice(complexity.multi_goals.keys(), p=complexity.multi_goals.values())
        self.goal_ptr = 0
        self.usr_constrains, self.sys_goals = self._sample_goal()
        self.state = self.DialogState(self.sys_goals)

    def state_update(self, sys_actions):
        """
        Update the dialog state given system's action in a new turn
        
        :param sys_actions: a list of system action
        """
        self.state.update_history(self.state.SYS, sys_actions)
        self.state.spk_state = self.DialogState.SPEAK
        self.state.input_buffer = copy.deepcopy(sys_actions)

    def _sample_goal(self):
        """
        :return: {slot_name -> value} for user constrains, [slot_name, ..] for system goals
        """
        temp_constrains = self.domain.db.sample_unique_row().tolist()
        temp_constrains = [None if np.random.rand() < self.complexity.dont_care
                           else c for c in temp_constrains]
        # there is a chance user does not care
        usr_constrains = {s.name: temp_constrains[i] for i, s in enumerate(self.domain.usr_slots)}

        # sample the number of attribute about the system
        num_interest = np.random.randint(0, len(self.domain.sys_slots)-1)
        goal_candidates = [s.name for s in self.domain.sys_slots if s.name != BaseSysSlot.DEFAULT]
        selected_goals = np.random.choice(goal_candidates, size=num_interest, replace=False)
        np.random.shuffle(selected_goals)
        sys_goals = [BaseSysSlot.DEFAULT] + selected_goals.tolist()
        return usr_constrains, sys_goals

    def _constrain_equal(self, top_action):
        proposed_constrains = top_action.parameters[0]
        for k, v in self.usr_constrains.items():
            if k in proposed_constrains:
                if v != proposed_constrains[k]:
                    return False, k
            else:
                return False, k
        return True, None

    def _increment_goal(self):
        if self.goal_ptr >= self.goal_cnt-1:
            return None
        else:
            self.goal_ptr += 1
            _, self.sys_goals = self._sample_goal()
            change_key = np.random.choice(self.usr_constrains.keys())
            change_slot = self.domain.get_usr_slot(change_key)
            old_value = self.usr_constrains[change_key]
            old_value = -1 if old_value is None else old_value
            new_value = np.random.randint(0, change_slot.dim-1) % change_slot.dim
            self.logger.info("Filp user constrain %s from %d to %d" %
                             (change_key, old_value, new_value))
            self.usr_constrains[change_key] = new_value
            self.state.reset_goal(self.sys_goals)
            return change_key

    def policy(self):
        if self.state.spk_state == self.DialogState.EXIT:
            return None

        if len(self.state.input_buffer) == 0:
            self.state.spk_state = self.DialogState.LISTEN
            return None

        if len(self.state.history) > 100:
            self.state.input_buffer = []
            return Action(UserAct.GOODBYE)

        top_action = self.state.input_buffer[0]
        self.state.input_buffer.pop(0)

        if top_action.act == SystemAct.GREET:
            return Action(UserAct.GREET)

        elif top_action.act == SystemAct.GOODBYE:
            return Action(UserAct.GOODBYE)

        elif top_action.act == SystemAct.IMPLICIT_CONFIRM:
            if len(top_action.parameters) == 0:
                raise ValueError("IMPLICIT_CONFIRM is required to have parameter")
            slot_type, slot_val = top_action.parameters[0]
            if self.domain.is_usr_slot(slot_type):
                # if the confirm is right or usr does not care about this slot
                if slot_val == self.usr_constrains[slot_type] or self.usr_constrains[slot_type] is None:
                    return None
                else:
                    strategy = np.random.choice(self.complexity.reject_style.keys(),
                                                p=self.complexity.reject_style.values())
                    if strategy == "reject":
                        return Action(UserAct.DISCONFIRM, (slot_type, slot_val))
                    elif strategy == "reject+inform":
                        return [Action(UserAct.DISCONFIRM, (slot_type, slot_val)),
                                Action(UserAct.INFORM, (slot_type, self.usr_constrains[slot_type]))]
                    else:
                        raise ValueError("Unknown reject strategy")
            else:
                raise ValueError("Usr cannot handle imp_confirm to non-usr slots")

        elif top_action.act == SystemAct.EXPLICIT_CONFIRM:
            if len(top_action.parameters) == 0:
                raise ValueError("EXPLICIT_CONFIRM is required to have parameter")
            slot_type, slot_val = top_action.parameters[0]
            if self.domain.is_usr_slot(slot_type):
                # if the confirm is right or usr does not care about this slot
                if slot_val == self.usr_constrains[slot_type]:
                    return Action(UserAct.CONFIRM, (slot_type, slot_val))
                else:
                    return Action(UserAct.DISCONFIRM, (slot_type, slot_val))
            else:
                raise ValueError("Usr cannot handle imp_confirm to non-usr slots")

        elif top_action.act == SystemAct.INFORM:
            if len(top_action.parameters) != 2:
                raise ValueError("INFORM needs to contain the constrains and goal (2 parameters)")

            # check if the constrains are the same
            valid_constrain, wrong_slot = self._constrain_equal(top_action)
            if valid_constrain:
                # update the state for goal met
                complete_goals = self.state.update_goals_met(top_action)
                next_goal = self.state.unmet_goal()

                if next_goal is None:
                    slot_key = self._increment_goal()
                    if slot_key is not None:
                        return [Action(UserAct.NEW_SEARCH, (BaseSysSlot.DEFAULT, None)),
                                Action(UserAct.INFORM, (slot_key, self.usr_constrains[slot_key]))]
                    else:
                        return [Action(UserAct.SATISFY, [(g, None) for g in complete_goals]),
                                Action(UserAct.GOODBYE)]
                else:
                    ack_act = Action(UserAct.MORE_REQUEST, [(g, None) for g in complete_goals])
                    if np.random.rand() < self.complexity.yn_question:
                        # find a system slot with yn_templates
                        slot = self.domain.get_sys_slot(next_goal)
                        expected_val = np.random.randint(0, slot.dim)
                        if len(slot.yn_questions.get(slot.vocabulary[expected_val], [])) > 0:
                            # sample a expected value
                            return [ack_act, Action(UserAct.YN_QUESTION, (slot.name, expected_val))]

                    return [ack_act, Action(UserAct.REQUEST, (next_goal, None))]
            else:
                # find the wrong concept
                return Action(UserAct.INFORM, (wrong_slot, self.usr_constrains[wrong_slot]))

        elif top_action.act == SystemAct.REQUEST:
            if len(top_action.parameters) == 0:
                raise ValueError("Request is required to have parameter")

            slot_type, slot_val = top_action.parameters[0]

            if slot_type == BaseUsrSlot.NEED:
                next_goal = self.state.unmet_goal()
                return Action(UserAct.REQUEST, (next_goal, None))

            elif slot_type == BaseUsrSlot.HAPPY:
                return None

            elif self.domain.is_usr_slot(slot_type):
                if len(self.domain.usr_slots) > 1:
                    num_informs = np.random.choice(self.complexity.multi_slots.keys(),
                                                   p=self.complexity.multi_slots.values(),
                                                   replace=False)
                    if num_informs > 1:
                        candidates = [k for k, v in self.usr_constrains.items() if k != slot_type and v is not None]
                        num_extra = min(num_informs-1, len(candidates))
                        if num_extra > 0:
                            extra_keys = np.random.choice(candidates, size=num_extra, replace=False)
                            actions = [Action(UserAct.INFORM, (key, self.usr_constrains[key])) for key in extra_keys]
                            actions.insert(0, Action(UserAct.INFORM, (slot_type, self.usr_constrains[slot_type])))
                            return actions

                return Action(UserAct.INFORM, (slot_type, self.usr_constrains[slot_type]))

            else:
                raise ValueError("Usr cannot handle request to this type of parameters")

        elif top_action.act == SystemAct.CLARIFY:
            raise ValueError("Cannot handle clarify now")

        elif top_action.act == SystemAct.ASK_REPEAT:
            last_usr_actions = self.state.last_actions(self.state.USR)
            if last_usr_actions is None:
                raise ValueError("Unexpected ask repeat")
            return last_usr_actions

        elif top_action.act == SystemAct.ASK_REPHRASE:
            last_usr_actions = self.state.last_actions(self.state.USR)
            if last_usr_actions is None:
                raise ValueError("Unexpected ask rephrase")
            for a in last_usr_actions:
                a.add_parameter(BaseUsrSlot.AGAIN, True)
            return last_usr_actions

        elif top_action.act == SystemAct.QUERY:
            query, goals = top_action.parameters[0], top_action.parameters[1]
            valid_entries = self.domain.db.select([v for name, v in query])
            chosen_entry = valid_entries[np.random.randint(0, len(valid_entries)), :]

            results = {}
            if chosen_entry.shape[0] > 0:
                for goal in goals:
                    _, slot_id = self.domain.get_sys_slot(goal, return_idx=True)
                    results[goal] = chosen_entry[slot_id]
            else:
                print(chosen_entry)
                raise ValueError("No valid entries")

            return Action(UserAct.KB_RETURN, [query, results])
        else:
            raise ValueError("Unknown system act %s" % top_action.act)

    def step(self, inputs):
        """
        Given a list of inputs from the system, generate a response
        
        :param inputs: a list of Action
        :return: reward, terminal, [Action]
        """
        turn_actions = []
        # update the dialog state
        self.state_update(inputs)
        while True:
            action = self.policy()
            if action is not None:
                if type(action) is list:
                    turn_actions.extend(action)
                else:
                    turn_actions.append(action)

            if self.state.is_terminal():
                reward = 1.0 if self.state.unmet_goal() is None else -1.0
                self.state.update_history(self.state.USR, turn_actions)
                return reward, True, turn_actions

            if self.state.yield_floor():
                self.state.update_history(self.state.USR, turn_actions)
                return 0.0, False, turn_actions
