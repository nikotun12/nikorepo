# Problem Description: Backlink Discovery

The MCP Obsidian server lacks the ability to discover which notes link to a given target note, because no tool exists to scan the vault for wikilinks pointing to a specific file. Given a target note path, scan all markdown files in the vault (including subdirectories) and return notes containing wikilinks to that target, matching links by filename or frontmatter aliases regardless of format (`[[target]]`, `[[target.md]]`, `[[alias]]`, `[[target|display]]`). Ignore wikilinks in code blocks and escaped wikilinks (`\[[target]]`), deduplicate results (one entry per linking note even with multiple links), exclude the target from its own results, return empty list when no backlinks exist, and raise clear errors for nonexistent targets or missing parameters.

## Test Assumptions

### Class and Method Names

**In `src/mcp_obsidian/tools.py`:**
```python
class BacklinkDiscoveryToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("obsidian_get_backlinks")
    
    def get_tool_description(self) -> Tool:
        # Return Tool with name="obsidian_get_backlinks"
        # inputSchema must require "target_path" (string)
        # inputSchema may include optional "vault_path" (string)
        pass
    
    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Must raise RuntimeError if "target_path" not in args
        # Must accept "vault_path" in args (for testing with mock vaults)
        # Must return list with single TextContent containing JSON array
        pass
```

**In `src/mcp_obsidian/obsidian.py`:**
```python
class Obsidian:
    def get_backlinks(self, target_path: str, vault_path: str) -> list[dict]:
        # Raise Exception if target file doesn't exist
        # Return list of dicts with keys: "path" (str), "filename" (str)
        pass
```

**In `src/mcp_obsidian/server.py`:**
```python
# Add after existing tool handlers:
add_tool_handler(tools.BacklinkDiscoveryToolHandler())
```

### Input/Output Format

**Tool Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "target_path": {
      "type": "string",
      "description": "Path to the target note (relative to vault root)",
      "format": "path"
    },
    "vault_path": {
      "type": "string",
      "description": "Absolute path to the vault directory",
      "format": "path"
    }
  },
  "required": ["target_path"]
}
```

**Tool Output Format:**
```json
[
  {
    "path": "relative/path/to/linking-note.md",
    "filename": "linking-note.md"
  }
]
```

### Error Handling

- Raise `Exception` (or subclass) with descriptive message when target file doesn't exist
- Raise `RuntimeError` when required parameters are missing
- Raise `Exception` when vault_path is invalid or inaccessible

### Wikilink Pattern

Use regex pattern: `r'(?<!\\)\[\[(.*?)\]\]'` to match non-escaped wikilinks.

For each matched link:
1. Split on `|` and take first part (ignore display text)
2. Split on `#` and take first part (ignore heading/block refs)
3. Strip `.md` extension if present
4. Compare to target name (stem) or any target alias

### Frontmatter Alias Extraction

Match pattern: `r'^---\s*\n(.*?)\n---\s*\n'` (with `re.DOTALL`)

Within frontmatter, match: `r'aliases:\s*\[(.*?)\]'`

Parse comma-separated aliases and strip quotes/whitespace from each.

### Code Block Removal

Before extracting links, remove:
- Fenced code blocks: `r'```.*?```'` (with `re.DOTALL`)
- Inline code: `r'`.*?`'`

## Validation

Run tests to verify your implementation:

```bash
./test.sh base    # Must pass (6/6) - existing tools unaffected
./test.sh new     # Must pass (19/19) - new feature works
```

Or with Docker:
```bash
docker build -t mcp-obsidian-test .
docker run --rm mcp-obsidian-test ./test.sh base
docker run --rm mcp-obsidian-test
```
