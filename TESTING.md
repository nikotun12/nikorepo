# Test Infrastructure

## Overview

This repository uses Test-Driven Development (TDD) to validate new features. Tests are organized into two modes:

- **Base Mode**: Tests existing functionality remains unaffected
- **New Mode**: Tests new feature implementation

**Feature Specification**: See [PROBLEM.md](PROBLEM.md) for the problem description and implementation guide.

## Files

- `test.sh` - Test runner script with base/new modes
- `Dockerfile` - Docker image for containerized testing
- `test.patch` - Reference implementation patch for the backlink discovery feature
- `tests/test_existing_tools.py` - Base tests (6 tests)
- `tests/test_backlinks.py` - New feature tests (19 tests)

## Running Tests Locally

```bash
./test.sh base    # Run base tests (should pass)
./test.sh new     # Run new feature tests (will fail until feature implemented)
```

## Running Tests in Docker

```bash
docker build -t mcp-obsidian-test .

docker run --rm mcp-obsidian-test              # Run new tests (default)
docker run --rm mcp-obsidian-test ./test.sh base    # Run base tests
```

## Test Status

### Base Mode (✅ 6/6 passing)
Verifies existing tools are unaffected by new feature implementation.

### New Mode (❌ 0/19 passing)
All tests currently fail because `BacklinkDiscoveryToolHandler` does not exist yet.

## Feature: Backlink Discovery

The new feature allows discovering all notes that contain wikilinks pointing to a target note.

### Test Coverage

**Basic Functionality:**
- Find single backlink
- Return empty when no backlinks
- Exclude target from results

**Link Format Support:**
- `[[target.md]]` - With extension
- `[[target]]` - Without extension
- `[[alias]]` - Using frontmatter aliases
- `[[target|display]]` - Pipe aliases
- Multiple links to same target
- Links in nested folders

**Edge Cases:**
- Similar note names not confused
- Code blocks ignored
- Escaped wikilinks ignored

**Error Handling:**
- Nonexistent target
- Missing target_path argument
- Invalid vault path

**Tool Registration:**
- Handler class exists
- Correct tool name
- Description present
- Schema validation

## Applying the Patch

To implement the feature using the reference patch:

```bash
git apply test.patch
./test.sh new    # Should now pass all 19 tests
./test.sh base   # Should still pass all 6 tests
```
