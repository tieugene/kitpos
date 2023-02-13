# kitpos

Python library to control Kit-Invest's POS terminals.

## Requirements

- Python 3.9+
- [crcmod](https://crcmod.sourceforge.net) python library

## Installation

```py
pip3 install -e <project_folder>
```

## [CLI](https://en.wikipedia.org/wiki/Command-line_interface)

After library installation there will be `kitpos` utility to _demonstrate_ library functionality.
Type `kitpos -h` for help.

### JSON

Some commands require simple digit arguments (like `kitpos 1.2.3.4 SetDateTime 2302100046`).
But another ones need more comlicated data as json.
One way is to put json string as argument itself with same content:
```sh
kitpos <host> <cmd> 'json_string_without_spaces'
```
Another way is to point to json file (`-f` option):
```sh
kitpos -f <host> <cmd> json_file.json
```

### Sequences

Some POS commands should be called in sequences.
Some minimal samples:

- Session open:
  1. `SessionOpenBegin 1`
  2. `SessionOpenCommit`
- Session close:
  1. `SessionCloseBegin 1`
  2. `SessionCloseCommit`
- Receipt:
  1. `ReceiptBegin`
  2. `ReceiptItem <json>`
  3. `ReceiptAutomat <json>`
  4. `ReceiptPayment <json>`
  5. `ReceiptCommit <json>`
- Correction Receipt:
  1. `CorrReceiptBegin`
  2. `CorrReceiptData <json>`
  3. `CorrReceiptAutomat <json>`
  4. `CorrReceiptCommit <json>`

## Who's'who
- [`kitpos/`](`kitpos`): Library itself:
  + [`cmd`](kitpos/cmd.py): Cmd\* - POS commands handlers
  + [`rsp`](kitpos/rsp.py): Rsp\* - POS responses handlers
  + [`tag`](kitpos/tag.py): Tags handlers
  + [`const`](kitpos/const.py): Common constants
  + [`flag`](kitpos/flag.py): [`Flag`](https://docs.python.org/3/library/enum.html#enum.Flag)-based helping classes
  + [`util`](kitpos/util.py): Misc common utility functions
  + [`exc`](kitpos/exc.py): Exception classes
  + [`net`](kitpos/net.py): POS Tx/Rx sample
  + [`main`](kitpos/main.py): CLI entry point
  + [`cli`](kitpos/cli.py): CLI helpers

## Similar
- [pyshtrih](https://github.com/oleg-golovanov/pyshtrih)

## Licensing
You may use this library under the terms of the [GPLv3](LICENSE) license.
