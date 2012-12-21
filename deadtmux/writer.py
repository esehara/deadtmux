# -*- coding: utf-8 -*-
from util import debug_print
debug = False


class PaneManager(object):

    panes = []

    def __init__(self, ars):

        for num, ar in enumerate(ars):
            ar['no'] = num
            self.panes.append(Pane(ar))


class Pane(object):

    sendkeys = None
    alias = None
    is_global = False

    def __init__(self, d):
        self.num = d['no']

        if 'send-keys' in d:
            self.sendkeys = d['send-keys']

        if 'alias' in d:
            self.alias = d['alias']

        self.split_window = d['split-window']

    def init_write(self):
        return_string = ""

        if self.split_window == "horizon":
            return_string += "tmux split-window -h"

        if self.split_window == "vertical":
            return_string += "tmux split-window -v"

        return return_string + "\n"

    def prosess_write(self):
        return_string = ""
        return_string += "tmux select-pane -t %d \n" % self.num

        if not self.alias is None:
            return_string += self._generate_alias()

        if not self.sendkeys is None:
            return_string += self._generate_sendkeys()

        return return_string

    def __sendkeys_string(self, string):
        return "tmux send-keys '%s' enter \n" % string

    def _generate_sendkeys(self):
        return_string = ""

        for sendkey in self.sendkeys:
            return_string += self.__sendkeys_string(sendkey)
            return_string += "\n"

        return return_string

    def _generate_alias(self):
        return_string = ""

        for key, value in self.alias.items():
            return_string += self.__sendkeys_string(
                '"alias %s=\'%s\'"' % (key, value))
            return_string += "\n"

        return return_string

if __name__ == "__main__":
    global debug
    debug = True
