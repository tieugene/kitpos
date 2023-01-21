# Notes

## Levels
1. Ph:
  - Desc: L1 (Ph lvl): IP tx/rx
  - In: frame: bytes
  - Out: IP msg
  - Return: rsp frame: bytes
1. Connection:
  - Desc: Implements connection
  - In: bytes
  - Out: bytes
  - Return: connection
1. Logical:
  - Desc: L2 (logical lvl): [De]Packaging bytes into frames
  - In: payload: bytes
  - Out: frame (START, ..., CRC): bytes
  - Ret: refined rsp: bytes
1. Cmd:
  - Desc: Serialize cmd
  - In: cmd: object
  - Out: marshalled cmd: bytes
  - Ret: rsp: object
1. Sequence:
  - Desc: Execute cmd sequence (== operation)
  - In: Operation: object
  - Out: commands: List[cmd]
  - Ret: rsp payload: object

## Test data:

raw = b'\xB6\x29\x00\x05\x30\x01\x00\x00\x00\x95\xС8'
- b'\xB6\x29': header
- b'\x00\x05': LEN=5
- b'\x30': CMD (find FD by number)
- b'\x01\x00\x00\x00': DATA (number = 1)
- b'\x95\xС8': CRC (0xC895) of [LEN..DATA]

## QA
Q: Can I send 2+ commands per connection?
A: Standalone - no, sequences - &hellip;
