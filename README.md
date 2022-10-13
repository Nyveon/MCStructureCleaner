# MCStructureCleaner

Missing Structure Fix - Modded structure cleaner for minecraft. Removes all references to non-existent structures to allow for clean error logs and chunk saving. The program goes through every chunk, in every region file of the world, removing the relevant `structure reference` and `structure start` tags.

Designed to fix worlds suffering from the [[MC-194811] Missing structures will destroy saved worlds](https://bugs.mojang.com/browse/MC-194811) bug, where uninstalling a mod which generated custom structures causes the world to become unstable.

Fixes errors such as `Unknown structure start: <missing structure>`, `Failed to save chunk`

## Usage

⚠ Warning: NOT WORKING ON SOME 1.18 worlds, further testing in progress.

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

   ```bash
   python main.py -w "SMP"
   ```

   - **Example 2:** This command will delete all occurances of "Better Mineshaft" and of "Better Stronghold" in the world "My World", in the Nether (DIM-1), using 8 threads.

   ```bash
   python main.py -t "Better Mineshaft" "Better Stronghold" -j 8 -w "My World" -r "DIM-1"
   ```

   If you are on windows, I recommend using PowerShell.
4. Let it run. This may take a while, depending on the power of your computer and the size of your world.
5. Replace the contents of your region folder with the contents of new_region.
6. Enjoy your now working world 😊

## Warnings

1. Always back up your worlds before making any changes to them.
2. Structure specific effects that remained after uninstalling the mod will no longer work for the removed structures (This includes locating structures and custom loot tables).
3. If you have corrupted region files (With the wrong data format, or a size of 0b) the script may crash.

## Todo

- ✅ More detailed output.
- ✅ Multiple tag input. (Implemented in 1.4)
- ✅ Multithreading. (Thanks DemonInTheCloset!, now 2.8x faster)
- ✅ Command line arguments. (Thanks @DemonInTheCloset!)
- ✅ Selection of world/dimensions.
- 🔲 Allow for picking up progress where program left off.
- 🔲 Checking disk space available.
- ✅ Auto-removal of all non vanilla structures mode. (Implemented in 1.4)
- 🔲 All dimensions at once mode
- ✅ Checking for corrupted files (Thanks @lleheny0!)
- ❓ 1.18 support (Included but needs more testing)

## Notes

- Confirmed working for world between version 1.11 and 1.17. 1.18 Support is included, but may not be perfect (please report any issues!)
- Feel free to message me on discord (Nyveon#9999) or twitter (Nyveon) if you need help using it.
- Why did we make this? To save our own SMP world after uninstalling some mods and getting the MC-194811 error. We had spent a lot of time on it, and didn't want anyone else to have to lose their world to the same bug.

![MC Structure Cleaner](images/mc-structure-cleaner.png)
