# Notes

## Levels
1. Ph:
  - Desc: L1 (Ph lvl): IP tx/rx
  - In: frame: bytes
  - Out: IP msg
  - Return: rsp frame: bytes
1. Logical:
  - Desc: L2 (logical lvl): [De]Packaging bytes into frames
  - In: payload: bytes
  - Out: frame (START, ..., CRC): bytes
  - Ret: refined rsp: bytes
1. Cmd/Rsp:
  - Desc: Serialize cmd
  - In: cmd: object
  - Out: marshalled cmd: bytes
  - Ret: rsp: object
1. Sequence:
  - Desc: Execute cmd sequence (== operation)
  - In: Operation: object
  - Out: commands: List[cmd]
  - Ret: rsp payload: object

## Test frame:

raw = b'\xB6\x29\x00\x05\x30\x01\x00\x00\x00\x95\xС8'
- b'\xB6\x29': header
- b'\x00\x05': LEN=5
- b'\x30': CMD (find FD by number)
- b'\x01\x00\x00\x00': DATA (number = 1)
- b'\x95\xС8': CRC (0xC895) of [LEN..DATA]

## ADoc data
- 1: 49 = 2 + 47 (5+4+4+12+20+1+1)  # 5.1
- 2: 17 = 2 + 15 (5+4+4+2)  # 5.4
- 3: 21 = 2 + 19 (5+4+4+1+5)  # 5.3
- 5: 17 = 2 + 15 (5+4+4+2)  # 5.5
- B: 50 = 2 + 48 (5+4+4+12+20+1+1+1)  # 5.2

## Net
- if recv() right after txrx: get header and that's all
- tests:
  + 36: 13 tickets, 10x1000 &check; (32" = 30 ops/s)
  + 77: 56 tickets; 50x1000 &check; (31" = 30 ops/s)
  + 80: 3342 tickets; 3000x2000 &check; (5'20" = 6 ops/s)

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

## QA
- Q: Can I txrx 2+ commands per connection?
- A: Standalone - no, sequences - maybe but not recommended (due timeout)

- Q: Qu'est-ce que ce "фискальный признак"
- A: &sime; checksum

- Q: Receipt or CorReceipt?
- A: Receipt for today's and yesterday's; CorReceipt for earlier

- Q: Can I txrx interlaced commands:
- A: &hellip;

- Q: Can I get 2+ connections?
- A: &hellip;

## CLI tests
```sh
./main.sh 1.1.1.1 7777 CorrReceiptCommit 'json'
```

CorrReceiptData:
```json
{"1021":"auth_fio","1203":"1122334455","1173":false,"1055":1,"1031":5100,"1081":0,"1215":0,"1216":0,"1217":0,"1102":5100,"1103":0,"1104":0,"1105":0,"1106":0,"1107":0,"1174":{"1177":"выдача_билета","1178":"2022-06-01","1179":"12345_20220601"}}
```

CorrReceiptAutomat:
```json
{"1009":"addr","1187":"place","1036":"1"}
```

CorrReceiptCommit:
```json
{"type":1,"total":123}
```
