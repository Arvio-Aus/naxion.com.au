/*
 * Naxion product catalogue — the single source of truth for every product page.
 *
 * To add a product: copy an entry, give it a unique `id` (used in the URL:
 * product.html?id=<id>), add an image to assets/img/products/, and fill in specs.
 * `specs` is a list of [group, [[label, value], ...]] pairs rendered as tables.
 * `highlights` are the 4 headline figures shown at the top of the product page.
 * `tempCurve` (optional) drives the "capacity vs temperature" chart.
 */
window.NAXION_PRODUCTS = [
  // ------------------------------------------------------------------ CELLS
  {
    id: "nx-p160",
    type: "cell",
    name: "NX-P160",
    title: "160Ah Prismatic Sodium-Ion Cell",
    tagline: "Long-life energy-storage cell with 10,000+ cycles and −40 °C discharge.",
    image: "assets/img/products/nx-p160.svg",
    format: "Prismatic, aluminium case",
    featured: true,
    highlights: [
      ["Capacity", "160 Ah"],
      ["Energy", "480 Wh"],
      ["Cycle life", "≥10,000"],
      ["Discharge temp.", "−40 to 60 °C"],
    ],
    description:
      "The NX-P160 is a large-format prismatic sodium-ion cell built for stationary energy storage. It delivers 480 Wh per cell with over 10,000 cycles at 25 °C and keeps 90% of its capacity at −20 °C. It uses no lithium, cobalt or nickel, and it can be shipped and stored at 0 V for safer logistics.",
    applications: ["Residential & C&I energy storage", "Telecom & data-centre backup", "Off-grid solar", "Cold-climate installations"],
    specs: [
      ["Electrical", [
        ["Nominal capacity", "160 Ah (25 °C, 0.5C/0.5C)"],
        ["Nominal voltage", "3.0 V"],
        ["Rated energy", "480 Wh"],
        ["Charge cut-off voltage", "3.8 ± 0.05 V"],
        ["Discharge cut-off voltage", "1.5 V"],
        ["Internal resistance (AC 1 kHz)", "≤ 0.65 mΩ"],
      ]],
      ["Charge & discharge", [
        ["Standard charge current", "≤ 1C (0 to 45 °C); ≤ 0.2C (−20 to 0 °C)"],
        ["Max. continuous discharge", "3C (480 A)"],
        ["Max. pulse discharge", "6C (960 A), ≤ 30 s"],
        ["Cycle life", "≥ 10,000 cycles (25 ± 2 °C)"],
      ]],
      ["Physical", [
        ["Dimensions (T × W × H)", "71.7 × 173.7 × 207.2 mm"],
        ["Weight", "4.2 ± 0.2 kg"],
        ["Gravimetric energy density", "≥ 114 Wh/kg"],
        ["Terminals", "Aluminium, M6 threaded"],
      ]],
      ["Environmental", [
        ["Charging temperature", "0 to 55 °C"],
        ["Discharging temperature", "−40 to 60 °C"],
        ["Storage temperature", "−20 to 60 °C, < 85% RH"],
        ["Recommended storage SOC", "20–30%, cycle every 6 months"],
      ]],
      ["Safety testing", [
        ["Abuse tests passed", "Over-charge, over-discharge, short-circuit, 130 °C heating, crush, drop, heavy impact, vibration, low pressure"],
        ["Result", "No fire, no explosion"],
      ]],
    ],
    tempCurve: [[-40, 65], [-30, 80], [-20, 90], [-10, 97], [25, 100], [45, 100], [60, 95]],
  },
  {
    id: "nx-p210",
    type: "cell",
    name: "NX-P210",
    title: "210Ah High-Energy Prismatic Cell",
    tagline: "Our highest-energy sodium-ion cell for compact, large-scale storage.",
    image: "assets/img/products/nx-p210.svg",
    format: "Prismatic, aluminium case",
    featured: true,
    highlights: [
      ["Capacity", "210 Ah"],
      ["Energy", "651 Wh"],
      ["Energy density", "≥ 130 Wh/kg"],
      ["Cycle life", "≥ 6,000"],
    ],
    description:
      "The NX-P210 uses an upgraded layered-oxide cathode to fit 651 Wh into a standard 173 mm prismatic footprint. That means fewer cells and connections per kWh, which lowers pack and container costs for utility and commercial projects.",
    applications: ["Utility-scale & C&I storage", "Containerised BESS", "Microgrids"],
    specs: [
      ["Electrical", [
        ["Nominal capacity", "210 Ah (25 °C, 0.5C/0.5C)"],
        ["Nominal voltage", "3.1 V"],
        ["Rated energy", "651 Wh"],
        ["Charge cut-off voltage", "3.95 V"],
        ["Discharge cut-off voltage", "1.5 V"],
        ["Internal resistance (AC 1 kHz)", "≤ 0.5 mΩ"],
      ]],
      ["Charge & discharge", [
        ["Standard charge current", "0.5C"],
        ["Max. continuous charge", "1C"],
        ["Max. continuous discharge", "2C (420 A)"],
        ["Cycle life", "≥ 6,000 cycles (0.5C, 80% EOL)"],
      ]],
      ["Physical", [
        ["Dimensions (T × W × H)", "86.0 × 173.7 × 207.2 mm"],
        ["Weight", "5.0 ± 0.2 kg"],
        ["Gravimetric energy density", "≥ 130 Wh/kg"],
        ["Terminals", "Aluminium, laser-weldable"],
      ]],
      ["Environmental", [
        ["Charging temperature", "−10 to 55 °C"],
        ["Discharging temperature", "−40 to 60 °C"],
        ["Storage temperature", "−20 to 45 °C"],
      ]],
      ["Compliance", [
        ["Transport", "UN38.3"],
        ["Standards", "IEC 62619, GB/T 36276 (pending)"],
      ]],
    ],
    tempCurve: [[-40, 60], [-30, 75], [-20, 88], [-10, 95], [25, 100], [45, 100], [60, 96]],
  },
  {
    id: "nx-p50",
    type: "cell",
    name: "NX-P50",
    title: "50Ah High-Power Prismatic Cell",
    tagline: "High-rate cell for starter, hybrid and UPS applications.",
    image: "assets/img/products/nx-p50.svg",
    format: "Prismatic, aluminium case",
    highlights: [
      ["Capacity", "50 Ah"],
      ["Continuous discharge", "5C"],
      ["Pulse discharge", "10C"],
      ["Cycle life", "≥ 4,000"],
    ],
    description:
      "The NX-P50 is a slim, high-power sodium-ion cell. It has very low internal resistance and excellent cold-cranking performance, which makes it suitable for engine-start batteries, 12/24 V lead-acid replacements, UPS systems and rack modules.",
    applications: ["12/24 V lead-acid replacement", "Engine start & idle-stop", "UPS & telecom", "Rack-mount modules"],
    specs: [
      ["Electrical", [
        ["Nominal capacity", "50 Ah"],
        ["Nominal voltage", "3.0 V"],
        ["Rated energy", "150 Wh"],
        ["Voltage window", "1.5 – 3.95 V"],
        ["Internal resistance (AC 1 kHz)", "≤ 0.8 mΩ"],
      ]],
      ["Charge & discharge", [
        ["Max. continuous charge", "3C"],
        ["Max. continuous discharge", "5C (250 A)"],
        ["Max. pulse discharge", "10C (500 A), ≤ 10 s"],
        ["Cycle life", "≥ 4,000 cycles (1C/1C, 80% EOL)"],
      ]],
      ["Physical", [
        ["Dimensions (T × W × H)", "27.0 × 148.0 × 129.0 mm"],
        ["Weight", "1.2 ± 0.05 kg"],
        ["Gravimetric energy density", "≥ 125 Wh/kg"],
      ]],
      ["Environmental", [
        ["Charging temperature", "−20 to 55 °C"],
        ["Discharging temperature", "−40 to 60 °C"],
      ]],
      ["Compliance", [["Transport", "UN38.3"], ["Standards", "IEC 62619"]]],
    ],
    tempCurve: [[-40, 70], [-30, 83], [-20, 92], [-10, 97], [25, 100], [45, 100], [60, 96]],
  },
  {
    id: "nx-c26",
    type: "cell",
    name: "NX-C26",
    title: "26700 Cylindrical Sodium-Ion Cell",
    tagline: "A standard cylindrical format for modular packs, mobility and tools.",
    image: "assets/img/products/nx-c26.svg",
    format: "Cylindrical 26700, steel can",
    highlights: [
      ["Capacity", "3.5 Ah"],
      ["Nominal voltage", "3.0 V"],
      ["Continuous discharge", "5C"],
      ["Cycle life", "≥ 3,000"],
    ],
    description:
      "The NX-C26 is a 26700 cylindrical sodium-ion cell for pack builders who want automated assembly, good thermal behaviour and dependable cold-weather output. It suits light mobility, power tools, portable power stations and modular backup packs.",
    applications: ["Portable power stations", "E-bikes & light mobility", "Power tools", "Modular backup packs"],
    specs: [
      ["Electrical", [
        ["Nominal capacity", "3.5 Ah"],
        ["Nominal voltage", "3.0 V"],
        ["Rated energy", "10.5 Wh"],
        ["Voltage window", "1.5 – 3.95 V"],
        ["Internal resistance (AC 1 kHz)", "≤ 8 mΩ"],
      ]],
      ["Charge & discharge", [
        ["Standard charge current", "1C"],
        ["Max. continuous discharge", "5C (17.5 A)"],
        ["Max. pulse discharge", "10C, ≤ 10 s"],
        ["Cycle life", "≥ 3,000 cycles (1C/1C, 80% EOL)"],
      ]],
      ["Physical", [
        ["Dimensions", "Ø 26.2 × 70.5 mm"],
        ["Weight", "95 ± 3 g"],
        ["Gravimetric energy density", "≥ 110 Wh/kg"],
      ]],
      ["Environmental", [
        ["Charging temperature", "−10 to 50 °C"],
        ["Discharging temperature", "−40 to 60 °C"],
      ]],
      ["Compliance", [["Transport", "UN38.3"], ["Standards", "IEC 62133-2 (pending)"]]],
    ],
    tempCurve: [[-40, 62], [-30, 78], [-20, 88], [-10, 95], [25, 100], [45, 100], [60, 95]],
  },

  // ------------------------------------------------------------------ PACKS
  {
    id: "nx-w7",
    type: "pack",
    name: "NX-W7",
    title: "7.68 kWh Wall-Mount Home Battery",
    tagline: "A slim 48 V home battery for solar self-consumption and backup.",
    image: "assets/img/products/nx-w7.svg",
    format: "Wall-mount, IP65",
    featured: true,
    highlights: [
      ["Usable energy", "7.68 kWh"],
      ["Nominal voltage", "48 V"],
      ["Cycle life", "≥ 8,000"],
      ["Ingress", "IP65"],
    ],
    description:
      "The NX-W7 packs sixteen NX-P160 cells into a slim wall-mount enclosure with an integrated BMS. Up to 16 units can be connected in parallel (122 kWh). It works with hybrid inverters over CAN and RS485, and its chemistry has no lithium thermal-runaway pathway, so it is well suited to garages and outdoor walls.",
    applications: ["Residential solar storage", "Backup power", "Small business"],
    specs: [
      ["Electrical", [
        ["Cell", "NX-P160 × 16 (16S1P)"],
        ["Nominal energy", "7.68 kWh"],
        ["Nominal voltage", "48 V"],
        ["Operating voltage range", "40 – 59.2 V"],
        ["Max. continuous charge / discharge", "100 A / 150 A"],
        ["Parallel capability", "Up to 16 units"],
      ]],
      ["System", [
        ["BMS", "Integrated, active balancing"],
        ["Communication", "CAN, RS485, Bluetooth app"],
        ["Inverter compatibility", "Common 48 V hybrid inverters (protocol list on request)"],
        ["Cycle life", "≥ 8,000 cycles (0.5C, 25 °C, 80% EOL)"],
      ]],
      ["Physical", [
        ["Dimensions (W × D × H)", "600 × 170 × 880 mm"],
        ["Weight", "≈ 82 kg"],
        ["Ingress protection", "IP65"],
        ["Mounting", "Wall or floor stand"],
      ]],
      ["Environmental", [
        ["Operating temperature", "−30 to 55 °C (charge from 0 °C, self-heating option)"],
        ["Cooling", "Natural convection"],
      ]],
      ["Compliance", [["Standards", "IEC 62619, IEC 62040, UN38.3, AS/NZS 5139 installation ready"], ["Warranty", "10 years"]]],
    ],
  },
  {
    id: "nx-r5",
    type: "pack",
    name: "NX-R5",
    title: "4.8 kWh 19\" Rack-Mount Module",
    tagline: "A 3U, 48 V rack module for telecom, server and modular ESS cabinets.",
    image: "assets/img/products/nx-r5.svg",
    gallery: ["assets/img/products/nx-r5-stack.svg"],
    format: "19\" rack, 3U",
    highlights: [
      ["Energy", "4.8 kWh"],
      ["Nominal voltage", "48 V"],
      ["Form factor", "19\" 3U"],
      ["Cycle life", "≥ 6,000"],
    ],
    description:
      "The NX-R5 fits a standard 19-inch rack and replaces VRLA strings with a lighter, longer-lasting sodium-ion module. It holds up in unconditioned shelters and outdoor cabinets, which helps telecom and edge-compute sites.",
    applications: ["Telecom base stations", "Data-centre & server racks", "Modular ESS", "Off-grid solar"],
    specs: [
      ["Electrical", [
        ["Cell", "NX-P50 × 32 (16S2P)"],
        ["Nominal energy", "4.8 kWh"],
        ["Nominal voltage", "48 V"],
        ["Operating voltage range", "40 – 59.2 V"],
        ["Max. continuous charge / discharge", "100 A / 100 A"],
        ["Parallel capability", "Up to 15 modules"],
      ]],
      ["System", [
        ["BMS", "Integrated, passive balancing"],
        ["Communication", "CAN, RS485 × 2, dry contacts"],
        ["Protection", "DC breaker, pre-charge, reverse-polarity"],
        ["Cycle life", "≥ 6,000 cycles (0.5C, 25 °C, 80% EOL)"],
      ]],
      ["Physical", [
        ["Dimensions (W × D × H)", "442 × 420 × 133 mm (3U)"],
        ["Weight", "≈ 42 kg"],
        ["Ingress protection", "IP20"],
      ]],
      ["Environmental", [
        ["Operating temperature", "−30 to 55 °C"],
        ["Cooling", "Natural convection"],
      ]],
      ["Compliance", [["Standards", "IEC 62619, UN38.3, YD/T 2344 compatible"], ["Warranty", "7 years"]]],
    ],
  },
  {
    id: "nx-m12",
    type: "pack",
    name: "NX-M12",
    title: "12 V 100Ah Drop-In Battery",
    tagline: "A drop-in replacement for 12 V lead-acid with 10× the cycle life.",
    image: "assets/img/products/nx-m12.svg",
    format: "BCI Group 31 case",
    highlights: [
      ["Capacity", "100 Ah"],
      ["Nominal voltage", "12 V"],
      ["Cold cranking", "1,000 A"],
      ["Weight", "≈ 13 kg"],
    ],
    description:
      "The NX-M12 comes in a standard Group 31 case and replaces lead-acid in RVs, marine, caravans and off-grid systems. Sodium-ion's voltage range suits existing 14.4–14.8 V charging profiles, and the battery delivers strong cold-weather power without the low-temperature limits of lithium.",
    applications: ["RV & caravan", "Marine house & start", "Off-grid cabins", "Machinery & fleet"],
    specs: [
      ["Electrical", [
        ["Cell", "NX-P50 × 8 (4S2P)"],
        ["Nominal capacity", "100 Ah"],
        ["Nominal voltage", "12 V"],
        ["Nominal energy", "1.2 kWh"],
        ["Charge voltage", "14.4 – 14.8 V"],
        ["Max. continuous discharge", "200 A"],
        ["Cold cranking amps", "1,000 A (−18 °C)"],
      ]],
      ["System", [
        ["BMS", "Integrated 200 A, low-temp charge protection"],
        ["Connectivity", "Bluetooth app"],
        ["Series / parallel", "Up to 4S / 4P"],
        ["Cycle life", "≥ 4,000 cycles"],
      ]],
      ["Physical", [
        ["Dimensions (L × W × H)", "330 × 172 × 215 mm"],
        ["Weight", "≈ 13 kg"],
        ["Terminals", "M8 stud"],
        ["Ingress protection", "IP67"],
      ]],
      ["Environmental", [
        ["Operating temperature", "−40 to 60 °C (discharge), −20 to 55 °C (charge)"],
      ]],
      ["Compliance", [["Standards", "UN38.3, CE, IEC 62619"], ["Warranty", "5 years"]]],
    ],
  },
  {
    id: "nx-ci115",
    type: "pack",
    name: "NX-CI115",
    title: "115 kWh Commercial & Industrial Cabinet",
    tagline: "An all-in-one outdoor cabinet for peak shaving, solar shifting and backup.",
    image: "assets/img/products/nx-ci115.svg",
    format: "Outdoor cabinet, IP55",
    featured: true,
    highlights: [
      ["Energy", "115.2 kWh"],
      ["Nominal voltage", "720 V"],
      ["Cycle life", "≥ 8,000"],
      ["Fire suppression", "Integrated"],
    ],
    description:
      "The NX-CI115 is a fully integrated commercial battery cabinet. It includes 240 NX-P160 cells, a three-level BMS, thermal management, fire detection and suppression, and an optional 50 kW PCS. Multiple cabinets can run in parallel for MWh-scale sites.",
    applications: ["Peak shaving & demand charge reduction", "Solar time-shifting", "EV charging support", "Microgrids"],
    specs: [
      ["Electrical", [
        ["Cell", "NX-P160 × 240 (240S1P)"],
        ["Nominal energy", "115.2 kWh"],
        ["Nominal voltage", "720 V"],
        ["Operating voltage range", "600 – 888 V"],
        ["Rated power", "50 kW (0.5C)"],
        ["Round-trip efficiency", "≥ 88% (system, AC)"],
      ]],
      ["System", [
        ["BMS", "Three-level (cell / module / rack)"],
        ["PCS", "Optional integrated 50 kW, grid-forming"],
        ["Thermal management", "Air-conditioned, intelligent air flow"],
        ["Fire safety", "Gas & smoke detection, aerosol suppression"],
        ["Communication", "Modbus TCP, CAN, 4G remote monitoring"],
      ]],
      ["Physical", [
        ["Dimensions (W × D × H)", "1,100 × 1,000 × 2,200 mm"],
        ["Weight", "≈ 1,350 kg"],
        ["Ingress protection", "IP55"],
      ]],
      ["Environmental", [
        ["Operating temperature", "−30 to 55 °C"],
        ["Altitude", "≤ 3,000 m"],
      ]],
      ["Compliance", [["Standards", "IEC 62619, IEC 62933, UL 9540A tested, UN38.3"], ["Warranty", "10 years"]]],
    ],
  },
];
