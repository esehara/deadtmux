# -*- coding: utf-8 -*-
import yaml
import re
import os

debug = False


class PaneManager(object):

    panes = []
    global_pane = None
    configure = None

    def __init__(self, ars):
        no = 0
        for ar in ars:
            if ('is_global' in ar and
                    ar['is_global']):
                self.global_pane = Pane(ar)
                continue

            if ('configure' in ar):
                self.configure = ar['configure']
                continue

            ar['no'] = no
            self.panes.append(Pane(ar))
            no += 1

    def header_write(self):
        return_string = ""
        return_string += "%s & \n" % self.configure['run']
        return_string += "sleep 1"
        return return_string

    def footer_write(self):
        return_string = ""
        return_string += "tmux select-pane -t %d \n" % self.configure[
            'focus-pane']
        return_string += "tmux detach \n"
        return_string += "%s\n" % self.configure['run']
        return return_string

    def init_write(self):
        return_string = ""

        for pane in self.panes:
            return_string += pane.init_write()

        return return_string

    def process_write(self):
        return_string = ""

        for pane in self.panes:
            global_write = None

            if not self.global_pane is None:
                global_write = self.global_pane.process_write()

            return_string += pane.process_write(
                global_write)

        return return_string

    def output(self):
        return_string = ""
        return_string += self.header_write()
        return_string += self.init_write()
        return_string += self.process_write()
        return_string += self.footer_write()
        return return_string


class Pane(object):

    sendkeys = None
    alias = None
    export = None
    workspace = None
    resize = None
    is_global = False

    def __init__(self, d):

        if not ('is_global' in d and
                d['is_global']):
            self.num = d['no']
            if self.num != 0:
                self.split_window = d['split-window']
        else:
            self.is_global = True

        if 'send-keys' in d:
            self.sendkeys = d['send-keys']

        if 'alias' in d:
            self.alias = d['alias']

        if 'export' in d:
            self.export = d['export']

        if 'workspace' in d:
            self.workspace = self._workspace_parser(
                d['workspace'])

        if 'resize' in d:
            self.resize = d['resize']

        if 'tmux' in d:
            self.tmux = d['tmux']

    def _workspace_parser(self, d_workspace):
        abs_path = re.compile('^/')
        for key, value in d_workspace.items():
            if key == 'root':
                continue
            if not abs_path.match(d_workspace[key]):
                d_workspace[key] = os.path.join(
                    d_workspace['root'], d_workspace[key])
        return d_workspace

    def init_write(self):
        return_string = ""
        if self.num != 0:
            if self.split_window == "horizon":
                return_string += "tmux split-window -h"

            if self.split_window == "vertical":
                return_string += "tmux split-window -v"

        return return_string + "\n"

    def process_write(self, global_write=None):
        return_string = ""

        if not self.is_global:
            return_string += "tmux select-pane -t %d \n" % self.num

            if global_write is not None:
                return_string += global_write

        if self.resize is not None:
            return_string += self._generate_resize()

        if self.workspace is not None:
            return_string += self._generate_workspace()

        if self.export is not None:
            return_string += self._generate_export()

        if not self.alias is None:
            return_string += self._generate_alias()

        if not self.sendkeys is None:
            return_string += self._generate_sendkeys()

        return return_string

    def __sendkeys_string(self, string):
        return "tmux send-keys '%s' enter" % string

    def _generate_sendkeys(self):
        return_string = ""

        for sendkey in self.sendkeys:
            return_string += self.__sendkeys_string(sendkey)
            return_string += "\n"

        return return_string

    def _generate_alias(self):
        return_string = ""
        for key, value in self.alias.items():
            return_string += self.__alias_string(key, value)
            return_string += "\n"

        return return_string

    def __alias_string(self, key, value):
        return self.__sendkeys_string(
            'alias %s="%s"' % (key, value))

    def _generate_export(self):
        return_string = ""
        for key, value in self.export.items():
            return_string += self.__sendkeys_string(
                'export %s="%s"' % (key, value))
            return_string += "\n"
        return return_string

    def _generate_workspace(self):
        return_string = ""

        for key, value in self.workspace.items():
            alias_key = 'go-' + key
            alias_path = "cd " + value
            return_string += self.__alias_string(
                alias_key, alias_path)
            return_string += "\n"
        return return_string

    def _generate_resize(self):
        return_string = ""
        option_parser = {
            'up': '-U',
            'down': '-D',
            'left': '-L',
            'right': '-R'}

        for key, value in self.resize.items():
            return_string += "tmux resize-pane %s %d \n" % (
                option_parser[key], value)

        return return_string

    def _generate_tmux(self):
        return_string = ""

        for tmux in self.tmux:
            return_string += "tmux %s \n" % tmux

        return return_string


if __name__ == "__main__":
    debug = True
    test_yaml = yaml.load(open('example/deadtmux.yaml').read())
    panes = PaneManager(test_yaml)

    print panes.header_write()
    print panes.init_write()
    print panes.process_write()
    print panes.footer_write()
