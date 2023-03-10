"""`cmd.py` tests."""

from kitpos import util, cmd
from tests.samples import RAW_Q


def test_cmd_get_device_status():
    assert util.frame_pack(cmd.CmdGetDeviceStatus().to_bytes()) == RAW_Q[0]


def test_cmd_get_device_model():
    assert util.frame_pack(cmd.CmdGetDeviceModel().to_bytes()) == RAW_Q[1]


def test_cmd_get_storage_status():
    assert util.frame_pack(cmd.CmdGetStorageStatus().to_bytes()) == RAW_Q[2]


def test_cmd_get_register_params():
    assert util.frame_pack(cmd.CmdGetRegisterParms().to_bytes()) == RAW_Q[3]


def test_cmd_get_ofd_xchg_status():
    assert util.frame_pack(cmd.CmdGetOFDXchgStatus().to_bytes()) == RAW_Q[4]


def test_cmd_get_date_time():
    assert util.frame_pack(cmd.CmdGetDateTime().to_bytes()) == RAW_Q[5]


# def test_cmd_get_doc_by_num():
#    assert util.frame_pack(cmd.CmdGetDocInfo(1).to_bytes()) == RAW_Q[3]

# TODO: err
