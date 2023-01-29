# TODO

- [ ] Extend cmd #2 (Sequences, (15)):
  + [ ] 0x10: CancelDoc
  + [ ] Session (4):
    - [ ] 0x21: OpenStart
    - [ ] 0x22: Open
    - [ ] 0x29: CloseStart
    - [ ] 0x2A: Close
  + [ ] Receipt (6):
    - [ ] 0x23: Start
    - [ ] 0x2B: Position
    - [ ] 0x2C: Agent
    - [ ] 0x2D: Payment
    - [ ] 0x1F: AutoNum
    - [ ] 0x24: Flush
  + [ ] CorrReceipt (4):
    - [ ] 0x25: Start/Begin
    - [ ] 0x2E: Data
    - [ ] 0x3F: CorAutoNum
    - [ ] 0x26: ~~Flush~~Finalize (Commit, Push)
- [ ] Extend cmd #3 (FS (7)):
  + [ ] 0x40: ResetMLM
  + [ ] FSClose (3):
  + [ ] *Re*Register (3):
    - [ ] 0x12: RegisterStart
    - [ ] 0x16: RegisterData
    - [ ] 0x13: RegisterFlush
- [ ] Extend cmd #4 (GetDocByNum #2):
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
