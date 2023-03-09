"""CLI commands executors.

Copyright 2023 TI_Eugene <ti.eugene@gmail.com>
This file is part of the kitpos project.
You may use this file under the terms of the GPLv3 license.
"""
# 1. std
from typing import Optional, Dict, Callable
import datetime
# 3. local
from kitpos import cmd, tag, const, exc
# x. const
JSON_ARG = '<json>'
ERR_TEXT = {
    'ru': {
        0x01: "Неверный формат команды",
        0x02: "Данная команда требует другого состояния ФН",
        0x03: "Ошибка ФН",
        0x04: "Ошибка KC",
        0x05: "Закончен срок эксплуатации ФН",
        0x06: "Архив ФН переполнен",
        0x07: "Дата и время операции не соответствуют логике работы ФН",
        0x08: "Запрошенные данные отсутствуют в Архиве ФН",
        0x09: "Параметры команды имеют правильный формат, но их значение не верно",
        0x10: "Превышение размеров TLV данных",
        0x12: "Исчерпан ресурс КС. Требуется закрытие фискального режима",
        0x14: "Ресурс хранения документов для ОФД исчерпан",
        0x15: "Превышено время ожидания передачи сообщения (30 дней)",
        0x16: "Продолжительность смены более 24 часов",
        0x17: "Неверная разница во времени между 2 операциями (более 5 минут)",
        0x20: "Сообщение от ОФД не может быть принято",
        0x25: "Неверная структура команды, либо неверная контрольная сумма",
        0x26: "Неизвестная команда",
        0x27: "Неверная длина параметров команды",
        0x28: "Неверный формат или значение параметров команды",
        0x30: "Нет связи с ФН",
        0x31: "Неверные дата/время в ККТ",
        0x32: "Переданы не все необходимые данные",
        0x33: "РНМ сформирован неверно, проверка на данной ККТ не прошла",
        0x34: "Данные команды уже были переданы ранее. (Применительно к данным агента, данным оплаты, данным"
              " автоматического устройства расчетов)",
        0x35: "Аппаратный сбой ККТ",
        0x36: "Неверно указан признак расчета, возможные значения: приход, расход, возврат прихода, возврат расхода",
        0x37: "Указанный налог не может быть применен",
        0x38: "Команда необходима только для платежного агента (указано при регистрации)",
        0x39: "Сумма расчета чека не равна сумме следующих значений по чеку: сумма наличными, сумма электронными, сумма"
              " предоплатой, сумма постоплатой, сумма встречным предоставлением",
        0x3A: "Сумма оплаты соответствующими типами (за исключением наличных) превышает итог чека",
        0x3B: "Некорректная разрядность итога чека",
        0x3C: "Некорректная разрядность денежных величин",
        0x3D: "Превышено максимально допустимое количество предметов расчета в чеке",
        0x3E: "Превышено максимально допустимое количество предметов расчета c данными агента в чеке",
        0x3F: "Невозможно передать данные агента, допустимы данные агента либо для всего чека, либо данные агента по"
              " предметам расчета",
        0x40: "Некорректный статус печатающего устройства",
        0x42: "Сумма изъятия больше доступной суммы наличных в ККТ",
        0x43: "Операция внесения-изъятия денег в ККТ возможна только при открытой смене",
        0x44: "Счетчики денег не инициализированы",
        0x45: "Сумма по чеку коррекции всеми типами оплаты не равна полной сумме для расчетов по ставкам НДС",
        0x46: "Сумма по чеку коррекции всеми типами оплаты не равна итоговой сумме чека коррекции",
        0x47: "В чеке коррекции не указано ни одной суммы для расчетов по ставкам НДС",
        0x50: "Ошибка сохранения настроек",
        0x51: "Передано некорректное значение времени",
        0x52: "В чеке не должны присутствовать иные предметы расчета помимо предмета расчета с признаком способа"
              " расчета «Оплата кредита»",
        0x53: "Переданы не все необходимые данные для агента",
        0x54: "Итоговая сумма расчета (в рублях без учета копеек) не равна сумме стоимости всех предметов расчета (в"
              " рублях без учета копеек)",
        0x55: "Неверно указан признак расчета для чека коррекции, возможные значения: приход, расход",
        0x56: "Неверная структура переданных данных для агента",
        0x57: "Не указан режим налогообложения",
        0x58: "Данная ставка НДС недопустима для агента. Агент не является плательщиком НДС",
        0x59: "Не указано или неверно указано значение тэга `Признак платежного агента`",
        0x5A: "Невозможно внести товарную позицию уже после внесения данных об оплате",
        0x5B: "Команда может быть выполнена только при открытом чеке",
        0x5C: "Некорректный формат или длина в массиве переданных строк нефискальной информации",
        0x5D: "Достигнуто максимальное количество строк нефискальной информации",
        0x5E: "Не переданы данные кассира",
        0x60: "Номер блока прошивки указан некорректно",
        0x70: "Значение не зашито в ККТ",
        0x71: "Некорректное значение серийного номера",
        0x7F: "Команда не выполнена",
        0xE0: "Присутствуют неотправленные в ОФД документы",
        0xF3: "Подключенный ФН не соответствует данным регистрации ККТ",
        0xF4: "ФН еще не был активирован",
        0xF5: "ФН был закрыт",
        0x1F: "Передать данные автоматического устройства расчетов для кассового чека (БСО)",
        # 0x3F: "Передать данные автоматического устройства расчетов для кассового чека (БСО) коррекции",  # ???
    }
}


def __cmd_21(val: Optional[str]) -> Optional[cmd.CmdSessionOpenBegin]:
    """0x21: Begin opening session [0 (default)|1 - skip prn]."""
    if val:
        if val not in {'0', '1'}:
            raise exc.KpeCLI("Skip printing must be '0' or '1'.")  # == return None
        return cmd.CmdSessionOpenBegin(val == '1')
    return cmd.CmdSessionOpenBegin()


def __cmd_29(val: Optional[str]) -> Optional[cmd.CmdSessionCloseBegin]:
    """0x29: Begin closing session [0 (default)|1 - skip prn]."""
    if val:
        if val not in {'0', '1'}:
            raise exc.KpeCLI("Skip printing must be '0' or '1'.")
        return cmd.CmdSessionCloseBegin(val == '1')
    return cmd.CmdSessionCloseBegin()


def __cmd_30(val: Optional[str]) -> Optional[cmd.CmdGetDocInfo]:
    """0x30: Get document info."""
    if val:
        return cmd.CmdGetDocInfo(int(val))
    raise exc.KpeCLI("Doc number required.")


def __cmd_33(val: Optional[str]) -> Optional[cmd.CmdGetStorageActResult]:
    """0x33: Get FS activation result [0 (default)|1 - skip prn]."""
    if val:  # TODO: check 1..255
        return cmd.CmdGetStorageActResult(int(val))
    return cmd.CmdGetStorageActResult()


def __cmd_3a(val: Optional[str]) -> Optional[cmd.CmdGetDocData]:
    """0x3A: Read document content."""
    if val:
        return cmd.CmdGetDocData(int(val))
    raise exc.KpeCLI("Doc number required.")


def __cmd_72(val: Optional[str]) -> Optional[cmd.CmdSetDateTime]:
    """0x72: Set POS date/time."""
    if val:
        try:
            __dt = datetime.datetime.strptime(val, '%y%m%d%H%M')
        except ValueError as __e:
            raise exc.KpeCLI(__e)
        return cmd.CmdSetDateTime(__dt)
    raise exc.KpeCLI("Date/time required (yymmddHHMM).")


def __cmd_2e(val: Dict) -> cmd.CmdCorrReceiptData:
    """Corr. Receipt. Step #2/4 - send data."""
    return cmd.CmdCorrReceiptData(tag.tagdict_unjson(val))


def __cmd_3f(val: Dict) -> cmd.CmdCorrReceiptAutomat:
    """Corr. Receipt. Step #3/4 - send automat number (option)."""
    return cmd.CmdCorrReceiptAutomat(tag.tagdict_unjson(val))


def __cmd_26(val: Dict[str, int]) -> cmd.CmdCorrReceiptCommit:
    """Corr. Receipt. Step #4/4 - commit."""
    try:
        rcp_type = const.IEnumReceiptType(val['type'])
    except ValueError as __e:
        raise exc.KpeCLI(__e) from __e
    return cmd.CmdCorrReceiptCommit(
        req_type=rcp_type,
        total=val['total']
    )


def __cmd_2b(val: Dict) -> cmd.CmdReceiptItem:
    """Receipt. Step #2/6 - send receipt item."""
    return cmd.CmdReceiptItem(tag.tagdict_unjson(val))


def __cmd_1f(val: Dict) -> cmd.CmdReceiptAutomat:
    """Receipt. Step #4/6 - send receipt automat details."""
    return cmd.CmdReceiptAutomat(tag.tagdict_unjson(val))


def __cmd_2d(val: Dict) -> cmd.CmdReceiptPayment:
    """Receipt. Step #5/6 - send receipt payment details."""
    return cmd.CmdReceiptPayment(tag.tagdict_unjson(val))


def __cmd_24(val: Dict) -> cmd.CmdReceiptCommit:
    """Receipt. Step #6/6 - commit."""
    try:
        rcp_type = const.IEnumReceiptType(val['type'])
    except ValueError as __e:
        raise exc.KpeCLI(__e) from __e
    return cmd.CmdReceiptCommit(
        req_type=rcp_type,
        total=val['total'],
        notes=val.get('notes')
    )


COMMANDS: Dict[str, Callable] = {  # TODO: replace some functions w/ class directly
    'GetDeviceStatus': lambda: cmd.CmdGetDeviceStatus(),  # 0x01: Get POS status
    'GetDeviceFN': lambda: cmd.CmdGetDeviceFN(),  # 0x02: Get POS factory number
    'GetDeviceFWVer': lambda: cmd.CmdGetDeviceFWVer(),  # 0x03: Get POS firmware version
    'GetDeviceModel': lambda: cmd.CmdGetDeviceModel(),  # 0x04: Get POS model
    'GetStorageFN': lambda: cmd.CmdGetStorageFN(),  # 0x05: Get FS factory number
    'GetStorageFWVer': lambda: cmd.CmdGetStorageFWVer(),  # 0x06: Get FS firmware version
    'GetStorageExpired': lambda: cmd.CmdGetStorageExpired(),  # 0x07: Get FS date expired
    'GetStorageStatus': lambda: cmd.CmdGetStorageStatus(),  # 0x08: Get FS status
    'GetRegisterParms': lambda: cmd.CmdGetRegisterParms(),  # 0x0A: Get POS/FS registering parameters
    'GetDeviceCfgVer': lambda: cmd.CmdGetDeviceCfgVer(),  # 0x0B: Get POS config version
    'GetNetParms': lambda: cmd.CmdGetNetParms(),  # 0x0E: Get current network parameters
    'DocCancel': lambda: cmd.CmdDocCancel(),  # 0x10: Cancel current document
    'GetCurSession': lambda: cmd.CmdGetCurSession(),  # 0x20: Get session params
    'SessionOpenBegin': (__cmd_21, '[0/1]'),  # 0x21: Begin opening session
    'SessionOpenCommit': lambda: cmd.CmdSessionOpenCommit(),  # 0x22: Commit opening session
    'SessionCloseBegin': (__cmd_29, '[0/1]'),  # 0x29: Begin closing session
    'SessionCloseCommit': lambda: cmd.CmdSessionCloseCommit(),  # 0x2A Commit closing session
    'GetDocInfo': (__cmd_30, '<int>'),  # 0x30: Get document info
    'GetUnsentDocNum': lambda: cmd.CmdGetUnsentDocNum(),  # 0x32: Number of FD not confirmed by OFD
    'GetStorageActResult': (__cmd_33, '[int]'),  # 0x33: Get FS activation result
    'GetDocData': (__cmd_3a, '<int>'),  # 0x3A: Read document content
    'GetOFDXchgStatus': lambda: cmd.CmdGetOFDXchgStatus(),  # 0x50: Get OFD exchange status
    'SetDateTime': (__cmd_72, '<yymmddHHMM>'),  # 0x72: Set POS date/time
    'GetDateTime': lambda: cmd.CmdGetDateTime(),  # 0x73: Get POS date/time
    'GetDeviceNetParms': lambda: cmd.CmdGetDeviceNetParms(),  # 0x75: Get POS network settings
    'GetDeviceOFDParms': lambda: cmd.CmdGetDeviceOFDParms(),  # 0x77: Get POS OFD settings
    'GetPrnLineLen': lambda: cmd.CmdGetPrnLineLen(),  # 0xBB: Get print line length (symbols)
    'CorrReceiptBegin': lambda: cmd.CmdCorrReceiptBegin(),  # 0x25: Corr. Receipt. Step #1/4 - begin
    'CorrReceiptData': (__cmd_2e, JSON_ARG),
    'CorrReceiptAutomat': (__cmd_3f, JSON_ARG),
    'CorrReceiptCommit': (__cmd_26, JSON_ARG),
    'ReceiptBegin': lambda: cmd.CmdReceiptBegin(),  # 0x23: Receipt. Step #1/6 - begin
    'ReceiptItem': (__cmd_2b, JSON_ARG),
    'ReceiptAutomat': (__cmd_1f, JSON_ARG),
    'ReceiptPayment': (__cmd_2d, JSON_ARG),
    'ReceiptCommit': (__cmd_24, JSON_ARG)
}
