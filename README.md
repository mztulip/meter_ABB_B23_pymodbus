# meter_ABB_B23_pymodbus

Simple Python utility to read register values from ABB B23/B24 energy meters via Modbus RTU over RS485.

## Requirements

- ABB B23/B24 meter connected via RS485 to `/dev/ttyUSB0`
- Slave ID: 1, 9600 baud, no parity

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Instantaneous values

Reads phase voltages, currents, active/reactive/apparent power, frequency, phase angles, power factor, and current quadrant.

```bash
python b23read2.py
```

### Energy accumulators

Reads total energy registers: active/reactive/apparent import, export and net, plus CO2 and currency accumulators. Unsupported registers (e.g. export on import-only meter variants) show as `N/A`.

```bash
python b23energy.py
```

## Notes

- Requires `pymodbus==3.13` and `pyserial==3.5`
- Tested with ABB B23/B24 meters (Modbus RTU, function code 3)
- Register map based on document `2CMC485003M0201` (User Manual Rev. E, 2025-11-07)
