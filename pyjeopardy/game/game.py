from copy import deepcopy
from importlib import import_module

from pyjeopardy import config

from .hardware import Keyboard
from .log import Log

class Game:
    def __init__(self):
        self.rounds = []
        self.players = []
        self.hardware = []
        self.log = None

        # add keyboard as hardware
        self.keyboard = Keyboard()
        self.hardware.append(self.keyboard)

        # add hardware given in config
        for mod_name,class_name in config.HARDWARE:
            mod = import_module(mod_name)
            hw = getattr(mod, class_name)

            self.hardware.append(hw())

    def reset_log_and_points(self, cur_round):
        self.log = Log(cur_round)

        for p in self.players:
            p.reset_points()

    def add_round(self, round):
        self.rounds.append(round)

    def add_player(self, player):
        self.players.append(player)

    def delete_player(self, player):
        self.players.remove(player)

    @property
    def free_colors(self):
        used_colors = []
        for player in self.players:
            used_colors.append(player.color)

        free_colors = []
        for color in config.COLORS:
            if color not in used_colors:
                free_colors.append(color)

        return free_colors

    def is_active_hardware(self):
        for hw in self.hardware:
            if hw.active:
                return True
        return False

    def used_keys_for_hardware(self, hardware):
        if hardware not in self.hardware:
            return None

        keys = []
        for player in self.players:
            if player.hardware == hardware:
                keys.append(player.key)

        return keys

    def connect_hardware(self):
        for hw in self.hardware:
            if hw.active:
                hw.connect()

    def disconnect_hardware(self):
        for hw in self.hardware:
            if hw.active:
                hw.disconnect()

    def start_hardware(self, callback):
        for hw in self.hardware:
            if hw.active:
                hw.start(callback)

    def stop_hardware(self):
        for hw in self.hardware:
            if hw.active:
                hw.stop()
