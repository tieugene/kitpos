"""Test samples.

:todo: {class: sample}
"""
# ==== Frames ====
__frame_q_s = (  # raw command (Question) frames
    'B6290001018CEF',    # 0x01: GET_POS_STATUS
    'B62900010429BF',    # 0x04: GET_POS_MODEL
    'B629000108A57E',    # 0x08: GET_FS_STATUS
    'B62900010AE75E',    # 0x0A: GET_REG_PARMS
    'B6290001109CED',    # 0x10: DOC_CANCEL
    'B629000120CFDB',    # 0x20: GET_CUR_SES
    'B6290002210156CF',  # 0x21: SES_OPEN_BEGIN(1)
    'B6290001228DFB',    # 0x22: SES_OPEN_COMMIT
    'B62900022901FF46',  # 0x29: SES_CLOSE_BEGIN(1)
    'B62900012A857A',    # 0x2A: SES_CLOSE_COMMIT
    'B62900015058A5',    # 0x50: GET_OFD_XCHG_STATUS
    'B62900017359B1'     # 0x73: GET_DATETIME
)
__frame_a_s = (  # raw response (Answer) frames; TODO: add const.IEnumCmd entries
    #    len.ok<..........................................>crc.
    'B62900170035353031303130303631303517011512010000010300D9B8',  # 0x01: GET_POS_STATUS
    'B629000C005465726D696E616C2D46412D01',  # 0x04: GET_POS_MODEL
    'B629001F0003000001081604120C29393939393037383930323030333836370A0000008749',  # 0x08: GET_FS_STATUS
    'B62900240030303030303030303030303338303435202020203738303631393732373420200C044037EB',  # 0x0A: GET_REG_PARMS
    'B62901B40011041000393939393037383930323030333836370D0414003030303030303030303130343537383220202020FA'
    '030C003437303530323137343420201004040001000000F4030400045DD1633504060021045677B60D2004010000EA030100'
    '00E9030100015504010001560401000054040100002604010001180435008EA1E9A5E1E2A2AE20E120AEA3E0A0ADA8E7A5AD'
    'ADAEA920AEE2A2A5E2E1E2A2A5ADADAEE1E2ECEE202292E0A0ADE12D81A0ABE222F10356003139353235332C20A32E2091A0'
    'ADAAE22D8FA5E2A5E0A1E3E0A32C20E8AEE1E1A52090A5A2AEABEEE6A8A82C20A42E2035382DA02C208BA8E2A5E0A020802C'
    '20AFAEACA5E9A5ADA8A520318D2C20AFAEAC2E20FC3134A3040900E2E0A0ADE1AFAEE0E2FD03140088A2A0ADAEA22088A2A0'
    'AD2088A2A0ADAEA2A8E7C504010001F9030C00373834313436353139382020160421008E8E8E20228F859285902D91859082'
    '88912091AFA5E6E2A5E5ADAEABAEA3A8A8225D040E006E6F7265706C79406F66642E727524040C007777772E6E616C6F672E'
    '7275B904010002A504010002A404080046412030312E3035F5030C00353530313031303036313035A581'  # 0x3B of 10.15.63.36
    'B629007F0011041000393939393037383930323030363933320D0414003030303030303030303130303534393020202020FA'
    '030C003437313930323430373920201004040001000000F40304006CACDE623504060021042C3B234F2004010000EA030100'
    '00E90301000155040100015604010000540401000026040100034D0401000124A3'  # 0x3B of 10.15.63.70
    'B629011C0011041000393939393037383930323030363439350D0414003030303030303030303030333030323420202020FA'
    '030C003233323031313033333420201004040001000000F40304006C47565F3504060021046145824B2004010000EA030100'
    '00E90301000155040100015604010000540401000026040100011804040092A5E1E2F103040092A5E1E2A304040092A5E1E2'
    'FD03040092A5E1E2C504010001F9030C00373834313436353139382020160421008E8E8E20228F859285902D918590828891'
    '2091AFA5E6E2A5E5ADAEABAEA3A8A8225D040E006E6F7265706C79406F66642E727524040C007777772E6E616C6F672E7275'
    'B904010002A504010002A404080046412030312E3035F5030C00353530313031303131303936D8F5'  # 0x3B of 10.15.63.88
    'B629000E0002000A000100000016031C09292E93',  # 0x50: GET_OFD_XCHG_STATUS
    'B629000100ADFF',  # 0x72: SET_DATETIME
    'B629000A00307505001701180E2E88EA'  # 0x73: GET_DATETIME
)
# TODO: convert to __data_*
# TODO: add error response
# ==== Bytes ====
# TODO: __data_q_s
__data_a_s = (  # RspX.from_bytes(data)
    # TODO: GET_POS_STATUS, GET_POS_MODEL, GET_FS_STATUS
    '30303030303030303030303338303435202020203738303631393732373420200C0440',  # 0x0A: GET_REG_PARMS
    '02000A000100000016031C0929',  # 0x50: GET_OFD_XCHG_STATUS
    '307505001701171334',  # 0x73: GET_DATETIME (TLV; TAG=30000 (UINT16LE); LEN=5 (UINT16LE); TYPE=DATETIME(5))
)
__frame_q_dbn_s = (  # 0x30: GET_DOC_INFO(n).to_bytes() -> data
    'B6290005300100000095C8',  # n=1
    # TODO: add other nums
)
# ---- Bytes.GET_DOC_INFO ----
__data_a_gdi_s = (  # 0x30: RspGetDocInfo(n).from_bytes(data)
    '010016031C092901000000874096FE3738303631393732373420203030303030303030303030333830343520202020040C',  # RegRpt (49)
    '020016031C0929020000001259A70B0100',  # SesOpenRpt (17)
    '030016031C092F03000000ECC57C69014006000000',  # Receipt (21)
    '05001604120C220400000060C7B7A90100',  # SesCloseRpt (17)
    '0B001604120C27080000004CD1A78F3738303631393732373420203030303030303030303030333830343520202020040C04',  # ReRegRpt (50)
    '1F0017011A101103000000ACF2D47401800C000000',  # CorReceipt (21)
)
# ---- Bytes.GET_DOC_DATA ----
__data_a_gdd_s = (  # 0x3A: RspGetDocData(n).from_bytes(data)
    # Reg (435)
    '11041000393939393037383930323030333836370D0414003030303030303030303130343537383220202020FA030C003437'
    '303530323137343420201004040001000000F4030400045DD1633504060021045677B60D2004010000EA03010000E9030100'
    '015504010001560401000054040100002604010001180435008EA1E9A5E1E2A2AE20E120AEA3E0A0ADA8E7A5ADADAEA920AE'
    'E2A2A5E2E1E2A2A5ADADAEE1E2ECEE202292E0A0ADE12D81A0ABE222F10356003139353235332C20A32E2091A0ADAAE22D8F'
    'A5E2A5E0A1E3E0A32C20E8AEE1E1A52090A5A2AEABEEE6A8A82C20A42E2035382DA02C208BA8E2A5E0A020802C20AFAEACA5'
    'E9A5ADA8A520318D2C20AFAEAC2E20FC3134A3040900E2E0A0ADE1AFAEE0E2FD03140088A2A0ADAEA22088A2A0AD2088A2A0'
    'ADAEA2A8E7C504010001F9030C00373834313436353139382020160421008E8E8E20228F859285902D9185908288912091AF'
    'A5E6E2A5E5ADAEABAEA3A8A8225D040E006E6F7265706C79406F66642E727524040C007777772E6E616C6F672E7275B90401'
    '0002A504010002A404080046412030312E3035F5030C00353530313031303036313035',
    # Receipt (241)
    '11041000393939393037383930323030363439350D0414003030303030303030303030333030323420202020FA030C003233'
    '32303131303333342020100404000E0D0000F4030400FC79575F3504060031041F7D0F580E0404000700000012040400C400'
    '00001E04010001FC030200280A23043D0006041D0093E1ABE3A3A020AFA0E1E1A0A6A8E0E1AAA8A520AFA5E0A5A2AEA7AAA8'
    '37040200280AFF030200000113040200280AAF04010001BE040100040C040100311F04010001070401000039040200280ABF'
    '04010000C004010000C10401000024040C007777772E6E616C6F672E72754E040200B101B904010002',
    # CorReceipt (251)
    '11041000393939393037383930323030333836370D0414003030303030303030303130343537383220202020FA030C003437'
    '303530323137343420201004040003000000F40304007CA7D26335040600330474D4F2AC0E04040001000000120404000100'
    '00001E04010001FC030200800C9604260099040D00A2EBA4A0E7A020A1A8ABA5E2A09A04040080B8AF629B04090032323032'
    '333031323695040100001F04010001FD03140088A2A0ADAEA22088A2A0AD2088A2A0ADAEA2A8E7070401000039040200800C'
    'BF04010000C004010000C1040100004E040100004F040100005204010000500401000051040200800CB9040100020C04010031',
)

# ==== Public ====
RAW_Q = [bytes.fromhex(s) for s in __frame_q_s]  # raw commands
RAW_A = [bytes.fromhex(s) for s in __frame_a_s]  # raw responses
CMD = [bytes.fromhex(s)[4:-2] for s in __frame_q_s]
RSP = [bytes.fromhex(s)[5:-2] for s in __frame_a_s]  # responce objects dumps
RSP_GDI = [bytes.fromhex(s) for s in __data_a_gdi_s]  # RspGetDocInfo.from_bytes(data)
RSP_GDD = [bytes.fromhex(s) for s in __data_a_gdd_s]  # RspGetDocData.from_bytes(data)

# TODO: add errs
