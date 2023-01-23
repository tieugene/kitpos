"""`rsp.py` tests."""

from kitfr import const, rsp
from tests.samples import RAW_A


def __x(i: int) -> bytes:
    """Extract frame payload for RspX.from_bytes()."""
    # return util.frame2bytes(RAW_A[i])[1:]
    return RAW_A[i][5:-2]


def test_rsp_get_device_status():
    cls = rsp.RspGetDeviceStatus
    assert cls.from_bytes(__x(0)) == cls(
        sn='550101006105',
        datime=rsp.dt_from_ints((23, 1, 21, 18, 1)),
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
        datime=rsp.dt_from_ints((22, 4, 18, 12, 41)),
        sn='9999078902003867',
        last_doc_no=10
    )


def test_frame2rsp():  # TODO: on err returns
    cls_list = (const.IEnumCmd.GetDeviceStatus, const.IEnumCmd.GetDeviceModel, const.IEnumCmd.GetStorageStatus)
    for i, c in enumerate(cls_list):
        ok, o = rsp.frame2rsp(c, RAW_A[i])
        assert ok
