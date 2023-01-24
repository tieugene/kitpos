"""Test samples.

:todo: {class: sample}
"""

__frame_q_s = (  # raw command (Question) frames
    'B6290001018CEF',  # 0x01: GetDeviceStatus
    'B62900010429BF',  # 0x04: GetDeviceModel
    'B629000108A57E',  # 0x08: GetStorageStatus
)
__frame_a_s = (  # raw response (Answer) frames
    #    len.ok<..........................................>crc.
    'B62900170035353031303130303631303517011512010000010300D9B8',  # 0x01: GetDeviceStatus
    'B629000C005465726D696E616C2D46412D01',  # 0x04: GetDeviceModel
    'B629001F0003000001081604120C29393939393037383930323030333836370A0000008749',  # 0x08: GetStorageStatus
)
# TODO: __data_q_s
__data_a_s = (  # RspX.from_bytes(data)
    '30303030303030303030303338303435202020203738303631393732373420200C0440',  # 0x0A: GetRegisterParms
    '02000A000100000016031C0929',  # 0x50: GetOFDXchgStatus
    '307505001701171334',  # 0x73: GetDateTime (TLV; TAG=30000 (UINT16LE); LEN=5 (UINT16LE); TYPE=DATETIME(5))
)
__data_q_dbn_s = (  # 0x30: GetDocByNum(n).to_bytes() -> data
    'B6290005300100000095C8',  # n=1
)
__data_a_dbn_s = (  # 0x30: RspGetDocByNum(n).from_bytes(data)
    '010016031C092901000000874096FE3738303631393732373420203030303030303030303030333830343520202020040C',  # n=1 (49)
    '020016031C0929020000001259A70B0100',  # n=2 (17)
    '030016031C092F03000000ECC57C69014006000000',  # n=3 (21)
    '05001604120C220400000060C7B7A90100',  # n=4
    '02001604120C23050000009F27E2610200',  # n=5
    '03001604120C2506000000F621AA62014006000000',  # n=6
    '05001604120C27070000003BE1DB5E0200',  # n=7
    '0B001604120C27080000004CD1A78F3738303631393732373420203030303030303030303030333830343520202020040C04',  # n=8
    '02001604120C28090000003BA48DCA0300',  # n=9
    '03001604120C290A0000002E6A320E014006000000',  # n=10
)

RAW_Q = [bytes.fromhex(s) for s in __frame_q_s]  # raw commands
RAW_A = [bytes.fromhex(s) for s in __frame_a_s]  # raw responses
RSP = [bytes.fromhex(s) for s in __data_a_s]  # responce objects dumps
RSP_DBN = [bytes.fromhex(s) for s in __data_a_dbn_s]  # RspGetDocByNum.from_bytes(data)
