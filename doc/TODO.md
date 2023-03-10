# TODO

## 0.0.2:
- [x] #32: 0x81: Get POS ctrl parms
- [ ] #33: 0x3B: ReadRegDoc
- [ ] #27: Pretty print tags
- [ ] #30: Autodoc commands
- [ ] #34: FSClose (not documented):
  - [ ] GetDocByNum(6: FSCloseRpt (5.6?))
  - [ ] 0x14: CloseStorageBegin
  - [ ] 0x17: CloseStorageData
  - [ ] 0x15: CloseStorageCommit
- [ ] Sequences:
  + [ ] SessionOpen
  + [ ] SessionClose
  + [ ] Receipt
  + [ ] CorReceipt
- [ ] net:
  + [ ] strict (header, len, crc)
  + [ ] async
- [ ] #35: Tags as objects (from_json, from_bytes, to_bytes, to_str, to_native)

## 0.0.3:
- [ ] Extend cmd #6 (8):
  + [ ] GetX complex (0x09, 35..36, 79)
  + [ ] *Re*Register (4):
    + [ ] 0x40: ResetMLM
    - [ ] 0x12: RegisterBegin
    - [ ] 0x16: RegisterData
    - [ ] 0x13: RegisterCommit
- [ ] #8: Extend cmd #7 (GetDocByNum #2):
  + [ ] 21: SattleRpt (5.7)
  + [ ]  4: BSO
  + [ ] 41: CorBSO
  + [ ]  7: OpConfirm
- [ ] Misc
  + [ ] `tox.ini`
  + [ ] Multitag
  + [ ] Online tests (w/ live FRs)
- [ ] Tests (&rArr; coverage)

## Maybe:
  + Verbosity: up to 6 lvls
  + IEnumCmd &hArr; CmdX &hArr; RcpX
  + Mypy
  + POS State diagramm
  + flag._Flags: metaclass
  + Nice exception traceback
  + POS-stub

## 