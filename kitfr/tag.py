"""Tags things."""
import sys
from typing import Dict, Any, Tuple

from kitfr import const, flag, util


_TAG2FUNC = {  # Tag: (v2, b2v)
    const.IEnumTag.Tag_1009: (lambda v: util.s2b(v[:164]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1017: (lambda v: util.s2b(v[:12]).ljust(12), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1021: (lambda v: util.s2b(v[:64]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1023: (None, lambda v: util.fvln2n(v)),  # FVLN
    const.IEnumTag.Tag_1030: (lambda v: util.s2b(v[:128]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1031: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1036: (lambda v: util.s2b(v[:21]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1046: (lambda v: util.s2b(v[:64]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1048: (lambda v: util.s2b(v[:128]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1055: (lambda v: v.b(), lambda v: flag.TaxModes(util.b2ui(v))),
    const.IEnumTag.Tag_1059: (None, lambda v: tag_list_unpack(v)),  # STLV; recur
    const.IEnumTag.Tag_1079: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1081: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1102: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1103: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1104: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1105: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1106: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1107: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1117: (lambda v: util.s2b(v[:64]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1173: (lambda v: util.l2b(v), lambda v: util.b2l(v)),
    const.IEnumTag.Tag_1174: (None, lambda v: tag_list_unpack(v)),  # STLV; recur
    const.IEnumTag.Tag_1177: (lambda v: util.s2b(v[:255]), lambda v: util.b2s(v)),
    # 1178: Unixtime(y,d,m[,h])
    const.IEnumTag.Tag_1179: (lambda v: util.s2b(v[:32]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1187: (lambda v: util.s2b(v[:64]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1192: (lambda v: util.s2b(v[:16]), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1199: (lambda v: util.ui2b1(v.value), lambda v: const.IEnumVAT(util.b2ui(v))),
    const.IEnumTag.Tag_1203: (lambda v: util.s2b(v[:12]).ljust(12), lambda v: util.b2s(v)),
    const.IEnumTag.Tag_1212: (lambda v: util.l2b(v), lambda v: util.b2l(v)),  # TODO: enum
    const.IEnumTag.Tag_1214: (lambda v: util.l2b(v), lambda v: util.b2l(v)),  # TODO: enum
    const.IEnumTag.Tag_1215: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1216: (None, lambda v: util.b2ui(v)),  # VLN
    const.IEnumTag.Tag_1217: (None, lambda v: util.b2ui(v)),  # VLN
    # 30000: datetime[5]
}


def tag_list_unpack(v: bytes) -> Dict[const.IEnumTag, Any]:
    """Unpack raw TLV[] into ."""
    def __walk_taglist(__tl: bytes) -> Tuple[int, bytes]:
        __l_tl = len(__tl)  # whole data len
        __i = 0
        while __i < __l_tl:
            __l_t = util.b2ui(__tl[__i+2:__i+4])  # trag raw data len
            yield util.b2ui(__tl[__i:__i+2]), __tl[__i+4:__i+4+__l_t]  # tag (id, raw data)
            __i += (4 + __l_t)
    retvalue = {}
    for t_id, t_data in __walk_taglist(v):
        if t_id not in const.TAGS_UNKNOWN:  # skip not documented
            # print(f"{t_id} ({util.b2hex(util.ui2b2(t_id))}): {util.b2hex(t_data)} ({len(t_data)})")
            t = const.IEnumTag(t_id)
            if t in retvalue:  # FIXME: RTFM multitags
                raise RuntimeError(f"{t} already counted.")
            if t not in _TAG2FUNC:
                print(f"Tag {t} not processed ({util.b2hex(t_data)}).", file=sys.stderr)
                continue
            retvalue[t] = _TAG2FUNC[t][1](t_data)
    return retvalue
