# TODO

## &hellip;
- [ ] Fiscal-CS Activity Diagram
- [ ] Extend cmd #2 (GetDocByNum #2 (&times;2&hellip;6)):
  - [ ]  ~~3: Receipt (5.3)~~
  - [ ]  6: FSCloseRpt (5.6?)
  - [ ] 21: SattleRpt (5.7)
  - [ ] 31: CorReceipt
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
- [ ] FR: State diagramm
- [ ] Maybe: flag._Flags: metaclass

## CLI:
- get_something
- set_something
- fs (register/close)
- session
- receipt
- corr_receipt
- report
- archive
- reset
