# Adobe XD Scenegraph Toolkit

A toolkit for developers working with Adobe XD, including a scenegraph extractor and a detailed data format specification. This repository provides a detailed format reference and a practical extraction tool.

## AXDS Extractor (Adobe XD Scenegraph Extractor)

A lightweight, dependency-free tool to extract and consolidate scenegraph data from Adobe XD (`.xd`) files. It provides both a Command-Line Interface (CLI) for automation and a simple Graphical User Interface (GUI) for manual use.

### Key Features

* Extracts all `graphicContent.agc` files from an `.xd` archive.
* Consolidates all found scenegraph data into a single, comprehensive `all_graphic_content.json` file.
* Extracts key metadata files like `manifest`, `interactions.json`, and `metadata.xml`.
* Creates a `_extraction_info.json` file with a summary of the extraction process.

### Requirements

* Python 3.6+
* No external libraries are required. The tool uses only Python's standard library.

### Usage

The tool consists of two main files: `core_extractor.py` (the core logic and CLI) and `gui.py` (the graphical wrapper).

#### 1. Command-Line Interface (CLI)

The CLI is ideal for automation and integration into other scripts.

**Command:**

```bash
python core_extractor.py --input "path/to/your/design.xd" --output "path/to/your/output_folder"
````

**Arguments:**

- `-i`, `--input`: (Required) The full path to the input `.xd` file.
- `-o`, `--output`: (Required) The full path to the directory where extracted files will be saved.

#### 2. Graphical User Interface (GUI)

The GUI provides a simple point-and-click interface for manual extractions.

**Launch Command:**

Bash

```
python gui.py
```

**Steps:**

1. Run the `gui.py` script.
2. Click the first **"Browse..."** button to select your `.xd` file.
3. Click the second **"Browse..."** button to select an output directory.
4. Click the **"Extract"** button to begin the process.
5. A message box will appear upon completion or if an error occurs.

---

## Adobe XD Scenegraph Description Format

### Technical Reference

This reference has been updated based on analysis of multiple real-world projects.

### 1. Core Concepts

#### 1.1. The Scenegraph

The core of the format is a hierarchical tree of nodes (a scenegraph) that represents the visual elements. The primary scenegraph for each artboard is found within its corresponding `graphicContent.agc` file.

#### 1.2. Resources

A special section, typically in `resources/graphics/graphicContent.agc`, acts as a central library for the entire document. It contains definitions for:

- **Master Components (`symbols`):** The blueprint for all reusable components.
- **Document Assets (`documentLibrary`):** Centralized colors, character styles, etc.
- **Reusable Gradients and other assets.**

#### 1.3. Components (Symbols)

XD uses a powerful master-instance model for components.

- **Master Component:** Defined once in the `resources.symbols` array. It has `isMaster: true` and contains definitions for all its states and interactions.
- **Component Instance (`syncRef`):** An instance of a master component placed on an artboard. It has a `type` of `"syncRef"` and a `ref` property pointing to the `id` of the master component.

### 2. Root Structure

The root JSON object is a dictionary where keys are the paths to `graphicContent.agc` files. Each of these contains a scenegraph with a `version`, a `children` array (usually holding artboards), and a `resources` object.

JSON

```
{
  "artwork/artboard-id/graphics/graphicContent.agc": {
    "version": "1.5.0",
    "children": [ ... ],
    "resources": { ... }
  },
  "resources/graphics/graphicContent.agc": {
    "resources": {
      "symbols": [ ... ],
      "documentLibrary": { ... }
    }
  }
}
```

### 3. Node Reference

#### 3.1. Common Node Properties

|   |   |   |
|---|---|---|
|**Property**|**Type**|**Description**|
|`id`|`string`|A unique identifier for the node.|
|`name`|`string`|The layer name as set in Adobe XD.|
|`type`|`string`|The node type (e.g., `"shape"`, `"text"`, `"group"`).|
|`transform`|`object`|An affine transformation matrix defining position, scale, and rotation.|
|`visible`|`boolean`|Determines if the node is visible (defaults to `true`).|
|`opacity`|`number`|The node's opacity, from 0 (transparent) to 1 (opaque).|
|`style`|`object`|Contains all visual styling properties like `fill`, `stroke`, `effects`.|
|`meta.ux.symbolId`|`string`|For component instances, this ID links it to the master symbol.|

#### 3.2. Artboard

The top-level container for a screen. In some files, the `children` are nested inside an `artboard` object.

- **Key Properties**: `width`, `height`, `children`.
- **`meta.ux.scrollingType`**: Can be `"vertical"`, `"horizontal"`, or `"panning"`.

#### 3.3. Shape

Represents all vector graphics.

|   |   |   |
|---|---|---|
|**Shape Type**|**Key Properties**|**Description**|
|`rect`|`x`, `y`, `width`, `height`, `r`|A rectangle. `r` is an array of corner radii.|
|`ellipse`|`cx`, `cy`, `rx`, `ry`|An ellipse defined by its center and radii.|
|`path`|`path`|A custom vector shape defined by an SVG-like path string.|
|`line`|`x1`, `y1`, `x2`, `y2`|A straight line between two points.|
|`polygon`|`points`, `n`|A regular polygon with `n` sides.|

#### 3.4. Text

- **`rawText`**: The string content.
- **`paragraphs` & `styleRuns`**: Defines rich text with multiple styles in a single block.
- **`textAlign`**: `"left"`, `"center"`, `"right"`.
- **`lineAlign`**: Vertical alignment, e.g., `"leading"`.
- **`frame.type`**: Sizing behavior, e.g., `"auto-height"`, `"auto-width"`.

#### 3.5. Group

A container for other nodes. It can have its own `style` and `effects`.

- **`style.isolation`**: A property found on groups, e.g., `"isolate"`.

#### 3.6. Component Instance (`syncRef`)

- **`type`**: `"syncRef"`.
- **`ref`**: The `id` of the master component this instance is linked to.
- **`state`**: An object (`{ "id": "...", "name": "..." }`) specifying which state of the master component is active.

### 4. Resources Section In-Depth

#### 4.1. Master Components (`resources.symbols`)

This is an array where each object is a master component definition.

- **`isMaster: true`**: Identifies it as a master.
- **`children`**: The layers that make up the component.
- **`states`**: An array of all possible states for this component, including the default.
- **`meta.ux.interactions`**: A critical array defining all interactions for this component. See Section 6.

#### 4.2. Document Assets (`resources.documentLibrary`)

A centralized store for design system tokens.

- **`elements`**: Contains definitions for shared colors and character styles.
- **`colorSwatches`**: An array of color definitions, often organized into groups.

### 5. Styling In-Depth

#### 5.1. Fill & Stroke

- **`fill`**: Can be `solid`, `gradient`, or `pattern`.
- **`stroke`**: Besides `width` and `color`, it includes:
    - `type`: Can be `"solid"` or `"none"` to disable it.
    - `align`: `"inside"`, `"outside"`, `"center"`.
    - `join`: `"miter"`, `"round"`, `"bevel"`.
    - `cap`: `"butt"`, `"round"`, `"square"`.
    - `dash`: An array defining a dashed pattern, e.g., `[10, 5]`.

#### 5.2. Effects (`style.effects`)

An array of filter objects. Each object has `visible` and `params`.

|   |   |
|---|---|
|**Effect Type**|**Description**|
|`dropShadow`|A standard drop shadow effect.|
|`uxdesign#innerShadow`|An inner shadow effect.|
|`uxdesign#blur`|An object or background blur. `backgroundEffect: true` enables the "frosted glass" effect.|

### 6. Interactions

Defined within master components (`resources.symbols[...].meta.ux.interactions`). An interaction object has:

- **`triggerEvent`**: The user input that fires the interaction, e.g., `"tap"`, `"hover"`, `"drag"`.
- **`action`**: What the interaction does.
    - `"state-transition"`: Switches the component to a different state.
    - `"artboard-transition"`: Navigates to a different artboard.
    - `"overlay-transition"`: Shows another artboard as an overlay.
- **`properties`**: Details of the action.
    - `destination`: The target `id` for a transition (artboard or state).
    - `transition`: The animation style (`"auto-animate"`, `"dissolve"`, `"slideLeft"`).
    - `duration`: Animation length in seconds.
    - `easing`: The easing function (`"ease-out"`, `"linear"`, `"bounce"`).
