#!/usr/bin/env python3
"""Main CLI module."""
# 1. std
# 3. local
from kitfr import cmd, util, const

# x. const
RAW_Q = (  # raw commands
    'B6290001018CEF',  # 0x01: GetDeviceStatus
    'B62900010429BF',  # 0x04: GetDeviceModel
    'B629000108A57E',  # 0x08: GetStorageStatus
    'B6290005300100000095C8',  # 0x30: GetDocByNum(1)
)
RAW_A = (  # raw responses
    #    len.ok<..........................................>crc.
    'B62900170035353031303130303631303517011512010000010300D9B8',
    # 'B62900170035353031303130303631303517011512040000010300D8FB'
    # 'B629001700353530313031303036313035170115113500000103007649'
    # 'B629001700353530313031303036313035170115120F00000103007A38'
    'B629000C005465726D696E616C2D46412D01',
    'B629001F0003000001081604120C29393939393037383930323030333836370A0000008749',
    'B629003200010016031C092901000000874096FE3738303631393732373420203030303030303030303030333830343520202020040C6210',
)


def test_cmd():
    """Test cmd => frame conversion."""
    # frame = b2frame(const.IEnumCmd.GetDocByNum, int(1).to_bytes(4, 'little'))
    c = cmd.CmdGetDocByNum(1)
    raw = bytes.fromhex(RAW_Q[3])
    frame: bytes = util.bytes2frame(c.to_bytes())
    print(frame.hex(), frame == raw)
    rsp: bytes = util.frame2bytes(frame)
    print(c.to_bytes().hex(), '=>', rsp.hex())


def test_rsp():
    """Test frame => rsp conversion."""
    for (c, a) in (
            (const.IEnumCmd.GetDeviceStatus, RAW_A[0]),
            (const.IEnumCmd.GetDeviceModel, RAW_A[1]),
            (const.IEnumCmd.GetStorageStatus, RAW_A[2]),
    ):
        ok, rsp = util.frame2rsp(c, bytes.fromhex(a))
        if ok:
            print(rsp)
        else:
            print("Err:", rsp)


def main():
    """CLI."""
    test_cmd()
    test_rsp()


if __name__ == '__main__':
    main()
