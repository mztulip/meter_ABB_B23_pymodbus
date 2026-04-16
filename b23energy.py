import logging
from pymodbus.client import ModbusSerialClient
#pymodbus 3.13

logging.basicConfig()
logging.root.setLevel(logging.WARNING)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger("pymodbus").setLevel(logging.INFO)

def read_u64(client, address, slave=1):
    r = client.read_holding_registers(address=address, count=4, device_id=slave)
    if r.isError():
        return None
    val = (r.registers[0] << 48) | (r.registers[1] << 32) | (r.registers[2] << 16) | r.registers[3]
    return None if val == 0xFFFFFFFFFFFFFFFF else val

def read_s64(client, address, slave=1):
    r = client.read_holding_registers(address=address, count=4, device_id=slave)
    if r.isError():
        return None
    val = (r.registers[0] << 48) | (r.registers[1] << 32) | (r.registers[2] << 16) | r.registers[3]
    if val == 0x7FFFFFFFFFFFFFFF:
        return None
    if val >= 0x8000000000000000:
        val -= 0x10000000000000000
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

    print("\n--- Energia czynna ---")
    print(f"  Active import: {fmt(read_u64(client, 0x5000, s), 100, 'kWh')}")
    print(f"  Active export: {fmt(read_u64(client, 0x5004, s), 100, 'kWh')}")
    print(f"  Active net:    {fmt(read_s64(client, 0x5008, s), 100, 'kWh')}")

    print("\n--- Energia bierna ---")
    print(f"  Reactive import: {fmt(read_u64(client, 0x500C, s), 100, 'kvarh')}")
    print(f"  Reactive export: {fmt(read_u64(client, 0x5010, s), 100, 'kvarh')}")
    print(f"  Reactive net:    {fmt(read_s64(client, 0x5014, s), 100, 'kvarh')}")

    print("\n--- Energia pozorna ---")
    print(f"  Apparent import: {fmt(read_u64(client, 0x5018, s), 100, 'kVAh')}")
    print(f"  Apparent export: {fmt(read_u64(client, 0x501C, s), 100, 'kVAh')}")
    print(f"  Apparent net:    {fmt(read_s64(client, 0x5020, s), 100, 'kVAh')}")

    print("\n--- CO2 / Waluta ---")
    print(f"  Active import CO2:      {fmt(read_u64(client, 0x5024, s), 1000, 'kg', 3)}")
    print(f"  Active import Currency: {fmt(read_u64(client, 0x5034, s), 1000, 'currency', 3)}")

    print("\n--- Energia czynna per faza ---")
    print(f"  Active import L1: {fmt(read_u64(client, 0x5460, s), 100, 'kWh')}")
    print(f"  Active import L2: {fmt(read_u64(client, 0x5464, s), 100, 'kWh')}")
    print(f"  Active import L3: {fmt(read_u64(client, 0x5468, s), 100, 'kWh')}")
    print(f"  Active export L1: {fmt(read_u64(client, 0x546C, s), 100, 'kWh')}")
    print(f"  Active export L2: {fmt(read_u64(client, 0x5470, s), 100, 'kWh')}")
    print(f"  Active export L3: {fmt(read_u64(client, 0x5474, s), 100, 'kWh')}")
    print(f"  Active net L1:    {fmt(read_s64(client, 0x5478, s), 100, 'kWh')}")
    print(f"  Active net L2:    {fmt(read_s64(client, 0x547C, s), 100, 'kWh')}")
    print(f"  Active net L3:    {fmt(read_s64(client, 0x5480, s), 100, 'kWh')}")

    print("\n--- Energia bierna per faza ---")
    print(f"  Reactive import L1: {fmt(read_u64(client, 0x5484, s), 100, 'kvarh')}")
    print(f"  Reactive import L2: {fmt(read_u64(client, 0x5488, s), 100, 'kvarh')}")
    print(f"  Reactive import L3: {fmt(read_u64(client, 0x548C, s), 100, 'kvarh')}")
    print(f"  Reactive export L1: {fmt(read_u64(client, 0x5490, s), 100, 'kvarh')}")
    print(f"  Reactive export L2: {fmt(read_u64(client, 0x5494, s), 100, 'kvarh')}")
    print(f"  Reactive export L3: {fmt(read_u64(client, 0x5498, s), 100, 'kvarh')}")
    print(f"  Reactive net L1:    {fmt(read_s64(client, 0x549C, s), 100, 'kvarh')}")
    print(f"  Reactive net L2:    {fmt(read_s64(client, 0x54A0, s), 100, 'kvarh')}")
    print(f"  Reactive net L3:    {fmt(read_s64(client, 0x54A4, s), 100, 'kvarh')}")

    print("\n--- Energia pozorna per faza ---")
    print(f"  Apparent import L1: {fmt(read_u64(client, 0x54A8, s), 100, 'kVAh')}")
    print(f"  Apparent import L2: {fmt(read_u64(client, 0x54AC, s), 100, 'kVAh')}")
    print(f"  Apparent import L3: {fmt(read_u64(client, 0x54B0, s), 100, 'kVAh')}")
    print(f"  Apparent export L1: {fmt(read_u64(client, 0x54B4, s), 100, 'kVAh')}")
    print(f"  Apparent export L2: {fmt(read_u64(client, 0x54B8, s), 100, 'kVAh')}")
    print(f"  Apparent export L3: {fmt(read_u64(client, 0x54BC, s), 100, 'kVAh')}")
    print(f"  Apparent net L1:    {fmt(read_s64(client, 0x54C0, s), 100, 'kVAh')}")
    print(f"  Apparent net L2:    {fmt(read_s64(client, 0x54C4, s), 100, 'kVAh')}")
    print(f"  Apparent net L3:    {fmt(read_s64(client, 0x54C8, s), 100, 'kVAh')}")

    client.close()
