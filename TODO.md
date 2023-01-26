# TODO

## &hellip;
- [ ] RspX.str => str(splitter: str = ', ')
- [ ] Fiscal-CS Activity Diagram
- [ ] Extend commands #2:
  + [ ] Set
  + [ ] GetDocByNum #2 (&times;2&hellip;6)
    - [ ]  3: Receipt (5.3)
    - [ ]  6: FSCloseRpt (5.6?)
    - [ ] 21: SattleRpt (5.7)
    - [ ] 31: CorReceipt
    - [ ]  4: BSO
    - [ ] 41: CorBSO
    - [ ]  7: OpConfirm
  + [ ] Sequences
- [ ] Mk online tests (w/ live FRs)
- [ ] Async
- [ ] Wrap exceptions (all => `exc.Kit&hellip(e)`)
- [ ] Packaging (`requirements.txt`, `setup.{py,cfg}`, `kitfr.spec`, `?MANIFEST.in`, `?tox.*`)
- [ ] Try: 2+ &times; Cmd (sequence) @ 1 connection
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
