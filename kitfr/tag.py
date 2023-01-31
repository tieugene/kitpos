"""Tags things."""
# 1. std
from typing import Dict, Any, Tuple
import sys
# 3. local
from kitfr import const, flag, util

TagDict = Dict[const.IEnumTag, Any]

TAG2FUNC = {  # Tag: (json_2_value, value_2_bytes (pack), bytes_2_value (unpack))
    const.IEnumTag.Tag_1009: (
        lambda v: v[:164].strip(),
        lambda v: util.s2b(v[:164]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1017: (
        None,
        lambda v: util.s2b(v[:12]).ljust(12),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1021: (
        None,
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1023: (
        None,
        None,
        lambda v: util.fvln2n(v)),  # FVLN
    const.IEnumTag.Tag_1030: (
        None,
        lambda v: util.s2b(v[:128]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1031: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1036: (
        lambda v: v[:21].strip(),
        lambda v: util.s2b(v[:21]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1046: (
        None,
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1048: (
        None,
        lambda v: util.s2b(v[:128]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1055: (
        None,
        lambda v: v.b(),
        lambda v: flag.TaxModes(util.b2ui(v))),
    const.IEnumTag.Tag_1059: (
        None,
        None,
        lambda v: tag_list_unpack(v)),  # STLV; recur
    const.IEnumTag.Tag_1079: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1081: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1102: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1103: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1104: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1105: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1106: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1107: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1117: (
        None,
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1173: (
        None,
        lambda v: util.l2b(v),
        lambda v: util.b2l(v)),
    const.IEnumTag.Tag_1174: (
        None,
        None,
        lambda v: tag_list_unpack(v)),  # STLV; recur
    const.IEnumTag.Tag_1177: (
        None,
        lambda v: util.s2b(v[:255]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1178: (
        None,
        None,
        lambda v: util.b2ut(v)),  # Unixtime(y,d,m[,h])
    const.IEnumTag.Tag_1179: (
        None,
        lambda v: util.s2b(v[:32]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1187: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1192: (
        None,
        lambda v: util.s2b(v[:16]),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1199: (
        None,
        lambda v: util.ui2b1(v.value),
        lambda v: const.IEnumVAT(util.b2ui(v))),
    const.IEnumTag.Tag_1203: (
        None,
        lambda v: util.s2b(v[:12]).ljust(12),
        lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1212: (
        None,
        lambda v: util.l2b(v),
        lambda v: util.b2l(v)),  # TODO: enum
    const.IEnumTag.Tag_1214: (
        None,
        lambda v: util.l2b(v),
        lambda v: util.b2l(v)),  # TODO: enum
    const.IEnumTag.Tag_1215: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1216: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1217: (
        None,
        None,
        lambda v: util.b2ui(v)),  # VLN
    # 30000: datetime[5]
}


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
            retvalue[t] = TAG2FUNC[t][1](t_data)
    return retvalue


def tag_dict_pack(td: TagDict) -> bytes:
    """Pack TagDict into bytes."""
    retvalue: bytes = b''
    for k, v in td.items():
        f = TAG2FUNC[k][1]
        out_bytes = f(v)
        retvalue += util.ui2b2(k.value)
        retvalue += util.ui2b2(len(out_bytes))
        retvalue += out_bytes
    return retvalue
