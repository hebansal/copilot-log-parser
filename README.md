# GitHub Copilot Chat Log Parser

A lightweight, zero-dependency Python utility to convert raw VS Code GitHub Copilot Chat export streams (`.json` / `.jsonl` NDJSON files) into beautiful, human-readable Markdown documentation.

## Features

- **Handles NDJSON Streams:** Safely parses line-by-line JSON streams without throwing syntax errors.
- **Stitches Inline References:** Reconstructs broken text chunks by reinserting lost file paths (`src/cache/index.js`) and code symbols (`JSON.stringify()`) precisely where they belong.
- **Privacy Focused:** Completely strips away internal telemetry IDs, authorization tokens, and IDE workspace paths.

## How to Export Your Logs from VS Code

1. Open the **Command Palette** (`Ctrl+Shift+P` on Linux/Windows, `Cmd+Shift+P` on Mac).
2. Type and select **`Chat: Export Chat...`**.
3. Save the resulting file (e.g., `copilot_session.json`).

## Usage

No installation or external packages required. Just clone and run using native Python 3:

```bash
python3 parser.py <path_to_exported_log.json> [output_filename.md]
```

### Example
```bash
python3 parser.py ~/Downloads/copilot_session.jsonl code_review.md
```

## Sample Conversion

### Input Raw Stream Segment:
```json
{"kind":2,"k":["requests"],"v":[{"kind":"thinking","value":"Inspecting files..."}]}
{"kind":1,"k":["inputText"],"v":"If I need to use mysql instead"}
{"kind":2,"inlineReference":{"fsPath":"/home/user/project/src/cache/index.js"}}
{"value":" uses JSON.stringify() which is heavy."}
```

### Output Human-Readable Markdown:
> ### 👤 User
> > If I need to use mysql instead
>
> `src/cache/index.js` uses JSON.stringify() which is heavy.

## License
MIT License. Feel free to use, modify, and distribute.

## 🤝 Contributing, Feedback & Support
If you encounter any issues, find an unparsed log segment, or have ideas for enhancement, please feel free to reach out:

*   **File a Bug / Feature Request:** Open a formal ticket directly via the [GitHub Issues Page](https://github.com/hebansal/copilot-log-parser/issues).
*   **Contact via Email:** Send your inquiries or structural log samples directly to **hbansal@gmail.com**.

Contributions of all types are welcome! Please fork the repository and submit a pull request for structural updates.

