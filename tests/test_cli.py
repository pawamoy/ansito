import io

from ansito import cli


def test_main_ok_with_stdin(capsys, monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('[;34;41mhey[0m\n'))
    assert cli.main(["-"]) == 0
    lines = capsys.readouterr().out.rstrip("\n").split("\n")
    assert len(lines) == 1
    assert lines[0] == "${color blue}hey${color}"
