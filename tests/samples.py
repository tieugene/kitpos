"""Test samples.

:todo: {class: sample}
"""
# ==== Frames ====
__frame_q_s = (  # raw command (Question) frames
    'B6290001018CEF',  # 0x01: GetDeviceStatus
    'B62900010429BF',  # 0x04: GetDeviceModel
    'B629000108A57E',  # 0x08: GetStorageStatus
    # TODO: GetRegisterParms,  GetOFDXchgStatus, GetDateTime
)
__frame_a_s = (  # raw response (Answer) frames
    #    len.ok<..........................................>crc.
    'B62900170035353031303130303631303517011512010000010300D9B8',  # 0x01: GetDeviceStatus
    'B629000C005465726D696E616C2D46412D01',  # 0x04: GetDeviceModel
    'B629001F0003000001081604120C29393939393037383930323030333836370A0000008749',  # 0x08: GetStorageStatus
    # TODO: GetRegisterParms,  GetOFDXchgStatus, GetDateTime
)
# TODO: convert to __data_*
# TODO: add error response
# ==== Bytes ====
# TODO: __data_q_s
__data_a_s = (  # RspX.from_bytes(data)
    # TODO: GetDeviceStatus, GetDeviceModel, GetStorageStatus
    '30303030303030303030303338303435202020203738303631393732373420200C0440',  # 0x0A: GetRegisterParms
    '02000A000100000016031C0929',  # 0x50: GetOFDXchgStatus
    '307505001701171334',  # 0x73: GetDateTime (TLV; TAG=30000 (UINT16LE); LEN=5 (UINT16LE); TYPE=DATETIME(5))
)
__frame_q_dbn_s = (  # 0x30: GetDocByNum(n).to_bytes() -> data
    'B6290005300100000095C8',  # n=1
    # TODO: add other nums
)
# ---- Bytes.GetDocByNum ----
__data_a_dbn_s = (  # 0x30: RspGetDocByNum(n).from_bytes(data)
    '010016031C092901000000874096FE3738303631393732373420203030303030303030303030333830343520202020040C',
    '020016031C0929020000001259A70B0100',
    '030016031C092F03000000ECC57C69014006000000',
    '05001604120C220400000060C7B7A90100',
    '0B001604120C27080000004CD1A78F3738303631393732373420203030303030303030303030333830343520202020040C04',
)

RAW_Q = [bytes.fromhex(s) for s in __frame_q_s]  # raw commands
RAW_A = [bytes.fromhex(s) for s in __frame_a_s]  # raw responses
RSP = [bytes.fromhex(s) for s in __data_a_s]  # responce objects dumps
RSP_DBN = [bytes.fromhex(s) for s in __data_a_dbn_s]  # RspGetDocByNum.from_bytes(data)
