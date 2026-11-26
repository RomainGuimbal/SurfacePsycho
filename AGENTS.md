# Agent instructions

## Keep it simple, and stop when it isn't

Prefer the simple explanation and the simple fix. Investigate with normal tools:
read the code, look at the data the code writes, check git history.

Do not build elaborate diagnostics — decompressing binaries, scanning for UUID
byte patterns, building a reconstructed reference case to validate a guess, and
similar. If a simple check does not settle the question:

1. Stop.
2. Report what you established, what you suspect, and what you could not verify.
3. Ask the user for the one piece of information or the one test that would
   settle it.

## Start Blender from the environment path

Run `blender`, not a hardcoded install path such as
`C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`. The `blender` on
PATH is the version the project uses; hardcoded paths break when that changes.
