# TODO

## 0.0.2:
- [ ] Extend cmd #5 (14):
  - [ ] GetX (simple): 0x02, 03, 05, 06, 07, 0B, 0E, 32, 33, 75, 77, 79, 81, BB
- [ ] Sequences:
  + [ ] SessionOpen
  + [ ] SessionClose
  + [ ] Receipt
  + [ ] CorReceipt
- [ ] net:
  + [ ] strict (header, len, crc)
  + [ ] async

## 0.0.3:
- [ ] Tests (&rArr; coverage)
- [ ] Extend cmd #6 (8):
  + [ ] GetX complex (0x09, 35..36, 3B)
  + [ ] 0x40: ResetMLM
  + [ ] FSClose (3 (0x14, 0x17, 0x15)) - not documented
  + [ ] *Re*Register (4):
    - [ ] 0x3B: ReadRegDoc
    - [ ] 0x12: RegisterStart
    - [ ] 0x16: RegisterData
    - [ ] 0x13: RegisterFlush
- [ ] Extend cmd #7 (GetDocByNum #2):
  + [ ]  6: FSCloseRpt (5.6?)
  + [ ] 21: SattleRpt (5.7)
  + [ ]  4: BSO
  + [ ] 41: CorBSO
  + [ ]  7: OpConfirm
- [ ] Misc
  + [ ] `tox.ini`
  + [ ] Multitag
  + [ ] Online tests (w/ live FRs)
- Maybe:
  + Verbosity: up to 6 lvls
  + IEnumCmd &hArr; CmdX &hArr; RcpX
  + Mypy
  + POS State diagramm
  + flag._Flags: metaclass
  + Nice exception traceback
  + POS-stub
