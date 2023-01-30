# TODO

- [ ] Extend cmd #3 (11):
  + [ ] 0x3A: ReadDoc [^1]
  + [ ] Receipt (6):
    - [ ] 0x23: Begin
    - [ ] 0x2B: Position
    - [ ] 0x2C: Agent
    - [ ] 0x2D: Payment
    - [ ] 0x1F: AutoNum
    - [ ] 0x24: Comit
  + [ ] CorrReceipt (4):
    - [ ] 0x25: Begin
    - [ ] 0x2E: Data
    - [ ] 0x3F: CorAutoNum
    - [ ] 0x26: Commit
- [ ] Sequences:
  - [ ] SessionOpen
  - [ ] SessionClose
  - [ ] Receipt
  - [ ] CorReceipt
- [ ] Extend cmd #4 (FS (7)):
  + [ ] 0x40: ResetMLM
  + [ ] FSClose (3):
  + [ ] *Re*Register (3):
    - [ ] 0x3B: ReadRegDoc
    - [ ] 0x12: RegisterStart
    - [ ] 0x16: RegisterData
    - [ ] 0x13: RegisterFlush
- [ ] Extend cmd #5 (GetDocByNum #2):
  - [ ]  6: FSCloseRpt (5.6?)
  - [ ] 21: SattleRpt (5.7)
  - [ ]  4: BSO
  - [ ] 41: CorBSO
  - [ ]  7: OpConfirm
- [ ] Add tests: online tests (w/ live FRs)
- [ ] Async txrx
- [ ] Wrap all exceptions with `exc.KitX(e)`
- [ ] Packaging (`requirements.txt`, `setup.{py,cfg}`, `kitfr.spec`, `?MANIFEST.in`, `?tox.*`)

## Maybe
- [ ] FR: State diagramm
- [ ] flag._Flags: metaclass

## [^1]: Tags used:
1009, 1021, 1023, 1030, 1031, 1036, 1055, 1059, 1079, 1081,
1103, 1104, 1105, 1106, 1107, 1173, 1174, 1177, 1178, 1179,
1187, 1192, 1199, 1203, 1212, 1214, 1215, 1216, 1217, 30000
