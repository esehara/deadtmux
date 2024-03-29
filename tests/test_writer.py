# -*- coding: utf-8 -*-
from deadtmux import writer


def test_write_pane():
    test_pane = writer.Pane({
        'no': 0,
        'split-window': 'horizon'})
    result = test_pane.process_write()
    assert result.index('select-pane')
    assert result.index('0')


def test_split_window():
    test_pane = writer.Pane({
        'no': 1,
        'split-window': 'horizon'})
    result = test_pane.init_write()

    for include_string in [
            'split-window', '-h']:
        assert result.index(include_string)

    test_pane = writer.Pane({
        'no': 1,
        'split-window': 'vertical'})
    result = test_pane.init_write()

    for include_string in [
            'split-window', '-v']:
        assert result.index(include_string)


def test_sendkeys():
    test_pane = writer.Pane({
        'no': 0,
        'split-window': 'horizon',
        'send-keys': [
            'chronium-browser',
            'cd /home/esehara/hogehoge/']})
    result = test_pane.process_write()

    for include_string in [
        'chronium-browser',
        'cd',
            'send-keys']:

        assert result.index(include_string)


def test_global_pane():
    test_pane = writer.Pane({
        'is_global': True,
        'send-keys': ['chrome-browser']})
    result = test_pane.process_write()

    for include_string in [
            'send-keys', 'chrome-browser']:
        print include_string
        assert result.index(include_string)

def test_alias():
    test_pane = writer.Pane({
        'no': 0,
        'split-window': 'horizon',
        'alias': {
            'work': 'cat hoge.txt'}})

    result = test_pane.process_write()

    for include_string in [
        'send-keys',
        'alias',
        'work',
            'hoge.txt']:

        assert result.index(include_string)


def test_export():

    test_pane = writer.Pane({
        'no': 0,
        'export': {'hoge': 'fuga'}})

    result = test_pane.process_write()
    print result

    for include_string in [
            'export', 'hoge', '=', 'fuga']:
        assert result.index(include_string)


def test_workspace():
    test_pane = writer.Pane({
        'no': 0,
        'workspace': {
            'root': '/home/hoge/', 'test': 'test', 'source': '/home/source/'}})
    assert test_pane.workspace['root'] == '/home/hoge/'
    assert test_pane.workspace['test'] == '/home/hoge/test'
    assert test_pane.workspace['source'] == '/home/source/'

    result = test_pane.process_write()

    for include_string in [
            'go-root', 'go-test', 'go-source']:
        assert result.index(include_string)


def test_resize():
    test_pane = writer.Pane({
        'no': 0,
        'resize': {
            'up': 10,
            'left': 20}})

    result = test_pane.process_write()

    for include_string in [
            'resize-pane', '-U', '-L']:
        assert result.index(include_string)

def test_pane_manager_init():
    test_pane_manager = writer.PaneManager(
        {
            "name": "foobar",
            "panes":
                [{'split-window': 'horizon'},
                {'split-window': 'vertical'}]})

    assert len(test_pane_manager.panes) == 2


def test_pane_manager_init_writer():
    test_pane_manager = writer.PaneManager(
        {
            'name': 'foobar',
            'panes':
                [{'split-window': 'horizon'},
                {'split-window': 'vertical'}]})

    result = test_pane_manager.init_write()

    for include_string in ['-v', ]:
        assert result.index(include_string)


def test_pane_manager_process_writer():
    test_pane_manager = writer.PaneManager(
        {
            "name": 'foobar',
            "panes": [
                {
                    'send-keys': ['chrome-browser']},
                {
                    'split-window': 'vertical',
                    'alias': {'work': 'cat hoge.txt'}}]})

    result = test_pane_manager.process_write()

    for include_string in [
        'select-pane',
            'alias', 'work', '=']:
        assert result.index(include_string)


def test_window_setting():
    test_pane_manager = writer.PaneManager(
        {"name": "foobar",
            "panes": [
                {"send-keys":
                    ['chorium-browser']}]})

    result = test_pane_manager.header_write()


def test_window_manager_prefix():
    test_pane_manager = writer.WindowManager(
        [
            {
                'configure': {
                    'run': 'byobu',
                    'focus-pane': 1,
                    'focus-window': 'foobar'}},
            {
                'window': {
                    'name': 'foobar',
                    'panes': [
                        {'send-keys':
                            ['chronium-browser']}]}}])

    result = test_pane_manager.header_write()
    result += test_pane_manager.footer_write()

    for include_string in [
            'byobu', 'select-pane', 'detach']:
        result.index(include_string)


def test_window_manager():
    test_window_manager = writer.WindowManager(
        [
            {'configure':
                {'run': 'byobu',
                 'focus-window': 'hogehoge',
                 'focus-pane': 0}},
            {'window':
                {
                    'name': 'hogehoge',
                    'panes': [
                        {'send-keys': ['chrome-browser']}]}},
            {'window':
                {
                    'name': 'fugafuga',
                    'panes': [
                        {'send-keys': ['chrome-browser']}]}}, ])

    result = test_window_manager.output()
    for include_string in [
            'rename-window', 'new-window', '-t']:
        result.index(include_string)
