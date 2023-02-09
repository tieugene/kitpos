# TODO

- [ ] Fixing (0.0.1):
  + [ ] Exceptions (catch, wrap into KitPOS&hellip;)
  + [ ] Tests (&rArr; coverage)
  + […] Logging(`-v`)
  + [ ] Dox
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
  + [ ] `tox.ini`
  + [ ] Async txrx
  + [ ] Multitag
  + [ ] Online tests (w/ live FRs)
- Maybe:
  + POS State diagramm
  + flag._Flags: metaclass
  + Nice exception traceback

## Exceptions:

Wrap underlied exception and/or add text: function name, 

- [x] `net`: `KpeNet`
- [x] `util`: `KpeByte*`, `KpeFrame*`
- [ ] `tag`: `KpeTag*`
  + [ ] `const`: `__init__()`
  + [ ] `flag`: `__init__()`
- [ ] `cmd`: `__init__`, `to_bytes()`
- [ ] `rsp`: `KpeRsp*`
- [ ] `cli`: `KpeCLI` (bad arg (type, value))
