"""Tags things.

Copyright 2023 TI_Eugene <ti.eugene@gmail.com>
This file is part of the kitpos project.
You may use this file under the terms of the GPLv3 license.
"""
# 1. std
from typing import Dict, Any, Tuple, Callable, Optional
import datetime
import logging
# 3. local
from kitpos import const, flag, util, exc
# y. typedefs
TagDict = Dict[const.IEnumTag, Any]
TagPair = Tuple[const.IEnumTag, Any]


def tagdict_unjson(data: Dict[str, Any]) -> TagDict:
    """Convert raw json data into TagDict."""
    retvalue = {}
    for k, val in data.items():  # or: select keys by required iteration
        i_key = int(k)              # - check #1: tag is int
        try:
            __tag = const.IEnumTag(i_key)
        except ValueError as __e:
            raise exc.KpeTagUnjson(__e) from __e
        # if __tag not in TAG2FUNC:  # not need in normal use
        #    raise exc.KpeTagUnjson(f"Tag '{i_key}' unprocessable by TAG2FUNC yet")
        t_func = TAG2FUNC[__tag][0]
        try:
            real_val = t_func(val)
        except ValueError as __e:  # EnumType[/Flag] init
            raise exc.KpeTagUnjson(__e) from __e
        retvalue[__tag] = real_val
    return retvalue


def tag_pack(tag: const.IEnumTag, payload: bytes) -> bytes:
    """Pack tag-value pair into bytes."""
    return util.ui2b2(tag.value) + util.ui2b2(len(payload)) + payload


def tagdict_pack(t_dict: TagDict) -> bytes:
    """Pack TagDict into bytes."""
    retvalue: bytes = b''
    for k, val in t_dict.items():
        t_func = TAG2FUNC[k][1]
        try:
            payload = t_func(val)
        except ValueError as __e:  # EnumType[/Flag] init
            raise exc.KpeTagPack(__e) from __e
        retvalue += tag_pack(k, payload)
    return retvalue


def tag_unpack(data: bytes, skip_unknown: bool = False) -> Optional[TagPair]:  # FIXME: pylint: disable=R1710
    """Unpack tag from bytes (tag:uin16, len:uin16, value:Any)."""
    if (d_len := len(data)) < 4:
        raise exc.KpeRspUnpack(f"Too few data to unpack ({d_len} bytes)")
    # 1. get tag
    t_id = util.b2ui(data[:2])
    if skip_unknown and t_id in const.TAGS_UNKNOWN:
        logging.warning(f"Unknow tag: {t_id}")
        return
    try:
        __tag = const.IEnumTag(t_id)
    except ValueError as __e:
        raise exc.KpeTagUnpack(__e) from __e
    # 2. get data len
    if (t_len := util.b2ui(data[2:4])) != (d_len - 4):
        raise exc.KpeTagUnpack(f"Shipped tag data len ({t_len}) != real ({(d_len - 4)}).")
    t_data = data[4:]
    # 3. convert data
    if __tag not in TAG2FUNC:
        raise exc.KpeTagUnpack(f"Tag '{__tag}' not processing yet (payload '{util.b2hex(t_data)}').")
    try:
        __val = TAG2FUNC[__tag][2](t_data)
    except ValueError as __e:  # EnumType[/Flag] init
        raise exc.KpeTagUnpack(__e) from __e
    return __tag, __val


def tagdict_unpack(t_list: bytes) -> TagDict:
    """Unpack raw TLV[]:bytes into TagDict."""
    def __walk_chunks(__tl: bytes) -> bytes:
        """Split TLV[] by TLVs."""
        __l_tl = len(__tl)  # whole data len
        __i = 0  # 'ptr'
        while __i < __l_tl:
            if __i + 4 > __l_tl:
                raise exc.KpeTagUnpack(f"Too few data to unpack [{__i}:{__l_tl}].")
            __l_t = util.b2ui(__tl[__i+2:__i+4])  # current tag raw data len
            if __i + 4 + __l_t > __l_tl:
                raise exc.KpeTagUnpack(f"Too few data for tag [{__i}:] (need {__l_t + 4} vs {__l_tl - __i} last).")
            yield __tl[__i:__i+4+__l_t]
            __i += (4 + __l_t)
        if __i != __l_tl:  # check tail
            raise exc.KpeTagUnpack(f"Extra data: {util.b2hex(__tl[__i:])}.")
    retvalue = {}
    for chunk in __walk_chunks(t_list):
        # logging.debug(util.b2hex(chunk))
        if __tag__val := tag_unpack(chunk, skip_unknown=True):
            __tag, __val = __tag__val
            if __tag in retvalue:  # FIXME: multitags
                raise exc.KpeTagUnpack(f"Tag '{__tag}' already counted.")
            retvalue[__tag] = __val
    return retvalue


# Tag: (json_2_value, value_2_bytes (pack), bytes_2_value (unpack))
TAG2FUNC: Dict[const.IEnumTag, Tuple[Callable, Callable, Callable]] = {
    const.IEnumTag.TAG_1001: (
        lambda v: v,
        util.l2b,
        util.b2l),
    const.IEnumTag.TAG_1002: (
        lambda v: v,
        util.l2b,
        util.b2l),
    const.IEnumTag.TAG_1008: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        util.b2s),
    const.IEnumTag.TAG_1009: (
        lambda v: v[:164].strip(),
        lambda v: util.s2b(v[:164]),
        util.b2s),
    const.IEnumTag.TAG_1012: (
        datetime.datetime.fromisoformat,
        lambda v: util.ui2b4(int(v.timestamp())),
        util.b2ut),
    const.IEnumTag.TAG_1013: (
        lambda v: v[:20].strip(),
        lambda v: util.s2b(v[:20]),
        util.b2s),
    const.IEnumTag.TAG_1017: (
        lambda v: v[:12].strip(),
        lambda v: util.s2b(v[:12]).ljust(12),
        util.b2s),
    const.IEnumTag.TAG_1018: (
        lambda v: v[:12].strip(),
        lambda v: util.s2b(v[:12]).ljust(12),
        util.b2s),
    const.IEnumTag.TAG_1020: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1021: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        util.b2s),
    const.IEnumTag.TAG_1023: (
        lambda v: v,
        util.n2fvln,
        util.fvln2n),  # FVLN; 0x2B
    const.IEnumTag.TAG_1030: (
        lambda v: v[:128].strip(),
        lambda v: util.s2b(v[:128]),
        util.b2s),
    const.IEnumTag.TAG_1031: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1036: (
        lambda v: v[:21].strip(),
        lambda v: util.s2b(v[:21]),
        util.b2s),
    const.IEnumTag.TAG_1037: (
        lambda v: v[:20].strip(),
        lambda v: util.s2b(v[:20]),
        util.b2s),
    const.IEnumTag.TAG_1038: (
        lambda v: v,
        util.ui2b4,
        util.b2ui),
    const.IEnumTag.TAG_1040: (
        lambda v: v,
        util.ui2b4,
        util.b2ui),
    const.IEnumTag.TAG_1041: (
        lambda v: v[:16].strip(),
        lambda v: util.s2b(v[:16]),
        util.b2s),
    const.IEnumTag.TAG_1046: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        util.b2s),
    const.IEnumTag.TAG_1048: (
        lambda v: v[:128].strip(),
        lambda v: util.s2b(v[:128]),
        util.b2s),
    const.IEnumTag.TAG_1055: (
        flag.TaxModes,  # byte[1] == int
        lambda v: v.as_bytes(),
        lambda v: flag.TaxModes(util.b2ui(v))),  # 0x2D, 0x2E; FIXME: .bit_count() == 1
    const.IEnumTag.TAG_1059: (
        tagdict_unjson,
        tagdict_pack,
        tagdict_unpack),  # STLV; recur
    const.IEnumTag.TAG_1079: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1081: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1102: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1103: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1104: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1105: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1106: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1107: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1117: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        util.b2s),
    const.IEnumTag.TAG_1171: (
        lambda v: v[:20].strip(),
        lambda v: util.s2b(v[:20]),
        util.b2s),
    const.IEnumTag.TAG_1173: (
        lambda v: v,
        util.l2b,
        util.b2l),
    const.IEnumTag.TAG_1174: (
        tagdict_unjson,
        tagdict_pack,
        tagdict_unpack),  # STLV; recur
    const.IEnumTag.TAG_1177: (
        lambda v: v[:255].strip(),
        lambda v: util.s2b(v[:255]),
        util.b2s),
    const.IEnumTag.TAG_1178: (
        datetime.datetime.fromisoformat,
        lambda v: util.ui2b4(int(v.timestamp())),  # FIXME: hours
        util.b2ut),  # Unixtime(y,d,m), bytes[4]; 0x2E
    const.IEnumTag.TAG_1179: (
        lambda v: v[:32].strip(),
        lambda v: util.s2b(v[:32]),
        util.b2s),
    const.IEnumTag.TAG_1187: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        util.b2s),
    const.IEnumTag.TAG_1192: (
        lambda v: v[:16].strip(),
        lambda v: util.s2b(v[:16]),
        util.b2s),
    const.IEnumTag.TAG_1199: (
        const.IEnumVAT,
        lambda v: util.ui2b1(v.value),
        lambda v: const.IEnumVAT(util.b2ui(v))),
    const.IEnumTag.TAG_1203: (
        lambda v: v[:12].strip(),
        lambda v: util.s2b(v[:12]).ljust(12),
        util.b2s),
    const.IEnumTag.TAG_1212: (
        lambda v: v,
        util.ui2b1,
        util.b2ui),  # TODO: enum
    const.IEnumTag.TAG_1214: (
        lambda v: v,
        util.ui2b1,
        util.b2ui),  # TODO: enum
    const.IEnumTag.TAG_1215: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1216: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1217: (
        lambda v: v,
        util.ui2vln,
        util.b2ui),  # VLN
    const.IEnumTag.TAG_1222: (
        flag.AgentModes,
        lambda v: v.as_bytes(),
        lambda v: flag.AgentModes(util.b2ui(v))),
    const.IEnumTag.TAG_1225: (
        lambda v: v[:64].strip(),
        lambda v: util.s2b(v[:64]),
        util.b2s),
    const.IEnumTag.TAG_1226: (
        lambda v: v[:12].strip(),
        lambda v: util.s2b(v[:12]).ljust(12),
        util.b2s),
    const.IEnumTag.TAG_30000: (
        datetime.datetime.fromisoformat,
        util.dt2b5,
        util.b2dt),  # TODO: check
}
