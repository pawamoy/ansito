"""Tests for the `cli` module."""

import pytest

from ansito import cli


def test_main():
    """Basic CLI test."""
    assert cli.main([]) == 0


def test_show_help(capsys):
    """
    Shows help.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "ansito" in captured.out


def test_main_ok_with_stdin(capsys, monkeypatch):
    """Correctly converts ANSI codes from standard input."""
    monkeypatch.setattr("sys.stdin", io.StringIO("[;34;41mhey[0m\n"))
    assert cli.main(["-"]) == 0
    lines = capsys.readouterr().out.rstrip("\n").split("\n")
    assert len(lines) == 1
    assert lines[0] == "${color blue}hey${color}"
