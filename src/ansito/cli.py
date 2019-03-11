# coding=utf-8
"""
Module that contains the command line application.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later,
but that will cause problems: the code will get executed twice:

- When you run `python -m ansito` python will execute
  ``__main__.py`` as a script. That means there won't be any
  ``ansito.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``ansito.__main__`` in ``sys.modules``.

Also see http://click.pocoo.org/5/setuptools/#setuptools-integration.
"""

# https://unix.stackexchange.com/questions/230613/how-can-i-display-Ansi-color-in-a-cli-conky-display#230706
# http://wiki.bash-hackers.org/scripting/terminalcodes
# https://github.com/F1LT3R/parse-Ansi/blob/master/Ansi-seqs-to-Ansi-tags.js

# https://www.wikiwand.com/en/Ansi_escape_code#/Colors

# ═════════╦════════════════════════════════╦═════════════════════════════════════════════════════════════════════════╗
#  Code    ║             Effect             ║                                   Note                                  ║
# ═════════╬════════════════════════════════╬═════════════════════════════════════════════════════════════════════════╣
# 0        ║  Reset / Normal                ║  all attributes off                                                     ║
# 1        ║  Bold or increased intensity   ║                                                                         ║
# 2        ║  Faint (decreased intensity)   ║  Not widely supported.                                                  ║
# 3        ║  Italic                        ║  Not widely supported. Sometimes treated as inverse.                    ║
# 4        ║  Underline                     ║                                                                         ║
# 5        ║  Slow Blink                    ║  less than 150 per minute                                               ║
# 6        ║  Rapid Blink                   ║  MS-DOS Ansi.SYS; 150+ per minute; not widely supported                 ║
# 7        ║  [[reverse video]]             ║  swap foreground and background colors                                  ║
# 8        ║  Conceal                       ║  Not widely supported.                                                  ║
# 9        ║  Crossed-out                   ║  Characters legible, but marked for deletion.  Not widely supported.    ║
# 10       ║  Primary(default) font         ║                                                                         ║
# 11–19    ║  Alternate font                ║  Select alternate font `n-10`                                           ║
# 20       ║  Fraktur                       ║  hardly ever supported                                                  ║
# 21       ║  Bold off or Double Underline  ║  Bold off not widely supported; double underline hardly ever supported. ║
# 22       ║  Normal color or intensity     ║  Neither bold nor faint                                                 ║
# 23       ║  Not italic, not Fraktur       ║                                                                         ║
# 24       ║  Underline off                 ║  Not singly or doubly underlined                                        ║
# 25       ║  Blink off                     ║                                                                         ║
# 27       ║  Inverse off                   ║                                                                         ║
# 28       ║  Reveal                        ║  conceal off                                                            ║
# 29       ║  Not crossed out               ║                                                                         ║
# 30–37    ║  Set foreground color          ║  See color table below                                                  ║
# 38       ║  Set foreground color          ║  Next arguments are `5;n` or `2;r;g;b`, see below                       ║
# 39       ║  Default foreground color      ║  implementation defined (according to standard)                         ║
# 40–47    ║  Set background color          ║  See color table below                                                  ║
# 48       ║  Set background color          ║  Next arguments are `5;n` or `2;r;g;b`, see below                       ║
# 49       ║  Default background color      ║  implementation defined (according to standard)                         ║
# 51       ║  Framed                        ║                                                                         ║
# 52       ║  Encircled                     ║                                                                         ║
# 53       ║  Overlined                     ║                                                                         ║
# 54       ║  Not framed or encircled       ║                                                                         ║
# 55       ║  Not overlined                 ║                                                                         ║
# 60       ║  ideogram underline            ║  hardly ever supported                                                  ║
# 61       ║  ideogram double underline     ║  hardly ever supported                                                  ║
# 62       ║  ideogram overline             ║  hardly ever supported                                                  ║
# 63       ║  ideogram double overline      ║  hardly ever supported                                                  ║
# 64       ║  ideogram stress marking       ║  hardly ever supported                                                  ║
# 65       ║  ideogram attributes off       ║  reset the effects of all of 60-64                                      ║
# 90–97    ║  Set bright foreground color   ║  aixterm (not in standard)                                              ║
# 100–107  ║  Set bright background color   ║  aixterm (not in standard)                                              ║
# ═════════╩════════════════════════════════╩═════════════════════════════════════════════════════════════════════════╝

import argparse
import sys

MAP = {
    0: "reset",
    1: "font bold",
    2: "font faint",
    3: "font italic",
    4: "font underline",
    5: "font slow blink",
    6: "font rapid blink",
    7: "color reverse",
    8: "font conceal",
    9: "font crossed out",
    10: "font default",
    11: "font alternate 1",
    12: "font alternate 2",
    13: "font alternate 3",
    14: "font alternate 4",
    15: "font alternate 5",
    16: "font alternate 6",
    17: "font alternate 7",
    18: "font alternate 8",
    19: "font alternate 9",
    20: "font fraktur",
    21: "font bold off / double underline",
    22: "color default",
    23: "font italic and fraktur off",
    24: "font underline off",
    25: "font blink off",
    # 26,
    27: "color reverse off",
    28: "font reveal",
    29: "font crossed out off",
    30: "color fg black",
    31: "color fg red",
    32: "color fg green",
    33: "color fg yellow",
    34: "color fg blue",
    35: "color fg magenta",
    36: "color fg cyan",
    37: "color fg white",
    38: {2: "color fg rgb", 5: "color fg 256"},
    39: "color fg default",
    40: "color bg black",
    41: "color bg red",
    42: "color bg green",
    43: "color bg yellow",
    44: "color bg blue",
    45: "color bg magenta",
    46: "color bg cyan",
    47: "color bg white",
    48: {2: "color bg rgb", 5: "color bg 256"},
    49: "color bg default",
    # 50,
    51: "font framed",
    52: "font encircled",
    53: "font overlined",
    54: "font framed and encircled off",
    55: "font overlined off",
    # 56 - 59,
    60: "ideogram underline",
    61: "ideogram double underline",
    62: "ideogram overline",
    63: "ideogram double overline",
    64: "ideogram stress marking",
    65: "ideogram attributes off",
    # 66 - 89,
    90: "color fg bright black",
    91: "color fg bright red",
    92: "color fg bright green",
    93: "color fg bright yellow",
    94: "color fg bright blue",
    95: "color fg bright magenta",
    96: "color fg bright cyan",
    97: "color fg bright white",
    # 98 - 99,
    100: "color bg bright black",
    101: "color bg bright red",
    102: "color bg bright green",
    103: "color bg bright yellow",
    104: "color bg bright blue",
    105: "color bg bright magenta",
    106: "color bg bright cyan",
    107: "color bg bright white",
}

# Could be used instead:
# https://github.com/selectel/pyte/blob/master/pyte/graphics.py
MAP_256_COLOR = {
    16: "#000000",
    17: "#00005f",
    18: "#000087",
    19: "#0000af",
    20: "#0000d7",
    21: "#0000ff",
    22: "#005f00",
    23: "#005f5f",
    24: "#005f87",
    25: "#005faf",
    26: "#005fd7",
    27: "#005fff",
    28: "#008700",
    29: "#00875f",
    30: "#008787",
    31: "#0087af",
    32: "#0087d7",
    33: "#0087ff",
    34: "#00af00",
    35: "#00af5f",
    36: "#00af87",
    37: "#00afaf",
    38: "#00afd7",
    39: "#00afff",
    40: "#00d700",
    41: "#00d75f",
    42: "#00d787",
    43: "#00d7af",
    44: "#00d7d7",
    45: "#00d7ff",
    46: "#00ff00",
    47: "#00ff5f",
    48: "#00ff87",
    49: "#00ffaf",
    50: "#00ffd7",
    51: "#00ffff",
    52: "#5f0000",
    53: "#5f005f",
    54: "#5f0087",
    55: "#5f00af",
    56: "#5f00d7",
    57: "#5f00ff",
    58: "#5f5f00",
    59: "#5f5f5f",
    60: "#5f5f87",
    61: "#5f5faf",
    62: "#5f5fd7",
    63: "#5f5fff",
    64: "#5f8700",
    65: "#5f875f",
    66: "#5f8787",
    67: "#5f87af",
    68: "#5f87d7",
    69: "#5f87ff",
    70: "#5faf00",
    71: "#5faf5f",
    72: "#5faf87",
    73: "#5fafaf",
    74: "#5fafd7",
    75: "#5fafff",
    76: "#5fd700",
    77: "#5fd75f",
    78: "#5fd787",
    79: "#5fd7af",
    80: "#5fd7d7",
    81: "#5fd7ff",
    82: "#5fff00",
    83: "#5fff5f",
    84: "#5fff87",
    85: "#5fffaf",
    86: "#5fffd7",
    87: "#5fffff",
    88: "#870000",
    89: "#87005f",
    90: "#870087",
    91: "#8700af",
    92: "#8700d7",
    93: "#8700ff",
    94: "#875f00",
    95: "#875f5f",
    96: "#875f87",
    97: "#875faf",
    98: "#875fd7",
    99: "#875fff",
    100: "#878700",
    101: "#87875f",
    102: "#878787",
    103: "#8787af",
    104: "#8787d7",
    105: "#8787ff",
    106: "#87af00",
    107: "#87af5f",
    108: "#87af87",
    109: "#87afaf",
    110: "#87afd7",
    111: "#87afff",
    112: "#87d700",
    113: "#87d75f",
    114: "#87d787",
    115: "#87d7af",
    116: "#87d7d7",
    117: "#87d7ff",
    118: "#87ff00",
    119: "#87ff5f",
    120: "#87ff87",
    121: "#87ffaf",
    122: "#87ffd7",
    123: "#87ffff",
    124: "#af0000",
    125: "#af005f",
    126: "#af0087",
    127: "#af00af",
    128: "#af00d7",
    129: "#af00ff",
    130: "#af5f00",
    131: "#af5f5f",
    132: "#af5f87",
    133: "#af5faf",
    134: "#af5fd7",
    135: "#af5fff",
    136: "#af8700",
    137: "#af875f",
    138: "#af8787",
    139: "#af87af",
    140: "#af87d7",
    141: "#af87ff",
    142: "#afaf00",
    143: "#afaf5f",
    144: "#afaf87",
    145: "#afafaf",
    146: "#afafd7",
    147: "#afafff",
    148: "#afd700",
    149: "#afd75f",
    150: "#afd787",
    151: "#afd7af",
    152: "#afd7d7",
    153: "#afd7ff",
    154: "#afff00",
    155: "#afff5f",
    156: "#afff87",
    157: "#afffaf",
    158: "#afffd7",
    159: "#afffff",
    160: "#d70000",
    161: "#d7005f",
    162: "#d70087",
    163: "#d700af",
    164: "#d700d7",
    165: "#d700ff",
    166: "#d75f00",
    167: "#d75f5f",
    168: "#d75f87",
    169: "#d75faf",
    170: "#d75fd7",
    171: "#d75fff",
    172: "#d78700",
    173: "#d7875f",
    174: "#d78787",
    175: "#d787af",
    176: "#d787d7",
    177: "#d787ff",
    178: "#d7af00",
    179: "#d7af5f",
    180: "#d7af87",
    181: "#d7afaf",
    182: "#d7afd7",
    183: "#d7afff",
    184: "#d7d700",
    185: "#d7d75f",
    186: "#d7d787",
    187: "#d7d7af",
    188: "#d7d7d7",
    189: "#d7d7ff",
    190: "#d7ff00",
    191: "#d7ff5f",
    192: "#d7ff87",
    193: "#d7ffaf",
    194: "#d7ffd7",
    195: "#d7ffff",
    196: "#ff0000",
    197: "#ff005f",
    198: "#ff0087",
    199: "#ff00af",
    200: "#ff00d7",
    201: "#ff00ff",
    202: "#ff5f00",
    203: "#ff5f5f",
    204: "#ff5f87",
    205: "#ff5faf",
    206: "#ff5fd7",
    207: "#ff5fff",
    208: "#ff8700",
    209: "#ff875f",
    210: "#ff8787",
    211: "#ff87af",
    212: "#ff87d7",
    213: "#ff87ff",
    214: "#ffaf00",
    215: "#ffaf5f",
    216: "#ffaf87",
    217: "#ffafaf",
    218: "#ffafd7",
    219: "#ffafff",
    220: "#ffd700",
    221: "#ffd75f",
    222: "#ffd787",
    223: "#ffd7af",
    224: "#ffd7d7",
    225: "#ffd7ff",
    226: "#ffff00",
    227: "#ffff5f",
    228: "#ffff87",
    229: "#ffffaf",
    230: "#ffffd7",
    231: "#ffffff",
    232: "#080808",
    233: "#121212",
    234: "#1c1c1c",
    235: "#262626",
    236: "#303030",
    237: "#3a3a3a",
    238: "#444444",
    239: "#4e4e4e",
    240: "#585858",
    241: "#626262",
    242: "#6c6c6c",
    243: "#767676",
    244: "#808080",
    245: "#8a8a8a",
    246: "#949494",
    247: "#9e9e9e",
    248: "#a8a8a8",
    249: "#b2b2b2",
    250: "#bcbcbc",
    251: "#c6c6c6",
    252: "#d0d0d0",
    253: "#dadada",
    254: "#e4e4e4",
    255: "#eeeeee",
}


def split_sequence(char_list):
    codes = [int(n) for n in "".join(char_list).split(";") if n.isdigit()]

    if not codes:
        codes = [0]

    seqs = []

    c = 0
    while c < len(codes):
        ansi = MAP[codes[c]]

        while isinstance(ansi, dict):
            ansi = ansi[codes[c + 1]]
            c += 1

        if ansi in ("color fg 256", "color bg 256"):
            value = codes[c + 1]
            c += 1
        elif ansi in ("color fg rgb", "color bg rgb"):
            value = (codes[c + 1], codes[c + 2], codes[c + 3])
            c += 3
        else:
            value = None

        seq = {"type": ansi}
        if value is not None:
            seq["value"] = value

        seqs.append(seq)
        c += 1

    return seqs


def yield_sequences(text):
    cur_text = []

    pos = 0
    while pos < len(text):
        if ord(text[pos]) == 27 and text[pos + 1] == "[":
            if cur_text:
                yield {"type": "text", "value": "".join(cur_text)}
                cur_text = []
            pos += 2
            char_list = []
            while text[pos] != "m":
                char_list.append(text[pos])
                pos += 1
            for seq in split_sequence(char_list):
                yield seq
        else:
            cur_text.append(text[pos])
        pos += 1

    if cur_text:
        yield {"type": "text", "value": "".join(cur_text)}


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def to_conky(sequences):
    for seq in sequences:
        c = seq_to_conky(seq)
        if c is not None:
            yield seq_to_conky(seq)


def seq_to_conky(seq):
    if seq["type"] == "text":
        return seq["value"]
    elif seq["type"] == "reset":
        return "${color}"
    elif seq["type"] == "color fg black":
        return "${color black}"
    elif seq["type"] == "color fg red":
        return "${color red}"
    elif seq["type"] == "color fg green":
        return "${color green}"
    elif seq["type"] == "color fg yellow":
        return "${color yellow}"
    elif seq["type"] == "color fg blue":
        return "${color blue}"
    elif seq["type"] == "color fg magenta":
        return "${color magenta}"
    elif seq["type"] == "color fg cyan":
        return "${color cyan}"
    elif seq["type"] == "color fg white":
        return "${color white}"
    elif seq["type"] == "color fg rgb":
        return "${color %s}" % rgb_to_hex(seq["value"])
    elif seq["type"] == "color fg 256":
        if 0 <= seq["value"] <= 7:
            return seq_to_conky({"type": MAP[seq["value"] + 30]})
        elif 8 <= seq["value"] <= 15:
            return seq_to_conky({"type": MAP[seq["value"] + 82]})
        else:
            return "${color %s}" % MAP_256_COLOR[seq["value"]]


def get_parser():
    parser = argparse.ArgumentParser(prog="ansito")
    parser.add_argument("filename", metavar="FILENAME", help="File to translate, or - for stdin.")
    return parser


def main(args=None):
    """The main function, which is executed when you type ``ansito`` or ``python -m ansito``."""
    parser = get_parser()
    args = parser.parse_args(args=args)
    if args.filename == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.filename) as stream:
                text = stream.read()
        except FileNotFoundError as e:
            print(e, file=sys.stderr)

    for s in to_conky(yield_sequences(text)):
        print(s, end="")

    return 0
