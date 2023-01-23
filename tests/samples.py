"""Test samples."""

__raw_q_s = (  # raw commands
    'B6290001018CEF',  # 0x01: GetDeviceStatus
    'B62900010429BF',  # 0x04: GetDeviceModel
    'B629000108A57E',  # 0x08: GetStorageStatus
    'B6290005300100000095C8',  # 0x30: GetDocByNum(1)
)
__raw_a_s = (  # raw responses
    #    len.ok<..........................................>crc.
    'B62900170035353031303130303631303517011512010000010300D9B8',  # 0x01: GetDeviceStatus
    'B629000C005465726D696E616C2D46412D01',  # 0x04: GetDeviceModel
    'B629001F0003000001081604120C29393939393037383930323030333836370A0000008749',  # 0x08: GetStorageStatus
    # 0x30: GetDocByNum(1)
    'B629003200010016031C092901000000874096FE3738303631393732373420203030303030303030303030333830343520202020040C6210',
)
__rsp_s = (  # RspX.from_bytes() inputs
    '30303030303030303030303338303435202020203738303631393732373420200C0440',  # 0x0A: GetRegisterParms
    '02000A000100000016031C0929',  # 0x50: GetOFDXchgStatus
    '307505001701171334',  # 0x73: GetDateTime
)

RAW_Q = [bytes.fromhex(s) for s in __raw_q_s]  # raw commands
RAW_A = [bytes.fromhex(s) for s in __raw_a_s]  # raw responses
RSP = [bytes.fromhex(s) for s in __rsp_s]  # responce objects dumps
