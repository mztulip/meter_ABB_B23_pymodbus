import logging
import sys
from pymodbus.client import ModbusSerialClient
#pymodbus 3.13

logging.basicConfig()
logging.root.setLevel(logging.WARNING)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger("pymodbus").setLevel(logging.INFO)

INVALID_U32 = 0xFFFFFFFF
INVALID_S32_MAX = 0x7FFFFFFF
INVALID_S32_MIN = 0x80000000
INVALID_U16 = 0xFFFF
INVALID_S16_MAX = 0x7FFF
INVALID_S16_MIN = 0x8000

def read_u32(client, address, slave=1):
    r = client.read_holding_registers(address=address, count=2, device_id=slave)
    if r.isError():
        return None
    val = (r.registers[0] << 16) | r.registers[1]
    return None if val == INVALID_U32 else val

def read_s32(client, address, slave=1):
    r = client.read_holding_registers(address=address, count=2, device_id=slave)
    if r.isError():
        return None
    val = (r.registers[0] << 16) | r.registers[1]
    if val == INVALID_S32_MAX or val == INVALID_S32_MIN:
        return None
    if val >= 0x80000000:
        val -= 0x100000000
    return val

def read_u16(client, address, slave=1):
    r = client.read_holding_registers(address=address, count=1, device_id=slave)
    if r.isError():
        return None
    val = r.registers[0]
    return None if val == INVALID_U16 else val

def read_s16(client, address, slave=1):
    r = client.read_holding_registers(address=address, count=1, device_id=slave)
    if r.isError():
        return None
    val = r.registers[0]
    if val == INVALID_S16_MAX or val == INVALID_S16_MIN:
        return None
    if val >= 0x8000:
        val -= 0x10000
    return val

def fmt(value, divisor, unit, decimals=2):
    if value is None:
        return "N/A"
    return f"{value / divisor:.{decimals}f} {unit}".strip()

if __name__ == "__main__":
    client = ModbusSerialClient(
        port="/dev/ttyUSB0",
        baudrate=9600,
        stopbits=1,
        parity='N',
        bytesize=8
    )

    s = 1  # slave id

    print("\n--- Napięcia fazowe ---")
    print(f"  Voltage L1-N:  {fmt(read_u32(client, 0x5B00, s), 10, 'V', 1)}")
    print(f"  Voltage L2-N:  {fmt(read_u32(client, 0x5B02, s), 10, 'V', 1)}")
    print(f"  Voltage L3-N:  {fmt(read_u32(client, 0x5B04, s), 10, 'V', 1)}")

    print("\n--- Napięcia międzyfazowe ---")
    print(f"  Voltage L1-L2: {fmt(read_u32(client, 0x5B06, s), 10, 'V', 1)}")
    print(f"  Voltage L3-L2: {fmt(read_u32(client, 0x5B08, s), 10, 'V', 1)}")
    print(f"  Voltage L1-L3: {fmt(read_u32(client, 0x5B0A, s), 10, 'V', 1)}")

    print("\n--- Prądy ---")
    print(f"  Current L1:    {fmt(read_u32(client, 0x5B0C, s), 100, 'A')}")
    print(f"  Current L2:    {fmt(read_u32(client, 0x5B0E, s), 100, 'A')}")
    print(f"  Current L3:    {fmt(read_u32(client, 0x5B10, s), 100, 'A')}")
    print(f"  Current N:     {fmt(read_u32(client, 0x5B12, s), 100, 'A')}")

    print("\n--- Moc czynna ---")
    print(f"  Active power Total: {fmt(read_s32(client, 0x5B14, s), 100, 'W')}")
    print(f"  Active power L1:    {fmt(read_s32(client, 0x5B16, s), 100, 'W')}")
    print(f"  Active power L2:    {fmt(read_s32(client, 0x5B18, s), 100, 'W')}")
    print(f"  Active power L3:    {fmt(read_s32(client, 0x5B1A, s), 100, 'W')}")

    print("\n--- Moc bierna ---")
    print(f"  Reactive power Total: {fmt(read_s32(client, 0x5B1C, s), 100, 'var')}")
    print(f"  Reactive power L1:    {fmt(read_s32(client, 0x5B1E, s), 100, 'var')}")
    print(f"  Reactive power L2:    {fmt(read_s32(client, 0x5B20, s), 100, 'var')}")
    print(f"  Reactive power L3:    {fmt(read_s32(client, 0x5B22, s), 100, 'var')}")

    print("\n--- Moc pozorna ---")
    print(f"  Apparent power Total: {fmt(read_s32(client, 0x5B24, s), 100, 'VA')}")
    print(f"  Apparent power L1:    {fmt(read_s32(client, 0x5B26, s), 100, 'VA')}")
    print(f"  Apparent power L2:    {fmt(read_s32(client, 0x5B28, s), 100, 'VA')}")
    print(f"  Apparent power L3:    {fmt(read_s32(client, 0x5B2A, s), 100, 'VA')}")

    print("\n--- Częstotliwość ---")
    print(f"  Frequency: {fmt(read_u16(client, 0x5B2C, s), 100, 'Hz')}")

    print("\n--- Kąty fazowe mocy ---")
    print(f"  Phase angle power Total: {fmt(read_s16(client, 0x5B2D, s), 10, '°', 1)}")
    print(f"  Phase angle power L1:    {fmt(read_s16(client, 0x5B2E, s), 10, '°', 1)}")
    print(f"  Phase angle power L2:    {fmt(read_s16(client, 0x5B2F, s), 10, '°', 1)}")
    print(f"  Phase angle power L3:    {fmt(read_s16(client, 0x5B30, s), 10, '°', 1)}")

    print("\n--- Kąty fazowe napięć ---")
    print(f"  Phase angle voltage L1: {fmt(read_s16(client, 0x5B31, s), 10, '°', 1)}")
    print(f"  Phase angle voltage L2: {fmt(read_s16(client, 0x5B32, s), 10, '°', 1)}")
    print(f"  Phase angle voltage L3: {fmt(read_s16(client, 0x5B33, s), 10, '°', 1)}")

    print("\n--- Kąty fazowe prądów ---")
    print(f"  Phase angle current L1: {fmt(read_s16(client, 0x5B37, s), 10, '°', 1)}")
    print(f"  Phase angle current L2: {fmt(read_s16(client, 0x5B38, s), 10, '°', 1)}")
    print(f"  Phase angle current L3: {fmt(read_s16(client, 0x5B39, s), 10, '°', 1)}")

    print("\n--- Współczynnik mocy ---")
    print(f"  Power factor Total: {fmt(read_s16(client, 0x5B3A, s), 1000, '-', 3)}")
    print(f"  Power factor L1:    {fmt(read_s16(client, 0x5B3B, s), 1000, '-', 3)}")
    print(f"  Power factor L2:    {fmt(read_s16(client, 0x5B3C, s), 1000, '-', 3)}")
    print(f"  Power factor L3:    {fmt(read_s16(client, 0x5B3D, s), 1000, '-', 3)}")

    print("\n--- Kwadrant prądu ---")
    print(f"  Current quadrant Total: {fmt(read_u16(client, 0x5B3E, s), 1, '', 0)}")
    print(f"  Current quadrant L1:    {fmt(read_u16(client, 0x5B3F, s), 1, '', 0)}")
    print(f"  Current quadrant L2:    {fmt(read_u16(client, 0x5B40, s), 1, '', 0)}")
    print(f"  Current quadrant L3:    {fmt(read_u16(client, 0x5B41, s), 1, '', 0)}")

    client.close()
