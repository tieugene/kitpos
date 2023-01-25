# TODO

- [ ] Extend commands:
  + [ ] #2:
    - [ ] GetDocByNum #2 (&times;2&hellip;6)
      + [ ] 21: SattleRpt (5.7)
      + [ ]  3: Receipt (5.3)
      + [ ] 31: CorReceipt
      + [ ]  4: BSO
      + [ ] 41: CorBSO
      + [ ]  6: FSCloseRpt (5.6?)
      + [ ]  7: OpConfirm
    - [ ] Set
    - [ ] Sequences
- [ ] FIXME: Sometimes receives just \xB6\x29 and nothing else
- [ ] Expand RespX flag (bit array) attributes:
  + [x] 0x01 (2)
  + […] 0x08 (3)
  + [ ] 0x0A (3)
  + [ ] 0x30 (1+): &hellip;
- [ ] Online tests
- [ ] Async
- [ ] Packaging (`requirements.txt`, `setup.{py,cfg}`, `kitfr.spec`, `?MANIFEST.in`, `?tox.*`)
- [ ] Try:
  + [ ] 2+ &times; Cmd (sequence) @ 1 connection

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
