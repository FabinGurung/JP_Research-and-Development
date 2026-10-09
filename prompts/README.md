# Owner-only researcher upgrade handovers

No Drive migration runs from GitHub. Each individual prompt becomes an execution instruction only when the user pastes the full contents into that researcher's owning chat.

These include the exact verified project root ID (except RSH-004 HOLD), direct-child Drive folder IDs, non-delete safety instructions and full A9 PRE/POST boundaries. Every owning thread must re-read live state and skip already completed operations.

Regenerate/check with `python3 scripts/researchers/generate_prompts.py --check` and `python3 scripts/researchers/generate_prompts.py --researcher RSH-010`. The latter rewrites local markdown only; it never calls Drive.
