# Backup

```py
def __tagdict_unpack_old(t_list: bytes) -> TagDict:  # not used
    def __walk_taglist(__tl: bytes) -> Tuple[int, bytes]:
        __l_tl = len(__tl)  # whole data len
        __i = 0  # 'ptr'
        while __i < __l_tl:
            __l_t = util.b2ui(__tl[__i+2:__i+4])  # current tag raw data len
            if __i + __l_t + 2 > __l_tl:
                raise exc.KpeTagUnpack(f"Tag [{__i}:] too big")
            yield util.b2ui(__tl[__i:__i+2]), __tl[__i+4:__i+4+__l_t]  # tag (id, raw data)
            __i += (4 + __l_t)
        # TODO: check last (__i == __l_tl)
    retvalue = {}
    for t_id, t_data in __walk_taglist(t_list):
        if t_id not in const.TAGS_UNKNOWN:  # skip not documented
            # print(f"{t_id} ({util.b2hex(util.ui2b2(t_id))}): {util.b2hex(t_data)} ({len(t_data)})")
            try:
                __tag = const.IEnumTag(t_id)
            except ValueError as e:
                raise exc.KpeTagUnpack(e) from e
            if __tag in retvalue:  # FIXME: multitags
                raise exc.KpeTagUnpack(f"Tag '{__tag}' already counted.")
            if __tag not in TAG2FUNC:
                exc.KpeTagUnpack(f"Tag '{__tag}' not processing yet (payload '{util.b2hex(t_data)}').")
            try:
                retvalue[__tag] = TAG2FUNC[__tag][2](t_data)
            except ValueError as e:  # EnumType[/Flag] init
                raise exc.KpeTagUnpack(e) from e
    return retvalue
```