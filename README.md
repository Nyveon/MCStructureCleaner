# MCStructureCleaner

Modded structure cleaner for minecraft. Removes all references to non-existent structures to allow for clean error logs and chunk saving. The program goes through every chunk, in every region file of the world, removing the relevant `structure reference` and `structure start` tags.

Designed to fix worlds suffering from the [[MC-194811] Missing structures will destroy saved worlds](https://bugs.mojang.com/browse/MC-194811) bug, where uninstalling a mod which generated custom structures causes the world to become unstable.

Fixes errors such as `Unknown structure start: <missing structure>`, `Failed to save chunk`

# Usage

1. Install the requirements: [Python 3.x](https://www.python.org/) and [Matcool's Anvil Parser](https://github.com/matcool/anvil-parser).
2. Download the [latest release](https://github.com/Nyveon/MCStructureCleaner/releases/) and place `main.py` in the same directory as your world folder 
   - **Example:** If it's a server: in the server folder, or if it is a singleplayer world, in the saves folder.
3. Run main.py with any of the following configuration properties. I recommend using [NBTExplorer](https://github.com/jaquadro/NBTExplorer) to find the name, or just letting the program fix all non-vanilla names by not inputting any tag.
   - `-h` For help on command line arguments.
   - `-t` For the tag you want removed, in quotes. Leave empty if you wish to remove ALL NON-VANILLA TAGS.
   - `-j` For the number of threads you want to run it on. Default: 2 x CPU Cores.
   - `-w` For the name of the world you want to process. Default: "world".
   - `-r` For the name of the sub-folder (dimension) in the world. Default: "".
   - **Example 1:** This command will delete all non-vanilla structures (defined up to 1.17) in the overworld of the world "SMP" 
   ```
   python main.py -w "SMP"
   ```
   - **Example 2:** This command will delete all occurances of "Better Mineshaft" in the world "My World", in the Nether (DIM-1), using 8 threads. 
   ```
   python main.py -t "Better Mineshaft" -j 8 -w "My World" -r "DIM-1"
   ```
4. Let it run. This may take a while, depending on the power of your computer and the size of your world.
5. Replace the contents of your region folder with the contents of new_region.
6. Enjoy your now working world 😊

# Todo:

- [x] More detailed output.
- [x] Multiple tag input. (Implemented in 1.4)
- [x] Multithreading. (Thanks DemonInTheCloset!, now 2.8x faster)
- [x] Command line arguments. (Thanks DemonInTheCloset)
- [x] Selection of world/dimensions.
- [ ] Allow for picking up progress where program left off.
- [ ] Checking disk space available.
- [x] Auto-removal of all non vanilla structures mode. (Implemented in 1.4)

# Notes:

- I have only tested this with 1.16 worlds. In theory it should work with all worlds that use the anvil format though.
- Feel free to message me on discord or twitter if you need help using it.
- Why did we make this? To save our own SMP world after uninstalling some mods. We had spent a lot of time on it, and didn't want anyone else to have to lose their world to the same bug.
