# TODO

- [ ] Fixing (0.0.1):
  + [x] Rename to `kitpos`
  + [ ] Packaging:
    - [x] `python-kitpos.spec`
    - [x] `pyproject.toml` (PEP-621)
    - [ ] `tox.ini`
    - [x] ~~`requirements.txt`, `setup.py`, `setup,cfg`, `MANIFEST.in`~~
  + [ ] Dox
  + [ ] Lint:
    - [x] `pydocstyle`
    - [x] `flake8`
    - [ ] `pylint`
    - [ ] coverage
  + [ ] Exceptions (catch, wrap into KitPOS&hellip;)
  + [ ] Tests
  + [ ] Logging(v)
- [ ] Sequences:
  + [ ] SessionOpen
  + [ ] SessionClose
  + [ ] Receipt
  + [ ] CorReceipt
- [ ] Extend cmd #5 (8):
  + [ ] 0x40: ResetMLM
  + [ ] FSClose (3)
  + [ ] *Re*Register (4):
    - [ ] 0x3B: ReadRegDoc
    - [ ] 0x12: RegisterStart
    - [ ] 0x16: RegisterData
    - [ ] 0x13: RegisterFlush
- [ ] Extend cmd #6 (GetDocByNum #2):
  + [ ]  6: FSCloseRpt (5.6?)
  + [ ] 21: SattleRpt (5.7)
  + [ ]  4: BSO
  + [ ] 41: CorBSO
  + [ ]  7: OpConfirm
- [ ] Misc
  + [ ] Async txrx
  + [ ] Multitag
  + [ ] Online tests (w/ live FRs)

## Maybe
- [ ] FR: State diagramm
- [ ] flag._Flags: metaclass

## Tags used:
1009, 1021, 1023, 1030, 1031, 1036, 1055, 1059, 1079, 1081,
1103, 1104, 1105, 1106, 1107, 1173, 1174, 1177, 1178, 1179,
1187, 1192, 1199, 1203, 1212, 1214, 1215, 1216, 1217, 30000
