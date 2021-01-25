# MCStructureCleaner

Modded structure cleaner for minecraft. Removes all references to non-existent structures to allow for clean error logs and chunk saving. The program goes through every chunk, in every region file of the world, removing the relevant `structure reference` and `structure start` tags.

Designed to fix worlds suffering from the [[MC-194811] Missing structures will destroy saved worlds](https://bugs.mojang.com/browse/MC-194811) bug, where uninstalling a mod which generated custom structures causes the world to become unstable.

Fixes errors such as `Unknown structure start: <missing structure>`, `Failed to save chunk`

# Usage

1. Install the requirements: [Python 3.x](https://www.python.org/) and [Matcool's Anvil Parser](https://github.com/matcool/anvil-parser).
2. Place main.py in a folder with your world folder.
3. Run main.py, and instruct it as to which structure tag you wish to remove. I recommend using [NBTExplorer](https://github.com/jaquadro/NBTExplorer) to find the name.
4. Let it run.
5. Replace the contents of your region folder with the contents of new_region.

# Todo:

- [x] More detailed output.
- [ ] Multiple tag input.
- [ ] Optimizations (Multithreading?).
- [ ] Selection of world/dimensions.
- [ ] Allow for picking up progress where program left off.

# Notes:

- I have only tested this with 1.16.5 worlds.
- Feel free to message DM me on twitter if you need help using it.
