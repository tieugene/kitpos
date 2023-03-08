# TODO

- [ ] New tags
  + [ ] 1171
  + [ ] 1222
  + [ ] 1225
  + [ ] 1226
- [ ] net:
  + [ ] strict (header, len, crc)
  + [ ] async
- [ ] Sequences:
  + [ ] SessionOpen
  + [ ] SessionClose
  + [ ] Receipt
  + [ ] CorReceipt
- [ ] Tests (&rArr; coverage)
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
