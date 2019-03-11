<!--
IMPORTANT:
  This file is generated from the template at 'scripts/templates/README.md'.
  Please update the template instead of this file.
-->

# ansito
[![pipeline status](https://gitlab.com/pawamoy/ansito/badges/master/pipeline.svg)](https://gitlab.com/pawamoy/ansito/pipelines)
[![coverage report](https://gitlab.com/pawamoy/ansito/badges/master/coverage.svg)](https://gitlab.com/pawamoy/ansito/commits/master)
[![documentation](https://img.shields.io/readthedocs/ansito.svg?style=flat)](https://ansito.readthedocs.io/en/latest/index.html)
[![pypi version](https://img.shields.io/pypi/v/ansito.svg)](https://pypi.org/project/ansito/)

Translate ANSI codes to any other format.

Currently, only Conky format is supported.

## Requirements
ansito requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.8

# make it available globally
pyenv global system 3.6.8
```
</details>

## Installation
With `pip`:
```bash
python3.6 -m pip install ansito
```

With [`pipx`](https://github.com/cs01/pipx):
```bash
# install pipx with the recommended method
curl https://raw.githubusercontent.com/cs01/pipx/master/get-pipx.py | python3

pipx install --python python3.6 ansito
```

## Usage (as a library)
TODO

## Usage (command-line)
```
{{ command_line_help }}
```

Example:

```bash
command-that-output-colors | ansito -
```

Real-word example with `taskwarrior` in a Conky configuration file:

```lua
${texecpi 60 flock ~/.task task limit:10 rc.defaultwidth:80 rc._forcecolor:on rc.verbose:affected,blank list | ansito - | sed -r 's/([^ ])#/\1\\#/g'
```

{% if commands %}Commands:
{% for command in commands %}
- [`{{ command.name }}`](#{{ command.name }}){% endfor %}

{% for command in commands %}
### `{{ command.name }}`
```
{{ command.help }}
```

{% include "command_" + command.name.replace("-", "_") + "_extra.md" ignore missing %}
{% endfor %}{% endif %}
