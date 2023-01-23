# TODO

- [x] Try:
  + [x] Raw send/get
  + [x] Test 2+ &times; Cmd (standalones)
  + [x] crc:
    - [x] ~~std: hashlib, binascii, zlib~~
    - [x] [crcmod](https://crcmod.sourceforge.net)
    - [x] [~~crcelk~~](https://github.com/zeroSteiner/crcelk/) *(no need yet)*
  + [ ] Test 2+ &times; Cmd (sequence)
- [x] Core:
  + [x] util &times;2
  + [x] cmd &times;4
  + [x] rsp &times;4:
- [x] Tests
  + [x] util &times;2
  + [x] cmd &times;4
  + [x] rsp &times;4
- [x] CLI:
  + [x] rsp.RspX.__str__()  &times;3
  + [x] err_strings
- [ ] Extend commands to:
  + [ ] Get
  + [ ] Set
  + [ ] Sequences
- [ ] Expand RespX flag (bit array) attributes
- [ ] Async
- [ ] Packaging (`requirements.txt`, `setup.{py,cfg}`, `kitfr.spec`, `?MANIFEST.in`, `?tox.*`)

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
