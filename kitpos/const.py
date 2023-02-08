"""Constants."""
# 1. std
import enum


FRAME_HEADER = b'\xB6\x29'


@enum.unique
class _IEnumPrintable(enum.IntEnum):
    def __str__(self):
        return f"{self.name}({self.value})"


@enum.unique
class IEnumCmd(enum.IntEnum):
    """Commands."""

    GET_POS_STATUS = 0x01       # ✓ [Info] Get status
    GET_POS_MODEL = 0x04        # ✓ [Info]
    GET_FS_STATUS = 0x08        # ✓ [Info]
    GET_REG_PARMS = 0x0A        # ✓ [Info] (not used in C#)
    DOC_CANCEL = 0x10           # ✓ [RegFS]
    RCP_AUTOMAT = 0x1F          # … [Receipt]
    GET_CUR_SES = 0x20          # ✓ [Session]
    SES_OPEN_BEGIN = 0x21       # ✓ [Session]
    SES_OPEN_COMMIT = 0x22      # ✓ [Session]
    RCP_BEGIN = 0x23            # … [Receipt]
    RCP_COMMIT = 0x24           # … [Receipt]
    COR_RCP_BEGIN = 0x25        # ✓ [CorRcpt]
    COR_RCP_COMMIT = 0x26       # ✓ [CorRcpt]
    SES_CLOSE_BEGIN = 0x29      # ✓ [Session]
    SES_CLOSE_COMMIT = 0x2A     # ✓ [Session]
    RCP_ITEM = 0x2B             # … [Receipt]
    # RCP_AGENT = 0x2C          # … [Receipt] (not used in C#)
    RCP_PAYMENT = 0x2D          # … [Receipt]
    COR_RCP_DATA = 0x2E         # ✓ [CorRcpt]
    GET_DOC_INFO = 0x30         # ✓ [Archive]
    GET_DOC_DATA = 0x3A         # … [Info]
    COR_RCP_AUTOMAT = 0x3F      # ✓ [CorRcpt]
    # RESET_MGM = 0x40
    GET_OFD_XCHG_STATUS = 0x50  # ✓ [Info]
    SET_DATETIME = 0x72         # ✓ [Settings]
    GET_DATETIME = 0x73         # ✓ [Settings] (not used in C#)
    RESTART = 0xEF


TAGS_UNKNOWN = {  # not documented
    1001, 1002, 1012, 1013, 1018, 1020, 1037, 1038, 1040, 1041,
    1042, 1043, 1050, 1051, 1052, 1053, 1054, 1056, 1060, 1062,
    1077, 1097, 1098, 1108, 1109, 1110, 1111, 1118, 1188, 1189,
    1209, 1221
}


@enum.unique
class IEnumTag(_IEnumPrintable):
    """Tags."""

    TAG_1008 = 1008    # str[..64], Customer email
    TAG_1009 = 1009    # str[..164], POS address
    TAG_1017 = 1017    # ! str[12], OFD INN
    TAG_1021 = 1021    # ! str[..64] Authorized person's FIO (reg, session, receipt)
    TAG_1023 = 1023    # FVLN, Subj number
    TAG_1030 = 1030    # str[..128], Subj name
    TAG_1031 = 1031    # ! VLN, Payment as cash (kop)
    TAG_1036 = 1036    # ! str[..21], Automatic sale device numer (mandatory for Termainal-FA)
    TAG_1046 = 1046    # ! str[..64], OFD name
    TAG_1048 = 1048    # ! str[..128], User name
    TAG_1055 = 1055    # ! byte[1], Tax mode (addon 7)
    TAG_1059 = 1059    # STLV (!), includes other
    TAG_1079 = 1079    # VLN, Subj price
    TAG_1081 = 1081    # ! VLN, Payment as cashless (kop)
    TAG_1102 = 1102    # ! VLN, Base sum for VAT 18%
    TAG_1103 = 1103    # ! VLN, Base sum for VAT 10%
    TAG_1104 = 1104    # ! VLN, Base sum for VAT 0%
    TAG_1105 = 1105    # ! VLN, Base sum w/o VAT
    TAG_1106 = 1106    # ! VLN, Base sum for VAT 18/118
    TAG_1107 = 1107    # ! VLN, Base sum for VAT 10/110
    TAG_1117 = 1117    # str[..64], Sender email
    TAG_1173 = 1173    # ! byte[1] = 0/1, Correction type
    TAG_1174 = 1174    # ! STLV(1177,1178,1179)
    TAG_1177 = 1177    # str[..255]
    TAG_1178 = 1178    # Unixtime(y,d,m[,h])
    TAG_1179 = 1179    # str[..32]
    TAG_1187 = 1187    # str[..64], POS place
    TAG_1192 = 1192    # str[..16]
    TAG_1199 = 1199    # bytes[1], Subj VAT (1-6, addon 4)
    TAG_1203 = 1203    # str[12] Authorized person's INN (reg, session, receipt)
    TAG_1212 = 1212    # bytes[1], optional (1-19, addon 4)
    TAG_1214 = 1214    # bytes[1] (1-7, addon 4)
    TAG_1215 = 1215    # ! VLN, PrePayment (kop)
    TAG_1216 = 1216    # ! VLN, PostPayment (kop)
    TAG_1217 = 1217    # ! VLN, Counter provosion (kop)
    # Mode = 9999      # byte[1] bitmap flags (addon 7); Note: Terminal-FA always stay auto
    # TAG_30000 = 30000  # byte[5], DateTime


@enum.unique
class IEnumPrnStatus(_IEnumPrintable):
    """Printing device status.

    Used:
    - ...
    """

    OK = 0
    OFFLINE = 1  # Prn device is not connected
    NO_PAPER = 2  # Out of paper
    PAPER_JAM = 3
    COVER_OPENED = 5
    CUT_ERR = 6
    HW_ERR = 7


@enum.unique
class IEnumFSphase(_IEnumPrintable):
    """FS live phase.

    Used:
    - ...
    """

    FAIL = 0   # Impossible, but...
    READY = 1  # Ready for fiscalization
    FISC = 3   # Fiscalization mode
    POST = 7   # Post-fiscal mode (sending FD to OFD)
    ARCH = 5   # Reading data from archive


@enum.unique
class IEnumFSCurDoc(_IEnumPrintable):
    """FS current document type.

    Used:
    - ...
    """

    EMPTY = 0x00
    REG_RPT = 0x01  # FR registration report
    SES_OPEN_RPT = 0x02  # Session opening report
    RECEIPT = 0x04
    SES_CLOSE_RPT = 0x08  # Session closing report
    FS_CLOSE_RPT = 0x10  # Fiscal mode close report
    FS_CHG_RPT = 0x12  # Re-registration due FS replacing report
    RE_REG_RPT = 0x13  # Reregistration report
    COR_RECEIPT = 0x14  # Corr. receipt
    SATTLE_RPT = 0x17  # Sattlement report


@enum.unique
class IEnumADocType(_IEnumPrintable):
    """Archive document types.

    Used:
    - RspGetDocInfo
    """

    REG_RPT = 1  # FR registration report
    RE_REG_RPT = 11  # Reregistration report
    SES_OPEN_RPT = 2  # Session opening report
    SATTLE_RPT = 21  # Sattlement report
    RECEIPT = 3
    COR_RECEIPT = 31  # Corr. receipt
    BSO = 4
    COR_BSO = 41
    SES_CLOSE_RPT = 5  # Session closing report
    FS_CLOSE_RPT = 6  # Fiscal mode close report
    OP_CONFIRM = 7  # Operator's confirmation


@enum.unique
class IEnumReRegReason(_IEnumPrintable):
    """Reason for reregistration."""

    FS = enum.auto()  # Changing FS
    OFD = enum.auto()  # Changing OFD
    USER = enum.auto()  # Changing user's requisitions
    FR = enum.auto()  # Changing FR settings (OFD INN + place/user)


@enum.unique
class IEnumReceiptType(_IEnumPrintable):
    """Receipt type (tag 1199)."""

    IN = enum.auto()  # Incoming
    IN_RET = enum.auto()  # Incoming return
    OUT = enum.auto()  # Outcome
    OUT_RET = enum.auto()  # Outcom return


@enum.unique
class IEnumVAT(_IEnumPrintable):
    """VAT type."""

    VAT_20 = enum.auto()
    VAT_10 = enum.auto()
    VAT_1_6 = enum.auto()
    VAT_1_11 = enum.auto()
    VAT_0 = enum.auto()
    NO_VAT = enum.auto()


class IFlagFSErr(enum.IntFlag):
    """FS errors and warnings.

    Used:
    - flag.FSErr > 0x...
    """

    EXP_3 = 1  # Expired 3 days
    EXP_MON = 2  # Expired 30 days
    FULL_90 = 4  # FS filled upt to 90%
    TIMEOUT = 8  # OFD timeout
    CRIT_ERR = 0x80  # Critical error


class IFlagFRMode(enum.IntFlag):
    """FR working mode.

    Used:
    - flag.FRModes > 0x...
    """

    ENC = enum.auto()  # Encryption
    ALONE = enum.auto()  # Autonomous mode
    AUTO = enum.auto()  # Automatic mode
    SRV = enum.auto()  # Service sector
    BSO = enum.auto()  # BSO(1)/Receipt(0) mode
    INET = enum.auto()  # FR is Internet device


class IFlagTax(enum.IntFlag):
    """Tax type."""

    GENERAL = enum.auto()
    USN = enum.auto()
    USN_DELTA = enum.auto()
    ENVD = enum.auto()
    ESD = enum.auto()
    PSN = enum.auto()


class IFlagAgent(enum.IntFlag):
    """Agent types."""

    MODE_0 = enum.auto()
    MODE_1 = enum.auto()
    MODE_2 = enum.auto()
    MODE_3 = enum.auto()
    MODE_4 = enum.auto()
    MODE_5 = enum.auto()
