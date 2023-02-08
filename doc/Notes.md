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


## Tags used:
1009, 1021, 1023, 1030, 1031, 1036, 1055, 1059, 1079, 1081,
1103, 1104, 1105, 1106, 1107, 1173, 1174, 1177, 1178, 1179,
1187, 1192, 1199, 1203, 1212, 1214, 1215, 1216, 1217, 30000

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

- Q: Can I send tags in any orders?
- A: &hellip;

- Q: What about full tag list?
- A: N/a (`TerminalFAUtility.exe` not helps)

## Live tests

### CorrReceipt:
1. SessionOpenBegin 1
2. SessionOpenCommit
3. CorrReceiptBegin
4. CorrReceiptData <2E.json>
5. CorrReceiptAutomat <3F.json>
6. CorrReceiptCommit <26.json>
7. SessionCloseBegin 1
8. SessionCloseCommit

### Receipt:
1. SessionOpenBegin 1
2. SessionOpenCommit
3. ReceiptBegin
4. ReceiptItem <2B.json>
5. ReceiptAutomat <1F.json> (!)
6. ReceiptPayment <2D.json>
7. ReceiptCommit <24.json>
8. SessionCloseBegin 1
9. SessionCloseCommit
