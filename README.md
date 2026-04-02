# SurfacePsycho

![Preview](https://github.com/user-attachments/assets/3e378c30-7f09-4066-b101-409f11a62dfd)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Blender](https://img.shields.io/badge/Blender-4.3+-orange.svg)](https://www.blender.org/)
[![Status](https://img.shields.io/badge/Status-Alpha-red.svg)]()

**SurfacePsycho is a Blender add-on that introduces procedural NURBS surface modeling and CAD interoperability directly into Blender.**  
It enables non-destructive, precision surface design using Geometry Nodes, with support for STEP file workflows.

---

## 🚧 Status

> [!CAUTION]
> **Alpha Status — Expect Instability**
> SurfacePsycho is evolving rapidly since May 2023. Expect breaking changes and file incompatibility between updates. **Always back up your work before upgrading.**

---

## 🧠 Why SurfacePsycho Exists

Blender is powerful for polygon modeling but lacks tools for:
- Precision surface design
- NURBS workflows
- CAD interoperability

SurfacePsycho fills this gap by integrating a procedural NURBS system directly into Blender using Geometry Nodes — keeping everything natively inside `.blend` files.

---

## ⚙️ Key Features

| Feature | Description |
|---|---|
| **Procedural Modeling** | Edit surfaces non-destructively via a polygon cage system |
| **STEP / CAD Support** | Full import and export via OpenCascade |
| **G0 → G4 Continuity** | Professional, smooth transitions between patches |
| **Native Integration** | Powered by Geometry Nodes — files work without the add-on installed |
| **Surface Primitives** | Bezier patches, NURBS patches, and slab presets included |

---

## 🧩 Installation

### Requirements
- Blender **4.3 or newer** (latest version requires Blender 5.0+)

---

### Install via Blender Extensions (Recommended)

1. Open Blender
2. Go to `Edit → Preferences → Get Extensions`
3. Search for **SurfacePsycho**
4. Click **Install**

Or install directly from the [Blender Extensions Platform](https://extensions.blender.org/add-ons/surfacepsycho/)

---

### Install Manually from GitHub

1. Download the latest `.zip` from [GitHub Releases](https://github.com/RomainGuimbal/SurfacePsycho/releases)
2. Open Blender → `Edit → Preferences → Add-ons`
3. Click **Install from Disk** and select the `.zip`

---

### After Installing — Register the Asset Library

> [!IMPORTANT]
> This step is required before you can use SP objects.

1. Go to `Preferences → Add-ons → SurfacePsycho`
2. Click **"Add assets path"**
3. Open your **Asset Browser** — you should see a new SurfacePsycho library

---

### Platform Notes

- **Windows**: OpenCascade is bundled automatically
- **Linux / macOS**: You may need to enable execution permissions. If STEP import/export fails, check add-on preferences

---

## ⚡ Quick Start (First 5 Minutes)

### 0. Setup Asset Library (Do This First)
After installing, you must register the asset library:
- Go to `Preferences → Add-ons → SurfacePsycho`
- Click **"Add assets path"**
- You should now see a new SurfacePsycho library in your Asset Browser

> [!IMPORTANT]
> Skipping this step means SP objects won't appear in your menus.

### 1. Add a Surface
- Press `Shift + A`
- Navigate to **Surface/Curve → SurfacePsycho**
- Choose a primitive:
  - **Bezier Patch** ← recommended for beginners (faster and simpler)
  - NURBS Patch
  - Flat Patch

### 2. Edit the Shape
- Enter **Edit Mode**
- Move vertices of the **polygon cage** (control structure)
- The NURBS surface updates in real-time

### 3. Adjust Parameters
- Open the **Sidebar** (`N` key) → **SurfacePsycho** tab
- Modify continuity, structure, and export settings

---

## 🛠️ Troubleshooting

**"DLL not found" error on startup:**

Navigate to your Blender extensions folder:
```
...\Blender Foundation\Blender\5.0\extensions
```
Delete the `.cache` and `.local` folders. This forces a reinstall of the required Python modules.

**STEP import/export not working on Linux/macOS:**
- Check that execution permissions are enabled
- Review add-on preferences for platform-specific settings

---

## 🧠 Core Concept: The Polygon Cage

SurfacePsycho does **not** work like standard mesh modeling.

You edit a **control structure (the cage)**, not the final geometry.

- The cage defines the surface shape
- Geometry Nodes compute the final NURBS surface procedurally
- All edits are non-destructive

---

## 🔄 Typical Workflow

1. Create a base patch
2. Shape it using the polygon cage
3. Combine multiple surfaces
4. Apply continuity (G0–G4) between surfaces
5. Export to STEP for use in CAD software

---

## 📤 CAD Export

- Use the **"Export STEP"** button in the SurfacePsycho panel (`N panel → SurfacePsycho`)
- Compatible with Rhino, Plasticity, SolidWorks, and other CAD tools

---

## ⚠️ Known Limitations

- Alpha instability — breaking changes expected
- Performance may drop with heavy STEP files
- Limited direct control-point editing
- Circular dependencies between surfaces will break Blender's dependency graph

**To avoid circular dependencies:**  
Use a **Master surface** and drive other surfaces as dependents — never make two surfaces depend on each other.

---

## 📚 Documentation

Full documentation (WIP): [GitHub Wiki](https://github.com/RomainGuimbal/SurfacePsycho/wiki)

Key sections:
- [Install and Setup](https://github.com/RomainGuimbal/SurfacePsycho/wiki/1.-Install-and-Setup)
- [SP Objects](https://github.com/RomainGuimbal/SurfacePsycho/wiki/2.-SP-Objects)
- [Modifiers and Tools](https://github.com/RomainGuimbal/SurfacePsycho/wiki/3.-Modifers-and-Tools)
- [Import and Export](https://github.com/RomainGuimbal/SurfacePsycho/wiki/4.-Import-and-Export)
- [Tips for Better Workflow](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Tips-for-better-workflow)

---

## 🎥 Tutorials & Demos

[Full YouTube Playlist](https://www.youtube.com/playlist?list=PLsTbL26zgwpI6m0qrpZZFmrgf3PaFzuiq)

---

## 🤝 Community & Support

- **Discord**: [Join the SurfacePsycho Dev server](https://discord.gg/MJdxMBM6pm)
- **GitHub Issues**: [Report bugs or request features](https://github.com/RomainGuimbal/SurfacePsycho/issues)
- **BlenderArtists Forum**: [Community discussion](https://blenderartists.org/t/surfacepsycho-addon-project/1487629)

---

## 💛 Support the Project

SurfacePsycho is free and open source.  
If it's useful to you, consider supporting its development:

- [Donate via Gumroad](https://acideromineh.gumroad.com/l/SurfacePsycho)
- [OpenCollective](https://opencollective.com/surfacepsycho)

---

## 🤝 Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

The documentation also needs contributors — feel free to edit the [Wiki](https://github.com/RomainGuimbal/SurfacePsycho/wiki) directly.

---

## 📄 License

GNU General Public License v3.0
