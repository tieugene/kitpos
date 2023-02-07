"""Tags things."""
# 1. std
from typing import Dict, Any, Tuple
import sys
import datetime
# 3. local
from kitpos import const, flag, util

TagDict = Dict[const.IEnumTag, Any]

TAG2FUNC = {  # Tag: (json_2_value, value_2_bytes (pack), bytes_2_value (unpack))
    const.IEnumTag.Tag_1008: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1009: (
        lambda v: v[:164].strip(),
        lambda v: util.s2b(v[:164]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1017: (
        lambda v: v[:12].strip(),
        lambda v: util.s2b(v[:12]).ljust(12),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1021: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1023: (
        lambda v: v,
        lambda v: util.n2fvln(v),
        lambda v: util.fvln2n(v)),  # FVLN; 0x2B
    const.IEnumTag.Tag_1030: (
        lambda v: v[:128].strip(),
        lambda v: util.s2b(v[:128]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1031: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1036: (
        lambda v: v[:21].strip(),
        lambda v: util.s2b(v[:21]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1046: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1048: (
        lambda v: v[:128].strip(),
        lambda v: util.s2b(v[:128]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1055: (
        lambda v: flag.TaxModes(v),  # byte[1] == int
        lambda v: v.b(),
        lambda v: flag.TaxModes(util.b2ui(v))),  # 0x2D, 0x2E; FIXME: .bit_count() == 1
    const.IEnumTag.Tag_1059: (
        lambda v: json2tagdict(v),
        lambda v: tag_dict_pack(v),
        lambda v: tag_list_unpack(v)),  # STLV; recur
    const.IEnumTag.Tag_1079: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1081: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1102: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1103: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1104: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1105: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1106: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1107: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1117: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1173: (
        lambda v: v,
        lambda v: util.l2b(v),
        lambda v: util.b2l(v)),
    const.IEnumTag.Tag_1174: (
        lambda v: json2tagdict(v),
        lambda v: tag_dict_pack(v),
        lambda v: tag_list_unpack(v)),  # STLV; recur
    const.IEnumTag.Tag_1177: (
        lambda v: v[:255].strip(),
        lambda v: util.s2b(v[:255]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1178: (
        lambda v: datetime.datetime.fromisoformat(v),
        lambda v: util.ui2b4(int(v.timestamp())),  # FIXME: hours
        lambda v: util.b2ut(v)),  # Unixtime(y,d,m[,h]), bytes[4]; 0x2E
    const.IEnumTag.Tag_1179: (
        lambda v: v[:32].strip(),
        lambda v: util.s2b(v[:32]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1187: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1192: (
        lambda v: v[:16].strip(),
        lambda v: util.s2b(v[:16]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1199: (
        lambda v: const.IEnumVAT(v),
        lambda v: util.ui2b1(v.value),
        lambda v: const.IEnumVAT(util.b2ui(v))),
    const.IEnumTag.Tag_1203: (
        lambda v: v[:12].strip(),
        lambda v: util.s2b(v[:12]).ljust(12),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1212: (
        lambda v: v,
        lambda v: util.ui2b1(v),
        lambda v: util.b2ui(v)),  # TODO: enum
    const.IEnumTag.Tag_1214: (
        lambda v: v,
        lambda v: util.ui2b1(v),
        lambda v: util.b2ui(v)),  # TODO: enum
    const.IEnumTag.Tag_1215: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1216: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1217: (
        lambda v: v,
        lambda v: util.ui2vln(v),
        lambda v: util.b2ui(v)),  # VLN
    # 30000: datetime[5]
}


def json2tagdict(data: dict) -> TagDict:
    """Convert raw json data into TagDict."""
    retvalue = {}
    for k, v in data.items():  # or: select keys by required iteration
        ik = int(k)              # - check #1: tag is int
        t = const.IEnumTag(ik)  # TODO: exception if not in
        f = TAG2FUNC[t][0]
        # print(t, v)
        real_val = f(v)
        retvalue[t] = real_val
    return retvalue


def tag_dict_pack(td: TagDict) -> bytes:
    """Pack TagDict into bytes."""
    retvalue: bytes = b''
    for k, v in td.items():
        # print(k, v)
        f = TAG2FUNC[k][1]
        out_bytes = f(v)
        retvalue += util.ui2b2(k.value)
        retvalue += util.ui2b2(len(out_bytes))
        retvalue += out_bytes
    return retvalue


def tag_list_unpack(tl: bytes) -> TagDict:
    """Unpack raw TLV[]:bytes into TagDict."""
    def __walk_taglist(__tl: bytes) -> Tuple[int, bytes]:
        __l_tl = len(__tl)  # whole data len
        __i = 0
        while __i < __l_tl:
            __l_t = util.b2ui(__tl[__i+2:__i+4])  # trag raw data len
            yield util.b2ui(__tl[__i:__i+2]), __tl[__i+4:__i+4+__l_t]  # tag (id, raw data)
            __i += (4 + __l_t)
    retvalue = {}
    for t_id, t_data in __walk_taglist(tl):
        if t_id not in const.TAGS_UNKNOWN:  # skip not documented
            # print(f"{t_id} ({util.b2hex(util.ui2b2(t_id))}): {util.b2hex(t_data)} ({len(t_data)})")
            t = const.IEnumTag(t_id)
            if t in retvalue:  # FIXME: RTFM multitags
                raise RuntimeError(f"{t} already counted.")
            if t not in TAG2FUNC:
                print(f"Tag {t} not processed ({util.b2hex(t_data)}).", file=sys.stderr)
                continue
            retvalue[t] = TAG2FUNC[t][2](t_data)
    return retvalue
