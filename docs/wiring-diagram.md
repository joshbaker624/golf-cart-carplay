# Hardware Wiring Guide for Golf Cart CarPlay System

## Power Connections

### Golf Cart Power (12V/48V to 5V Conversion)

```
Golf Cart Battery (+) ──┬── Fuse (5A) ──┬── DC-DC Converter ──┬── RPi 5V
                        │               │   (12V/48V to 5V)   │
Golf Cart Battery (-) ──┴───────────────┴────────────────────┴── RPi GND
```

**Components:**
- DC-DC Buck Converter (12V/48V to 5V, 3A minimum)
- 5A automotive fuse
- 18-20 AWG wire for power connections

## Display Connections

### Official Raspberry Pi 7" Touchscreen

```
Raspberry Pi 4          Display Board
┌─────────────┐        ┌──────────────┐
│ DSI Port    ├────────┤ DSI Ribbon   │
│             │        │              │
│ GPIO 2 (5V) ├────────┤ 5V Power     │
│ GPIO 6 (GND)├────────┤ GND          │
│             │        │              │
│ GPIO 3 (SDA)├────────┤ SDA (Touch)  │
│ GPIO 5 (SCL)├────────┤ SCL (Touch)  │
└─────────────┘        └──────────────┘
```

### Alternative HDMI Display

```
Raspberry Pi 4          HDMI Display
┌─────────────┐        ┌──────────────┐
│ HDMI 0      ├────────┤ HDMI Input   │
│             │        │              │
│ USB Port    ├────────┤ USB (Touch)  │
└─────────────┘        └──────────────┘
```

## Audio Connections

### USB Audio Interface (Recommended)

```
Raspberry Pi 4          USB Audio Card         Amplifier          Speakers
┌─────────────┐        ┌──────────────┐      ┌──────────┐      ┌─────────┐
│ USB Port    ├────────┤ USB Input    │      │ Line In  ├──────┤ Left    │
│             │        │              │      │          │      │         │
│             │        │ Line Out ────┼──────┤          │      │ Right   │
└─────────────┘        └──────────────┘      └──────────┘      └─────────┘
```

### Direct 3.5mm Audio (Lower Quality)

```
Raspberry Pi 4                              Amplifier
┌─────────────┐                            ┌──────────┐
│ 3.5mm Jack  ├────── 3.5mm to RCA ───────┤ Input    │
└─────────────┘                            └──────────┘
```

## GPS Module Connection

### USB GPS Module (Easiest)

```
Raspberry Pi 4          USB GPS Module
┌─────────────┐        ┌──────────────┐
│ USB Port    ├────────┤ USB Connector│
└─────────────┘        └──────────────┘
```

### GPIO GPS Module

```
Raspberry Pi 4          GPS Module (UART)
┌─────────────┐        ┌──────────────┐
│ GPIO 14 (TX)├────────┤ RX           │
│ GPIO 15 (RX)├────────┤ TX           │
│ GPIO 1 (3V3)├────────┤ VCC          │
│ GPIO 6 (GND)├────────┤ GND          │
└─────────────┘        └──────────────┘
```

## iPhone/CarPlay Connection

```
Raspberry Pi 4          Lightning Cable        iPhone
┌─────────────┐        ┌──────────────┐      ┌─────────┐
│ USB 3.0     ├────────┤ USB-A        │      │Lightning│
│ (Blue Port) │        │              ├──────┤ Port    │
└─────────────┘        └──────────────┘      └─────────┘
```

**Important:** Use a high-quality MFi-certified Lightning cable for reliable CarPlay connection.

## Complete Wiring Diagram

```
                          Golf Cart CarPlay System
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  Golf Cart Battery ─── Fuse ─── DC-DC Converter ─── 5V     │
    │                                           │                 │
    │                                    ┌──────┴──────┐          │
    │   ┌──────────────┐                │ Raspberry   │          │
    │   │ 7" Display   ├────DSI─────────┤    Pi 4     │          │
    │   │              ├────I2C─────────┤             │          │
    │   └──────────────┘                │  ┌────┐     │          │
    │                                   │  │USB │     │          │
    │   ┌──────────────┐                │  │    │     │          │
    │   │ USB Audio    ├────USB─────────┤  │    │     │          │
    │   └──────┬───────┘                │  │    │     │          │
    │          │                        │  │    │     │          │
    │   ┌──────┴───────┐                │  │    │     │          │
    │   │ Amplifier    ├── Speakers ───┤  │    │     │          │
    │   └──────────────┘                │  │    │     │          │
    │                                   │  │    │     │          │
    │   ┌──────────────┐                │  │    │     │          │
    │   │ GPS Module   ├────USB─────────┤  │    │     │          │
    │   └──────────────┘                │  │    │     │          │
    │                                   │  │    │     │          │
    │   ┌──────────────┐                │  │    │     │          │
    │   │   iPhone     ├────USB─────────┤  └────┘     │          │
    │   └──────────────┘                └─────────────┘          │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

## Installation Tips

1. **Power Management**
   - Always use a fuse between battery and converter
   - Consider adding a power switch for easy on/off
   - Use capacitors on power input to handle voltage spikes

2. **Mounting**
   - Mount display at eye level when seated
   - Ensure all connections are secure for vibration resistance
   - Use weatherproof enclosures if exposed to elements

3. **Cable Management**
   - Use cable ties to secure all wiring
   - Route cables away from moving parts
   - Leave some slack for vibration absorption

4. **Grounding**
   - Connect all ground points to a common ground
   - Use the golf cart chassis as ground if metal frame
   - Ensure good electrical contact at ground points

## Safety Warnings

⚠️ **IMPORTANT SAFETY INFORMATION** ⚠️

- Disconnect battery before making any connections
- Use appropriate fuses for all power connections
- Ensure all connections are properly insulated
- Do not operate while driving on public roads
- Mount display where it won't obstruct vision
- Secure all components to prevent movement while driving

## Troubleshooting

### No Power
- Check fuse
- Verify DC-DC converter output (should be 5.1V)
- Check power connections at Pi

### No Display
- Verify DSI cable is properly connected
- Check display power connections
- Try different HDMI port if using HDMI display

### No Touch Response
- Check I2C connections (SDA/SCL)
- Verify touch driver is installed
- Run touch calibration tool

### No Audio
- Check USB audio device recognition: `lsusb`
- Verify audio output selection in settings
- Test with: `speaker-test -t wav -c 2`

### GPS Not Working
- Check GPS module connection
- Verify gpsd is running: `sudo systemctl status gpsd`
- Test GPS: `cgps -s`