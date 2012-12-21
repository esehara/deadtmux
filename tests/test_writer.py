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


def test_pane_manager_init():
    test_pane_manager = writer.PaneManager(
        [{'split-window': 'horizon'},
         {'split-window': 'vertical'}])

    assert len(test_pane_manager.panes) == 2


def test_pane_manager_init_writer():
    test_pane_manager = writer.PaneManager(
        [{'split-window': 'horizon'},
         {'split-window': 'vertical'}])

    result = test_pane_manager.init_write()

    for include_string in ['-v', ]:
        assert result.index(include_string)


def test_pane_manager_process_writer():
    test_pane_manager = writer.PaneManager(
        [
            {
                'split-window': 'horizon',
                'send-keys': ['chrome-browser']},
            {
                'split-window': 'vertical',
                'alias': {'work': 'cat hoge.txt'}}])

    result = test_pane_manager.process_write()

    for include_string in [
        'select-pane',
            'alias', 'work', '=']:
        assert result.index(include_string)
