# TODO

- [ ] Fiscal-CS Activity Diagram:
  + [ ] QueueController:
    - [ ] SendTicket 
  + [ ] TerminalProxy:
    - [x] OpenSession()
    - [x] CloseSession()
    - [x] Receipt()
    - [ ] CorrectionReceipt()
- [ ] Extend cmd #2 (GetDocByNum #2):
  - [ ]  6: FSCloseRpt (5.6?)
  - [ ] 21: SattleRpt (5.7)
  - [ ]  4: BSO
  - [ ] 41: CorBSO
  - [ ]  7: OpConfirm
- [ ] Extend cmd #3 (Sequences, (15)):
    + [ ] CancelDoc (1)
    + [ ] Session Open(2)/Close(2)
    + [ ] Receipt (6)
    + [ ] CorrReceipt (4)
+ [ ] Extend cmd #4 (Maintain):
  - [ ] 0x40 ResetMLM
  - [ ] Register
  - [ ] ReRegister
  - [ ] FSClose
- [ ] Mk online tests (w/ live FRs)
- [ ] Async
- [ ] Wrap exceptions (all => `exc.Kit&hellip(e)`)
- [ ] Packaging (`requirements.txt`, `setup.{py,cfg}`, `kitfr.spec`, `?MANIFEST.in`, `?tox.*`)
- [ ] Try: 2+ &times; Cmd (sequence) @ 1 connection

## Maybe
- [ ] FR: State diagramm
- [ ] flag._Flags: metaclass
