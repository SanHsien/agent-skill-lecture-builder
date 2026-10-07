**English** | [繁體中文](README.md)

# Course Page Generator (SanHsien Maintenance Fork)

<div align="center">

[![CI](https://github.com/SanHsien/agent-skill-lecture-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/agent-skill-lecture-builder/actions/workflows/ci.yml)
[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE)

</div>

This project is a Windows-first maintenance fork of [`deancourse/agent-skill-lecture-builder`](https://github.com/deancourse/agent-skill-lecture-builder), licensed under the ISC License. It provides reproducible Windows 11 development gates, CI workflows, and upstream change tracking. The primary Traditional Chinese documentation is located in [`README.md`](README.md), and maintenance decisions are documented in [`FORK.md`](FORK.md).

> [!NOTE]
> 📺 **Accompanying Video Tutorial** — [YouTube Video](https://youtu.be/0pZri5f_tfk)

Provide a lecture topic or Markdown notes, and generate a standalone, responsive single-page HTML course website via Agent Skills with zero external build dependencies.

## Table of Contents

- [Quick Start](#quick-start)
- [Local Maintenance & Development (Windows 11)](#local-maintenance--development-windows-11)
- [Project Structure](#project-structure)
- [Adding a New Course](#adding-a-new-course)
- [Configuration Layering](#configuration-layering)
- [Markdown Syntax](#markdown-syntax)

## Quick Start

```bash
# Install optional dev dependencies (Puppeteer is needed for OG image generation)
npm install
```

In your AI chat window (e.g. Codex, Claude, Cursor, Antigravity), request "generate a course page", and the `course-page-generator` Skill will automatically execute the necessary workflow.

### Scenario 1: Topic Only (Zero to Hero)

Provide only a topic, and AI drafts the complete structured content:

```
Act as a cybersecurity expert skilled at explaining concepts with practical examples. Design a lecture website on "Generative AI Security", and start preview upon completion.
```

### Scenario 2: Existing Notes (Assisted Transformation)

Provide existing draft notes, slides, or transcript outlines:

```
Please transform these lecture notes into a structured course page (paste content or provide file path).
```

## Local Maintenance & Development (Windows 11)

Initialize the environment and run gates in one click:

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

Run gate checks manually:

```powershell
pwsh -NoProfile -File tools\dev_check.ps1
pwsh -NoProfile -File tools\test_product.ps1
```

See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for full development documentation.

## Project Structure

```
agent-skill-lecture-builder/
├── .agents/
│   └── skills/
│       └── course-page-generator/
│           ├── scripts/
│           │   ├── build.mjs        # Course page builder (pure Node.js ESM)
│           │   ├── dev.mjs          # Local dev server with live reload
│           │   └── generate-og.mjs  # Generates 1200x630 OG image card
│           └── reference/
│               ├── base.html        # HTML template
│               ├── components.md    # Component specifications
│               ├── config-example.yaml
│               └── content-example.md
├── config/
│   ├── global.yaml          # Global config (instructor, socials, footer)
│   └── assets/              # Shared assets (avatars, icons)
├── example/                 # Example course directory
│   ├── config.yaml          # Course-specific config (overrides global)
│   ├── content.md           # Structured Markdown lecture
│   ├── README.md            # Raw draft notes
│   └── index.html           # Generated course page
├── tools/                   # Windows gate and maintenance tools
├── package.json
└── README.md
```

## Adding a New Course

```bash
mkdir -p my-course/assets
```

1. **Create `my-course/content.md`** — Write lecture using the structured Markdown syntax.
2. **Create `my-course/config.yaml`** — Specify field overrides.
3. **Build**

```bash
node .agents/skills/course-page-generator/scripts/build.mjs my-course
```

Outputs `my-course/index.html`.

To start local preview:

```bash
node .agents/skills/course-page-generator/scripts/dev.mjs my-course
```

## Configuration Layering

Two layers, deep merge:

| Layer | File | Content |
|---|---|---|
| Global | `config/global.yaml` | Instructor bio, socials, footer |
| Course | `<dir>/config.yaml` | Title, badge, hero title, quotes, custom nav |

Course config only needs to override desired fields; others are inherited from global. Array fields (like `socials`) are replaced entirely.

## Markdown Syntax

| Syntax | Description |
|---|---|
| `# LABEL: TITLE` | Major section header |
| `> lead text` (directly below `#`) | Section lead intro |
| `## Title` | Sub-section header |
| `### 🔧 Title` | Card block |
| `` ```prompt [label="..."] `` | Terminal / Prompt box |
| `> **Bold Title**` | Callout / Insight box |
| `[flow]...[/flow]` | Flow step diagram |
| `[tags]...[/tags]` | Badge tags (`green / orange / purple / blue`) |
| `[summary]...[/summary]` | Summary card |
| `[bonus title="..."]...[/bonus]` | Bonus modal button + dialog |
| `[image-text]...[/image-text]` | Side-by-side image and text layout |
| `[youtube id="..." title="..."]` | Responsive 16:9 YouTube video embed |
| `---` | Section divider |

See [`components.md`](./.agents/skills/course-page-generator/reference/components.md) for the full component specification.
