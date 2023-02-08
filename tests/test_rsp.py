"""`rsp.py` tests."""
# 1. std
import datetime

import kitpos.util
# 3. local
from kitpos import const, rsp
from tests.samples import RAW_A, RSP


def __x(i: int) -> bytes:
    """Extract frame payload for RspX.from_bytes()."""
    # return util.frame2bytes(RAW_A[i])[1:]
    return RAW_A[i][5:-2]


def test_rsp_get_device_status():
    cls = rsp.RspGetDeviceStatus
    assert cls.from_bytes(__x(0)) == cls(
        sn='550101006105',
        datime=kitpos.util.b2dt((23, 1, 21, 18, 1)),
        err=0,
        status=0,
        is_fs=True,
        phase=3,
        wtf=0
    )


def test_rsp_get_device_model():
    cls = rsp.RspGetDeviceModel
    assert cls.from_bytes(__x(1)) == cls(
        name='Terminal-FA'
    )


def test_rsp_get_storage_status():
    cls = rsp.RspGetStorageStatus
    assert cls.from_bytes(__x(2)) == cls(
        phase=3,
        cur_doc=0,
        is_doc=False,
        is_session_open=True,
        flags=8,
        datime=kitpos.util.b2dt((22, 4, 18, 12, 41)),
        sn='9999078902003867',
        last_doc_no=10
    )


def test_rsp_get_register_params():
    cls = rsp.RspGetRegisterParms
    assert cls.from_bytes(__x(3)) == cls(
        rn='0000000000038045',
        inn='7806197274',
        mode=12,
        tax=4,
        agent=64
    )


def test_rsp_get_ofd_xchg_status():
    cls = rsp.RspGetOFDXchgStatus
    assert cls.from_bytes(__x(4)) == cls(
        status=2,
        state_ofd=0,
        out_count=10,
        next_doc_n=1,
        next_doc_d=datetime.datetime(2022, 3, 28, 9, 41)
    )


def test_rsp_get_date_time():
    cls = rsp.RspGetDateTime
    assert cls.from_bytes(__x(5)) == cls(
        datime=datetime.datetime(2023, 1, 24, 14, 46)
    )

# TODO: RspGetDocInfo


def test_bytes2rsp():
    cls_list = (
        const.IEnumCmd.GET_POS_STATUS,
        const.IEnumCmd.GET_POS_MODEL,
        const.IEnumCmd.GET_FS_STATUS,
        const.IEnumCmd.GET_REG_PARMS,
        const.IEnumCmd.GET_OFD_XCHG_STATUS,
        const.IEnumCmd.SET_DATETIME,
        const.IEnumCmd.GET_DATETIME,
    )
    for i, c in enumerate(cls_list):
        assert rsp.bytes2rsp(c, RSP[i]) is not None  # compare type

# TODO: add errors
