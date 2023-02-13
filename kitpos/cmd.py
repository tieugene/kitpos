"""Commands to send.

Copyright 2023 TI_Eugene <ti.eugene@gmail.com>
This file is part of the kitpos project.
You may use this file under the terms of the GPLv3 license.
"""
# pylint: disable=R0903
# 1. std
from typing import Optional, Iterable
import datetime
# 3. local
from kitpos import const, util, tag, exc


class _CmdBase:
    """Base for commands."""

    cmd_id: const.IEnumCmd

    @staticmethod
    def _chk_tags(payload: tag.TagDict, tags_required: Iterable[int], tags_optional: Iterable[int] = ()):
        """Check given payload on consistency (no less, no more)."""
        # step #1: All required tags shipped
        for __tag in tags_required:
            if __tag not in payload:
                raise exc.KpeCmdInit(f"Required tag '{__tag}' not found in given data.")
        # step #2: No one shipped tag excess
        __tag_set = set(tags_required).union(set(tags_optional))
        for __tag in payload.keys():
            if __tag.value not in __tag_set:
                raise exc.KpeCmdInit(f"Extra tag '{__tag.value}' in given data.")

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return util.ui2b1(self.cmd_id.value)


class CmdGetDeviceStatus(_CmdBase):
    """0x01: Get POS status."""

    cmd_id = const.IEnumCmd.GET_POS_STATUS


class CmdGetDeviceModel(_CmdBase):
    """0x04: Get POS model."""

    cmd_id = const.IEnumCmd.GET_POS_MODEL


class CmdGetStorageStatus(_CmdBase):
    """0x08: Get FS status."""

    cmd_id = const.IEnumCmd.GET_FS_STATUS


class CmdGetRegisterParms(_CmdBase):
    """0x0A: Get POS/FS registering parameters."""

    cmd_id = const.IEnumCmd.GET_REG_PARMS


class CmdDocCancel(_CmdBase):
    """0x10: Cancel any opened document."""

    cmd_id = const.IEnumCmd.DOC_CANCEL


class CmdGetCurSession(_CmdBase):
    """0x20: Get current session params."""

    cmd_id = const.IEnumCmd.GET_CUR_SES


class _CmdSessionAnyBegin(_CmdBase):
    """Base for CmdSessionOpenBegin/CmdSessioCloseBegin."""

    skip_prn: Optional[bool]  # Skip printing report (None = False)

    def __init__(self, skip_prn: Optional[bool] = None):
        super().__init__()
        self.skip_prn = skip_prn

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        retvalue = super().to_bytes()
        if self.skip_prn is not None:
            retvalue += util.l2b(self.skip_prn)
        return retvalue


class CmdSessionOpenBegin(_CmdSessionAnyBegin):
    """0x21: Begin opening session."""

    cmd_id = const.IEnumCmd.SES_OPEN_BEGIN


class CmdSessionOpenCommit(_CmdBase):
    """0x22: Commit opening session."""

    cmd_id = const.IEnumCmd.SES_OPEN_COMMIT


class CmdSessionCloseBegin(_CmdSessionAnyBegin):
    """0x29: Begin closing session."""

    cmd_id = const.IEnumCmd.SES_CLOSE_BEGIN


class CmdSessionCloseCommit(_CmdBase):
    """0x2A: Commit opening session."""

    cmd_id = const.IEnumCmd.SES_CLOSE_COMMIT


class _CmdGetDocAny(_CmdBase):
    """Base CmdGetDocInfo/CmdGetDocData."""

    num: int

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + util.ui2b4(self.num)


class CmdGetDocInfo(_CmdGetDocAny):
    """0x30: Find document by its number."""

    cmd_id = const.IEnumCmd.GET_DOC_INFO


class CmdGetDocData(_CmdGetDocAny):
    """0x3A: Read document content."""

    cmd_id = const.IEnumCmd.GET_DOC_DATA


class CmdGetOFDXchgStatus(_CmdBase):
    """0x50: Get OFD exchange status."""

    cmd_id = const.IEnumCmd.GET_OFD_XCHG_STATUS


class CmdSetDateTime(_CmdBase):
    """0x72: Set POS date/time."""

    cmd_id = const.IEnumCmd.SET_DATETIME
    datime: datetime.datetime

    def __init__(self, datime: datetime.datetime):
        """Make CmdSetDateTime object.

        :param datime: Date/time to set.
        """
        super().__init__()
        self.datime = datime

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tag_pack(const.IEnumTag.TAG_30000, util.dt2b5(self.datime))


class CmdGetDateTime(_CmdBase):
    """0x73: Get POS date/time."""

    cmd_id = const.IEnumCmd.GET_DATETIME


class CmdCorrReceiptBegin(_CmdBase):
    """0x25: Corr. Receipt. Step #1/4 - begin.

    Response: RspOK
    """

    cmd_id = const.IEnumCmd.COR_RCP_BEGIN


class CmdCorrReceiptData(_CmdBase):
    """0x2E: Corr. Receipt. Step #2/4 - send data.

    Response: RspOK
    """

    __tags = (1021, 1203, 1173, 1055, 1031, 1081, 1215, 1216, 1217, 1102, 1103, 1104, 1105, 1106, 1107, 1174)
    cmd_id = const.IEnumCmd.COR_RCP_DATA
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        """Make CmdCorrReceiptData object.

        :param payload: Dict of tag-value pairs.
        """
        super().__init__()
        self._chk_tags(payload, self.__tags)
        # TODO: chk 1031+1081+1215+1216+1217 == sum(1102..1107)
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tagdict_pack(self.payload)


class CmdCorrReceiptAutomat(_CmdBase):
    """0x3F: Corr. Receipt. Step #3/4 - send automat number.

    Response: RspOK
    """

    __tags = (1009, 1187, 1036)
    cmd_id = const.IEnumCmd.COR_RCP_AUTOMAT
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        """Make CmdCorrReceiptAutomat object.

        :param payload: Dict of tag-value pairs.
        """
        super().__init__()
        self._chk_tags(payload, self.__tags)
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tagdict_pack(self.payload)


class CmdCorrReceiptCommit(_CmdBase):
    """0x26: Corr. Receipt. Step #4/4 - commit.

    Response: RspCorrReceiptCommit
    """

    cmd_id = const.IEnumCmd.COR_RCP_COMMIT
    req_type: const.IEnumReceiptType
    total: int

    def __init__(self, req_type: const.IEnumReceiptType, total: int):
        """Make CmdCorrReceiptCommit object.

        :param req_type: Corr. receipt type (enum)
        :param total: Total of corr. receipt items prices.
        """
        super().__init__()
        self.req_type = req_type
        self.total = total

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + util.ui2b1(self.req_type) + util.ui2vln(self.total)


# noinspection DuplicatedCode
class CmdReceiptBegin(_CmdBase):
    """0x23: Receipt. Step #1/6 - begin.

    Response: RspOK
    """

    cmd_id = const.IEnumCmd.RCP_BEGIN


class CmdReceiptItem(_CmdBase):
    """0x2B: Receipt. Step #2/6 - send item.

    Response: RspOK
    """

    __1059_tags = (1030, 1079, 1023, 1199, 1214, 1212)
    cmd_id = const.IEnumCmd.RCP_ITEM
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        """Make CmdReceiptItem object.

        :param payload: Dict of tag-value pairs.
        """
        super().__init__()
        if not (len(payload) == 1 and const.IEnumTag.TAG_1059 in payload):
            raise exc.KpeCmdInit("The only '1059' tag required.")
        self._chk_tags(payload[const.IEnumTag.TAG_1059], self.__1059_tags)
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tagdict_pack(self.payload)


class CmdReceiptAutomat(_CmdBase):
    """0x1F: Receipt. Step #4/6 - send automat number.

    Response: RspOK
    """

    __tags = (1009, 1187, 1036)
    cmd_id = const.IEnumCmd.RCP_AUTOMAT
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        """Make CmdReceiptAutomat object.

        :param payload: Dict of tag-value pairs.
        """
        super().__init__()
        self._chk_tags(payload, self.__tags)
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tagdict_pack(self.payload)


class CmdReceiptPayment(_CmdBase):
    """0x2D: Receipt. Step #5/6 - send payment details.

    Response: RspOK
    """

    __tags = (1055, 1031, 1081, 1215, 1216, 1217)
    __opts = (1021, 1203, 1008, 1192)  # ... 1228, 1227, 1085, 1086
    cmd_id = const.IEnumCmd.RCP_PAYMENT
    payload: tag.TagDict

    def __init__(self, payload: tag.TagDict):
        """Make CmdReceiptPayment object.

        :param payload: Dict of tag-value pairs.
        """
        super().__init__()
        self._chk_tags(payload, self.__tags, self.__opts)
        self.payload = payload

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        return super().to_bytes() + tag.tagdict_pack(self.payload)


class CmdReceiptCommit(_CmdBase):
    """0x24: Receipt. Step #6/6 - commit.

    Response: RspReceiptCommit
    """

    cmd_id = const.IEnumCmd.RCP_COMMIT
    req_type: const.IEnumReceiptType
    total: int
    notes: Optional[str]

    def __init__(self, req_type: const.IEnumReceiptType, total: int, notes: Optional[str]):
        """Create CmdReceiptCommit object.

        :param req_type: Receipt type (enum)
        :param total: Total of receipt items prices.
        :param notes: Subj.
        """
        super().__init__()
        self.req_type = req_type
        self.total = total
        self.notes = notes

    def to_bytes(self) -> bytes:
        """Serialize to bytes."""
        retvalue = super().to_bytes() + util.ui2b1(self.req_type) + util.ui2b_n(self.total, 5)
        if self.notes:
            retvalue += util.s2b(self.notes)
        return retvalue
