# PCB design guide

This project's roadmap moves Embryo-Zero from a breadboard prototype to a
custom PCB (see [STEP_BY_STEP.md](STEP_BY_STEP.md), stretch goal 8.6, and
[ROADMAP.md](ROADMAP.md) Phase 6). This guide collects the knowledge needed
to make that jump: how a board goes from schematic to a manufactured part
you can bolt sensors and an LED to.

## 1. The design flow

1. **Schematic capture** — draw the circuit as a logical diagram: symbols
   and wires, no physical layout yet. Every net (electrical connection)
   gets a name.
2. **Component selection** — pick real, buyable parts with a footprint
   (physical land pattern), a datasheet, and confirmed stock. Prefer
   parts already used in embryo-zero (DHT22/DS18B20, common LEDs, ESP32
   modules) before introducing new ones.
3. **Footprint / land pattern assignment** — each schematic symbol maps to
   a physical footprint (pad layout) that matches the real package
   (e.g. SOIC-8, 0603 resistor, JST-PH connector).
4. **PCB layout** — place footprints on a physical board outline, then
   route copper traces between the pads that the schematic says should
   connect.
5. **Design rule check (DRC)** — automated check that trace widths,
   spacing, and drill sizes meet the fab's capabilities and don't violate
   your own electrical rules.
6. **Generate manufacturing files** — Gerbers (copper/mask/silkscreen
   layers), drill files, and a pick-and-place / BOM file if you want the
   board assembled, not just fabricated.
7. **Fab + assembly** — send files to a PCB manufacturer; solder parts by
   hand, reflow oven, or pay the fab's assembly service.
8. **Bring-up and test** — power the board through a current-limited
   supply first, check voltages before installing expensive ICs, then
   test each subsystem in isolation.

## 2. Core concepts

- **Net** — a set of pins that are electrically the same point. A
  schematic is really just a big list of nets.
- **Layer stack-up** — a board is copper layers separated by insulating
  substrate (FR4). A hobby board is usually **2-layer** (top + bottom
  copper). 4-layer adds internal power/ground planes for cleaner signal
  integrity and is worth it once you add a microcontroller with fast
  digital signals or need better EMI behavior.
- **Trace width and current capacity** — wider copper carries more
  current without excessive heating. Rule of thumb for external 1oz
  copper: ~0.4mm (16 mil) per amp is a conservative starting point for
  low-voltage hobby boards; use a trace-width calculator (IPC-2221) for
  anything carrying real current (motors, heaters, battery charging).
- **Via** — a plated hole that connects copper on different layers.
- **Ground plane** — a large area of copper tied to ground. Gives
  return current a low-impedance path and shields signals; almost always
  worth using on the bottom layer even for a simple 2-layer board.
- **Decoupling capacitors** — a 0.1µF ceramic capacitor placed close to
  every IC's power pin absorbs high-frequency switching noise. Cheap and
  non-optional on anything with a microcontroller or radio.
- **Pull-up / pull-down resistors** — needed on open-drain lines (I2C
  SDA/SCL, many sensor interrupt pins) so the line has a defined level
  when nothing is actively driving it.
- **Silkscreen** — the printed labels on the board surface; use it to
  mark polarity, connector pinouts, and test points so a future builder
  (or you, in six months) doesn't need the schematic to debug the board.

## 3. Design rules and tolerances (typical 2-layer hobby fab)

| Parameter | Typical minimum | Notes |
|---|---|---|
| Trace width / spacing | 0.15mm (6 mil) | 0.25mm+ is safer for hand-soldered boards |
| Drill size | 0.3mm | Match to the smallest through-hole part you use |
| Annular ring | 0.15mm | Copper ring around a drilled hole |
| Board thickness | 1.6mm standard | Thinner boards flex; fine for small boards |
| Solder mask clearance | fab default | Don't override unless you know why |

Always check the actual capability table of the fab you're using — these
vary by manufacturer and by price tier (cheaper = looser tolerances).

## 4. Practical layout guidance for Embryo-Zero-style boards

- **Group by function first.** Keep the power section (regulator, input
  connector, bulk capacitors) together, the sensor interface together,
  and the microcontroller/SBC interface together. Route power first,
  then signal.
- **Keep analog and digital sections separated** if you add analog
  sensors — route digital switching traces away from analog sense lines,
  and don't route noisy traces under an analog IC.
- **Star-ground or single-point return for sensitive analog** — for a
  simple sensor + LED board this is rarely critical, but it matters once
  you add anything measuring small voltages.
- **Connector footprints must match your actual cable/header** — verify
  pin pitch (2.54mm / 0.1" is the hobby default) before ordering.
- **Leave mounting holes and keep-out zones** if the board goes in an
  enclosure — decide the enclosure early, since it constrains board
  outline and connector placement.
- **Panelization** — if ordering multiple boards, most fabs will
  panelize (tile) small boards for you automatically; you don't need to
  design this yourself for a first run.

## 5. Recommended tools

- **KiCad** — free, open source, cross-platform. The default choice for
  an open-hardware project like this one (matches the CERN OHL v2
  license already used in this repo). Handles schematic, layout, 3D
  preview, and Gerber export in one package.
- **EasyEDA** — free, browser-based, tightly integrated with JLCPCB
  ordering and their component/assembly library. Good for very fast
  first boards.
- **Fusion 360 Electronics / Altium** — professional-grade, useful to
  know exist but not necessary for this project's scale.

## 6. From breadboard to PCB, step by step for this project

1. Finalize the breadboard circuit in `embryo-zero/hardware/` (sensor +
   LED + SBC/MCU wiring) and confirm it works reliably.
2. Redraw the confirmed wiring as a KiCad schematic — one symbol per
   part, one net per wire.
3. Assign footprints (DHT22 typically uses a 3-pin JST or header;
   ESP32 modules have vendor-published footprints).
4. Lay out a board outline sized to the enclosure or breadboard
   footprint you're replacing.
5. Route power first, decoupling capacitors next to every IC, then
   signal traces.
6. Run DRC, fix violations, then generate Gerbers + drill files + BOM.
7. Order a small batch (3-10 boards) from a hobby fab (e.g. JLCPCB,
   PCBWay, OSH Park).
8. Hand-solder the first board, bring it up on a current-limited supply,
   and verify each subsystem against the same firmware used on the
   breadboard version (`embryo-zero/firmware/`).
9. Document the board: schematic PDF, board photos, and a short log —
   same documentation habit already used for the breadboard builds.

## 7. Further reading

- KiCad official documentation and "Getting Started" guide
- IPC-2221 (generic standard for PCB design, trace width tables)
- Your chosen fab's design-rule and capability page (read before your
  first layout, not after)
