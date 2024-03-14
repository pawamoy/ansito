# ansito

[![ci](https://github.com/pawamoy/ansito/workflows/ci/badge.svg)](https://github.com/pawamoy/ansito/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/ansito/)
[![pypi version](https://img.shields.io/pypi/v/ansito.svg)](https://pypi.org/project/ansito/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/ansito)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#ansito:gitter.im)

Translate ANSI codes to any other format.

Currently, only Conky format is supported.

**:warning: This project is unmaintained.
Drop me a message if you would like me to transfer it to you
or add you as a collaborator.**

## Installation

With `pip`:

```bash
pip install ansito
```

With [`pipx`](https://github.com/pipxproject/pipx):

```bash
python3.8 -m pip install --user pipx
pipx install ansito
```

## Usage (command-line)

```
usage: ansito [-h] FILENAME

positional arguments:
  FILENAME    File to translate, or - for stdin.

optional arguments:
  -h, --help  show this help message and exit

```

Example:

```bash
command-that-output-colors | ansito -
```

Real-word example with `taskwarrior` in a Conky configuration file:

```lua
${texecpi 60 flock ~/.task task limit:10 rc.defaultwidth:80 rc._forcecolor:on rc.verbose:affected,blank list | ansito - | sed -r 's/([^ ])#/\1\\#/g'
```

:warning: **Conky does not have "background colors" for text,
so ansito will not be able to convert the ANSI codes for background colors
to Conky colors!**
