# -*- coding: utf-8 -*-
from deadtmux import writer


def test_write_pane():
    test_pane = writer.Pane({
        'no': 0,
        'split-window': 'horizon'})
    result = test_pane.prosess_write()
    assert result.index('select-pane')
    assert result.index('0')


def test_split_window():
    test_pane = writer.Pane({
        'no': 0,
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
    result = test_pane.prosess_write()

    for include_string in [
        'chronium-browser',
        'cd',
            'send-keys']:

        assert result.index(include_string)


def test_alias():
    test_pane = writer.Pane({
        'no': 0,
        'split-window': 'horizon',
        'alias': {
            'work': 'cat hoge.txt'}})

    result = test_pane.prosess_write()

    for include_string in [
        'send-keys',
        'alias',
        'work',
            'hoge.txt']:

        assert result.index(include_string)


def test_pane_manager_init():
    test_pane_manager = writer.PaneManager(
        [{'split-window': 'horizon'},
         {'split-window': 'vertical'}])

    assert len(test_pane_manager.panes) == 2
