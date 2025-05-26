# Adobe XD Scenegraph Toolkit

A technical reference and specification for the Adobe XD scenegraph data format (JSON), intended for developers building design-to-code tools. This repository provides a detailed format reference and a practical extraction tool.

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

### Technical Reference v1.0

### 1. Definition and Purpose

The Adobe XD Scenegraph is a specialized JSON-like data structure that declaratively describes the structure, properties, and styling of design elements.

- **Source:** The structure is extracted from `.xd` files, primarily from one or more `graphicContent.agc` files within the archive.
- **Purpose:** It serves as a machine-readable blueprint for rendering UIs, managing interactions, and converting designs into other formats.
- **Nature:** The format is declarative—it describes _what_ the design is, not _how_ it should be rendered step-by-step.

### 2. Adobe XD File Architecture

An `.xd` file is a standard ZIP archive containing a decentralized collection of files and folders. To get a complete representation of the design, multiple sources within the archive must be processed.

- **`graphicContent.agc`**: The most critical file, containing the detailed JSON description of design elements. An archive may contain multiple instances of this file for different artboards, pasteboards, or resources.
- **`interactions.json`**: Describes user interactions and transitions between artboards.
- **`manifest.json`**: Acts as a table of contents for the archive's structure.

### 3. Data Structure (The Scenegraph)

The format is a hierarchical tree of nodes. The root object contains the format version and a `children` array of `Artboard` nodes.

**JSON Example: Root Structure**

JSON

```
{
  "version": "1.5.0",
  "children": [
    {
      "type": "Artboard",
      "id": "...",
      "name": "MainScreen",
      "children": [ ... ]
    }
  ]
}
```

### 4. Common Node Properties

Most nodes share a base set of properties:

|   |   |   |
|---|---|---|
|**Property**|**Type**|**Description**|
|`id`|`string`|A unique identifier for the node.|
|`name`|`string`|The layer name as set in Adobe XD.|
|`type`|`string`|The node type (e.g., `"Shape"`, `"Text"`, `"Group"`).|
|`transform`|`object`|An affine transformation matrix defining position, scale, and rotation.|
|`visible`|`boolean`|Determines if the node is visible (defaults to `true`).|
|`opacity`|`number`|The node's opacity, from 0 (transparent) to 1 (opaque).|
|`blendMode`|`string`|The layer's blend mode (e.g., `"pass-through"`, `"multiply"`).|

JSON Example: transform Matrix

Defines translation, scale, and rotation. tx/ty are for translation.

JSON

```
"transform": {
  "type": "matrix",
  "a": 1, "b": 0, "c": 0, "d": 1,
  "tx": 150,
  "ty": 200
}
```

### 5. Core Node Types

#### 5.1. Artboard

A top-level container for a single UI screen.

**JSON Example: `Artboard`**

JSON

```
{
  "type": "Artboard",
  "id": "artboard-01",
  "name": "Login Screen",
  "width": 1920,
  "height": 1080,
  "style": {
    "fill": {
      "type": "solid",
      "color": { "mode": "RGB", "value": {"r": 255, "g": 255, "b": 255}, "alpha": 1 }
    }
  },
  "children": [ ... ]
}
```

#### 5.2. Shape

Represents any vector graphic. Consists of a `shape` object (geometry) and a `style` object (appearance).

**JSON Example: `Shape` (Rectangle)**

JSON

```
{
  "type": "Shape",
  "id": "shape-01",
  "name": "Button Background",
  "shape": {
    "type": "rect",
    "x": 0,
    "y": 0,
    "width": 200,
    "height": 50,
    "r": [10, 10, 10, 10]
  },
  "style": {
    "fill": { "type": "solid", "color": { "mode": "RGB", "value": {"r": 0, "g": 122, "b": 255} } }
  }
}
```

- **Other `shape.type` values:** `ellipse` (uses `cx`, `cy`, `rx`, `ry`), `path` (uses an SVG-like `path` string), `line` (uses `x1, y1, x2, y2`), and `compound` (uses a boolean `operation` on child shapes).

#### 5.3. Text

Represents text elements.

**JSON Example: `Text`**

JSON

```
{
  "type": "Text",
  "id": "text-01",
  "name": "Button Label",
  "text": {
    "rawText": "Sign In",
    "paragraphs": [
      {
        "lines": [ [ { "x": 0, "y": 0 } ] ],
        "styleRuns": [
          { "length": 7, "style": { "font": { "family": "Roboto", "style": "Bold", "size": 16 } } }
        ]
      }
    ],
    "textAlign": "center"
  },
  "style": {
    "fill": { "type": "solid", "color": { "mode": "RGB", "value": {"r": 255, "g": 255, "b": 255} } }
  }
}
```

#### 5.4. Group

A container for organizing other nodes. Transformations applied to a group affect all its children.

**JSON Example: `Group`**

JSON

```
{
  "type": "Group",
  "id": "group-01",
  "name": "Login Button",
  "transform": { "type": "matrix", "tx": 100, "ty": 300, "a": 1, "b": 0, "c": 0, "d": 1 },
  "children": [
    { "type": "Shape", "name": "Button Background", "id": "shape-01", ... },
    { "type": "Text", "name": "Button Label", "id": "text-01", ... }
  ]
}
```

#### 5.5. Component

Represents a reusable design element with a master-instance relationship.

**JSON Example: `Component` Instance**

JSON

```
{
  "type": "Component",
  "id": "component-instance-01",
  "name": "Primary Button",
  "ref": "master-component-guid",
  "state": {
    "id": "state-guid",
    "name": "Default"
  },
  "overrides": [],
  "children": [ ... ]
}
```

### 6. Styling and Visual Effects

#### 6.1. Fill (`style.fill`)

|   |   |   |
|---|---|---|
|**Type**|**Description**|**JSON Example**|
|`solid`|A single, solid color.|`{"type": "solid", "color": {"mode": "RGB", "value": ...}}`|
|`gradient`|A color gradient. Coordinates are relative to the object's bounds (`units: "objectBoundingBox"`).|`{"type": "gradient", "gradient": {"type": "linear", "x1": 0, "y1": 0, "x2": 1, "y2": 1, "stops": [...]}}`|
|`pattern`|An image fill. The `href` is often an absolute, non-portable file path.|`{"type": "pattern", "pattern": {"href": "D:\\...", "width": 100, "height": 100}}`|

#### 6.2. Stroke (`style.stroke`)

Defines an object's outline. Key properties include `width`, `color`, `align` (`inside`, `center`, `outside`), `cap`, `join`, and `dash` pattern.

**JSON Example: `stroke`**

JSON

```
"stroke": {
  "type": "solid",
  "align": "inside",
  "width": 2,
  "color": { "mode": "RGB", "value": {"r": 220, "g": 220, "b": 220} }
}
```

#### 6.3. Effects (`style.effects`)

An array of filter objects.

|   |   |   |
|---|---|---|
|**Type**|**Description**|**JSON Example**|
|`dropShadow`|Adds a drop shadow.|`{"type": "dropShadow", "visible": true, "params": {"blur": 10, "x": 0, "y": 5, "color": ...}}`|
|`blur`|Blurs the object. If `backgroundEffect` is `true`, it blurs the content _behind_ the element.|`{"type": "uxdesign#blur", "visible": true, "params": {"blurAmount": 5, "backgroundEffect": true}}`|

### 7. Responsive Design (`meta.ux`)

The `meta.ux` object contains properties that define adaptive behavior.

- **Constraints**: Boolean properties like `constraintLeft`, `constraintTop`, and `constraintWidth` determine how an element resizes and pins to its parent. `constraintsDisabled: true` on an artboard enforces absolute positioning for its children.
- **Grid Style**: The `gridStyle` object on an artboard defines a column grid with `columns`, `gutter`, `columnSpacing`, and margin properties.
- **Scrolling**: A group can be made scrollable with `scrollingType: "vertical"` or `"horizontal"`. The visible area is defined by `viewportWidth` and `viewportHeight`.
- **Other**: `aspectLock` ensures proportional scaling, while `rotation` specifies element rotation in degrees.

**JSON Example: Responsive Properties**

JSON

```
"meta": {
  "ux": {
    "constraintWidth": true,
    "constraintHeight": false,
    "scrollingType": "vertical",
    "viewportHeight": 500
  }
}
```
