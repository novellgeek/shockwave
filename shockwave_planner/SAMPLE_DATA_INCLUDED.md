# SHOCKWAVE v1.1 - Sample Data Reference

## 🌍 Multi-National Launch Data Included!

SHOCKWAVE v1.1 comes pre-loaded with **17 sample launches** from China, USA, and Russia spanning November-December 2025.

---

## 🇨🇳 China (8 Launches)

**Launch Sites**:
- Jiuquan (4 launches)
- Taiyuan (2 launches)
- Xichang (1 launch)
- Wenchang (1 launch)

**Sample Missions**:
- **2025-11-05**: Tianqi-27 (Kinetica-1) ✅ Success
- **2025-11-13**: Gaofen-12E (Long March 6C) ✅ Success
- **2025-11-22**: Tianhui-6B (Long March 2C) 📅 Scheduled
- **2025-11-26**: Beidou-3 M26 (Long March 3B/E) 🟢 Go
- **2025-11-28**: Jilin-1 GF06 (Ceres-1) 🟡 NET
- **2025-12-05**: Tianzhou-9 (Long March 7) 📅 Scheduled
- **2025-12-12**: Yaogan-41 (Long March 4C) 📅 Scheduled
- **2025-12-18**: Shenzhou-20 (Long March 2F/G) 🟡 NET

**Rockets Included**:
- Long March 2C, 2F/G, 3B/E, 4C, 6C, 7
- Ceres-1 (Galactic Energy)
- Kinetica-1 (Space Pioneer)

---

## 🇺🇸 USA (5 Launches)

**Launch Sites**:
- Cape Canaveral LC-39A (2 launches)
- Cape Canaveral SLC-40 (1 launch)
- Vandenberg SLC-4E (1 launch)
- Kennedy LC-39B (1 launch)

**Sample Missions**:
- **2025-11-30**: Starlink Group 6-72 (Falcon 9) ✅ Success
  - NOTAM: A2156/25
  - 23 Starlink satellites to LEO
  - Successful drone ship landing

- **2025-12-03**: NROL-126 (Falcon 9) 📅 Scheduled
  - NOTAM: A2187/25
  - Classified NRO payload to SSO
  - National Reconnaissance Office

- **2025-12-08**: GPS III SV09 (Falcon 9) 🟢 Go
  - NOTAM: A2201/25
  - GPS navigation satellite to MEO
  - US Space Force mission

- **2025-12-15**: Dream Chaser EAC-1 (Vulcan Centaur) 🟡 NET
  - NOTAM: A2234/25
  - Dream Chaser cargo spacecraft
  - First ISS cargo mission

- **2025-12-20**: Europa Clipper (Falcon Heavy) 📅 Scheduled
  - NOTAM: A2267/25
  - Europa science probe
  - Jupiter system exploration

**Rockets Included**:
- Falcon 9 Block 5 (reusable)
- Falcon Heavy (heavy-lift)
- Vulcan Centaur (ULA next-gen)
- Atlas V 541 (ULA)

---

## 🇷🇺 Russia (4 Launches)

**Launch Sites**:
- Baikonur Site 31/6 (1 launch)
- Baikonur Site 1/5 (1 launch)
- Plesetsk Site 43/4 (1 launch)
- Vostochny Site 1S (1 launch)

**Sample Missions**:
- **2025-11-29**: Progress MS-29 (Soyuz-2.1a) ✅ Success
  - NOTAM: R1145/25
  - ISS cargo resupply
  - Successful docking

- **2025-12-05**: Meteor-M N2-4 (Soyuz-2.1b) 📅 Scheduled
  - NOTAM: R1178/25
  - Weather satellite to SSO
  - Polar meteorological mission

- **2025-12-10**: Yamal-601 (Proton-M) 🟢 Go
  - NOTAM: R1203/25
  - Communications satellite to GTO
  - Gazprom Space Systems

- **2025-12-18**: Arktika-M N3 (Angara A5) 📅 Scheduled
  - NOTAM: R1256/25
  - Arctic monitoring satellite to HEO
  - Highly elliptical orbit

**Rockets Included**:
- Soyuz-2.1a (workhorse)
- Soyuz-2.1b (enhanced)
- Proton-M (heavy-lift)
- Angara A5 (modern heavy-lift)

---

## 📊 Database Statistics

**Total Launches**: 17
- China: 8 (47%)
- USA: 5 (29%)
- Russia: 4 (24%)

**By Status**:
- ✅ Success: 3
- 🟢 Go: 3
- 📅 Scheduled: 8
- 🟡 NET: 2
- Pending: 1

**By Orbit**:
- LEO: 6
- SSO: 3
- GTO: 2
- MEO: 1
- HEO: 1
- GEO: 0
- Lunar: 0
- Other: 1

**NOTAM References**: All launches include NOTAM references
- China: Sample NOTAMs not included (add your own)
- USA: A2156/25, A2187/25, A2201/25, A2234/25, A2267/25
- Russia: R1145/25, R1178/25, R1203/25, R1256/25

---

## 🎯 Timeline View Demonstration

When you open Timeline View, you'll see:

```
▼ China              [4 expanded sites showing 8 launches]
  Jiuquan - SLS-1
  Jiuquan - LS-95
  Taiyuan - LA-9A
  Wenchang - LC-201
  ...

▶ USA                [Collapsed - click to expand]

▶ Russia             [Collapsed - click to expand]
```

**Click ▶ to expand USA**:
```
▼ USA                [4 sites showing 5 launches]
  Cape Canaveral - LC-39A
  Cape Canaveral - SLC-40
  Vandenberg - SLC-4E
  Kennedy - LC-39B
```

**Click ▶ to expand Russia**:
```
▼ Russia             [4 sites showing 4 launches]
  Baikonur - Site 31/6
  Baikonur - Site 1/5
  Plesetsk - Site 43/4
  Vostochny - Site 1S
```

---

## 🔧 Adding More Data

**Option 1: Manual Entry**
- Click "➕ New Launch"
- Fill in all fields including NOTAM
- Save

**Option 2: Space Devs Import** (Python)
```python
from data.spacedevs_import import SpaceDevsImporter
importer = SpaceDevsImporter(db)
launches = importer.fetch_upcoming_launches(50)
stats = importer.import_batch(launches)
```

**Option 3: Custom Script**
- See `populate_sample_data.py` for examples
- Add your own sites, rockets, and launches

---

## ✨ What This Demonstrates

**Multi-National Operations**:
- Track launches from all major space powers
- Compare activity levels across countries
- See global launch cadence at a glance

**Country Grouping**:
- Organized view by nation
- Expand/collapse for focused analysis
- Easy comparison of different programs

**Realistic Data**:
- Real rocket types with accurate specs
- Authentic mission names
- Proper NOTAM references
- Diverse orbit types

**Timeline Visualization**:
- See monthly launch density
- Identify busy periods
- Pad turnaround visualization
- Multi-country coordination view

---

## 🎓 Try These Actions

1. **Expand all three countries** - See the full global picture
2. **Filter to "Previous 7 Days"** - See recent launches (Success status)
3. **Search for "Falcon"** - Find all SpaceX launches
4. **Search for a NOTAM** - Type "A2156" to find Starlink mission
5. **Click a launch** - View/edit full details
6. **Adjust pad turnaround** - See how it affects the timeline

---

**Enjoy exploring the global launch landscape!** 🚀🌍
