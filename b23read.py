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


    client.close()