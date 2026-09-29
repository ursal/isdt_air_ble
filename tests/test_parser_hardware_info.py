"""Unit tests for HardwareInfo parsing."""

from __future__ import annotations

from isdt_air_ble.parser import parse_hardware_info


def test_parse_hardware_info_with_centperi_yields_no_serial():
    """Devices sending static 'CENTPERI' (0x49524550544E4543) should return None for serial."""
    raw = bytes.fromhex("e1 01 01 01 06 43 45 4e 54 50 45 52 49")
    res = parse_hardware_info(raw)
    assert res is not None
    hw, sw, sn = res
    assert hw == "1.1"
    assert sw == "1.6"
    assert sn is None


def test_parse_hardware_info_framed_with_centperi():
    """Framed version (0x31 0xE1 ...) with CENTPERI."""
    raw = bytes.fromhex("31 e1 02 00 01 04 43 45 4e 54 50 45 52 49")
    res = parse_hardware_info(raw)
    assert res is not None
    hw, sw, sn = res
    assert hw == "2.0"
    assert sw == "1.4"
    assert sn is None


def test_parse_hardware_info_valid_custom_serial():
    """Valid non-CENTPERI device ID."""
    raw = bytes.fromhex("e1 01 00 01 00 12 34 56 78 9a bc de f0")
    res = parse_hardware_info(raw)
    assert res is not None
    hw, sw, sn = res
    assert hw == "1.0"
    assert sw == "1.0"
    assert sn == "F0DEBC9A78563412"


def test_parse_hardware_info_too_short():
    assert parse_hardware_info(b"\xe1\x01\x01") is None
    assert parse_hardware_info(b"") is None


def test_parse_hardware_info_invalid_cmd():
    assert parse_hardware_info(bytes.fromhex("31 e7 00 03 4f 09 00")) is None
