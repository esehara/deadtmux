# -*- coding: utf-8 -*-
import yaml
import re
import os

debug = False


class WindowManager(object):

    global_pane = None

    def __init__(self, args):

        self.window = []

        no = 0
        for window in args:

            if 'configure' in window:
                self.configure = window['configure']

                if ('new-window' in window['configure'] and
                        window['configure']['new-window']):
                    no = 1

                continue

            if ('is_global' in window and
                    window['is_global']):
                self.global_pane = Pane(window)
                continue

            self.window.append(
                PaneManager(window['window'], no))
            no += 1

    def output(self):
        result_string = ""
        result_string += self.header_write()

        for window in self.window:
            global_string = None

            if self.global_pane is not None:
                global_string = self.global_pane.process_write()

            result_string += window.output(global_string)

        result_string += self.footer_write()
        return result_string

    def header_write(self):
        return_string = ""

        if 'run' in self.configure:
            return_string += "%s & \n" % self.configure['run']
        
        return_string += "sleep 1 \n"
        return return_string

    def footer_write(self):
        return_string = ""
        return_string += "tmux select-window -t %s \n" % self.configure[
            'focus-window']
        return_string += "tmux select-pane -t %d \n" % self.configure[
            'focus-pane']

        if 'run' in self.configure:
            return_string += "tmux detach \n"
            return_string += "%s\n" % self.configure['run']
        return return_string


class PaneManager(object):

    panes = None
    no = 0
    name = None
    global_pane = None
    configure = None

    def __init__(self, ars, window_no=0):

        self.panes = []
        self.no = window_no
        no = 0

        self.name = ars['name']

        for ar in ars['panes']:
            if ('is_global' in ar and
                    ar['is_global']):
                self.global_pane = Pane(ar)
                continue

            ar['no'] = no
            self.panes.append(Pane(ar))
            no += 1

    def init_write(self):
        return_string = ""

        for pane in self.panes:
            return_string += pane.init_write()

        return return_string

    def process_write(self, global_string=None):
        return_string = ""
        for pane in self.panes:
            global_write = ""

            if global_string is not None:
                global_write += global_string

            if self.global_pane is not None:
                global_write += self.global_pane.process_write()

            if global_write == "":
                global_write = None

            return_string += pane.process_write(
                global_write)
        return return_string

    def header_write(self):
        return_string = ""

        if self.no != 0:
            return_string += 'tmux new-window -n %s' % self.name
        else:
            return_string += 'tmux rename-window %s' % self.name

        return return_string

    def output(self, global_string=None):
        return_string = ""
        return_string += self.header_write()
        return_string += self.init_write()
        return_string += self.process_write(global_string)
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
    panes = WindowManager(test_yaml)

    print panes.header_write()
    print panes.init_write()
    print panes.process_write()
    print panes.footer_write()
