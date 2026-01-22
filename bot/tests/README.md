# Unit Tests for Gamerbot

This directory contains comprehensive unit tests for all Gamerbot modules/extensions.

## Running Tests

To run all tests:
```bash
cd /home/runner/work/GamerbotAgain/GamerbotAgain/bot
pytest
```

To run tests for a specific module:
```bash
pytest tests/test_imgmaker.py
pytest tests/test_internet.py
```

To run tests with verbose output:
```bash
pytest -v
```

To run tests with coverage:
```bash
pytest --cov=src/exts --cov-report=html
```

## Important Note about Testing Discord Commands

The bot uses `disnake` slash command decorators (`@commands.slash_command()`). When testing these commands, you must call the callback method directly:

```python
# Correct way to test a command
await cog.command_name.callback(cog, inter)

# NOT this
await cog.command_name(inter)
```

This is because the decorator wraps the method, and direct calls will fail with a "missing argument" error.

## Test Structure

Tests are organized by module, with each module having its own test file:

- `test_util_functions.py` - Utility functions (message formatting, file operations, shell commands, GeoIP)
- `test_imgmaker.py` - Image manipulation commands (meme generators, figlet, etc.)
- `test_internet.py` - Network/Internet tools (traceroute, whois, nmap, tldr, etc.)
- `test_shell.py` - Linux/Shell command execution
- `test_chat.py` - Chat reaction commands (memes, GIFs)
- `test_admin.py` - Bot administration commands
- `test_randomstuff.py` - Miscellaneous utility commands
- `test_debug.py` - Debug and development tools
- `test_about.py` - Bot information commands
- `test_fuckedup.py` - Reaction/meme commands
- `test_status.py` - Bot status and presence management
- `test_xkcd.py` - XKCD comic search
- `test_reminders.py` - Reminder system with timezone support
- `test_speak.py` - Text-to-speech and voice functionality
- `test_schizo.py` - Bot automation and background tasks

## Module Organization Analysis

### Well-Organized Modules

1. **imgmaker.py** - Image manipulation
   - All commands relate to creating/modifying images
   - Appropriately categorized

2. **internet.py** - Network/Internet tools
   - Contains network utilities (traceroute, whois, nmap)
   - Contains web tools (tldr, cht.sh, archwiki)
   - Well-focused on internet/network functionality

3. **shell.py** - Linux/Shell commands
   - Focused on shell command execution
   - Includes appropriate security measures
   - Well-categorized

4. **admin.py** - Bot administration
   - Contains bot info and extension management
   - Appropriately focused

5. **reminders.py** - Reminder functionality
   - Well-organized around reminder features
   - Includes timezone management

6. **status.py** - Bot status management
   - Focused on presence and uptime
   - Well-defined purpose

7. **speak.py** - Voice/TTS functionality
   - All commands relate to voice channels
   - Appropriately categorized

8. **xkcd.py** - XKCD functionality
   - Single-purpose module for XKCD comics
   - Well-focused

9. **about.py** - Bot information
   - Contains bot info, links, and support
   - Well-organized

### Modules with Potential Organization Issues

1. **randomstuff.py**
   - **Issue**: Contains commands that could belong elsewhere
   - `gcache` command - Could belong in `internet.py` as it's a web tool
   - `math` command - Could be in a utilities module
   - **Recommendation**: Consider moving `gcache` to `internet.py`

2. **fuckedup.py**
   - **Issue**: Similar functionality to `chat.py`
   - Both contain reaction/meme GIF commands
   - Module name is somewhat ambiguous
   - **Recommendation**: Consider merging with `chat.py` or renaming to be more descriptive (e.g., `reactions.py`)

3. **schizo.py**
   - **Issue**: Contains mixed functionality
   - `make_bonk` method duplicates functionality from `imgmaker.py`
   - Contains bot automation, owner utilities, and image generation
   - **Recommendation**: Move `make_bonk` to `imgmaker.py`, or remove if redundant

4. **chat.py** and **fuckedup.py**
   - **Issue**: Overlapping functionality
   - Both modules serve similar purposes (reaction commands)
   - **Recommendation**: Merge into single module or clearly differentiate their purposes

### Security Considerations

1. **imgmaker.py**
   - `space` command uses `os.system("wget")` which is a security risk
   - **Recommendation**: Replace with `requests` or `aiohttp`

2. **shell.py**
   - Good security measures in place:
     - Forbidden command list
     - Forkbomb detection
     - Guild permission checking
     - User-specific sandboxed environments

## Test Coverage

Each test file includes:
- Cog initialization tests
- Command functionality tests
- Error handling tests
- Edge case tests
- Mocking of external dependencies (Discord API, filesystem, network)

## Dependencies

Testing dependencies are defined in `requirements.txt`:
- pytest
- pytest-asyncio
- pytest-mock

## Notes

- All tests use mocking to avoid dependencies on:
  - Discord API
  - Filesystem operations
  - Network requests
  - External services
- Tests are designed to run independently and in parallel
- Each test file is self-contained with its own fixtures
