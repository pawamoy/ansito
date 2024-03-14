"""Tests for the `cli` module."""

from __future__ import annotations

import io

import pytest

from ansito import cli, debug


def test_main() -> None:
    """Basic CLI test."""
    assert cli.main([]) == 0


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "ansito" in captured.out


def test_show_version(capsys: pytest.CaptureFixture) -> None:
    """Show version.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-V"])
    captured = capsys.readouterr()
    assert debug.get_version() in captured.out


def test_show_debug_info(capsys: pytest.CaptureFixture) -> None:
    """Show debug information.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["--debug-info"])
    captured = capsys.readouterr().out.lower()
    assert "python" in captured
    assert "system" in captured
    assert "environment" in captured
    assert "packages" in captured


def test_main_ok_with_stdin(capsys, monkeypatch):
    """Correctly converts ANSI codes from standard input."""
    monkeypatch.setattr("sys.stdin", io.StringIO("\x1b[;34;41mhey\x1b[0m\n"))
    assert cli.main(["-"]) == 0
    lines = capsys.readouterr().out.rstrip("\n").split("\n")
    assert len(lines) == 1
    assert lines[0] == "${color blue}hey${color}"
