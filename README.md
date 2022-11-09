# MCStructureCleaner

Missing Structure Fix - Modded structure cleaner for minecraft. Removes all references to non-existent structures to allow for clean error logs and chunk saving. The program goes through every chunk, in every region file of the world, removing the relevant `structure reference` and `structure start` tags.

Designed to fix worlds suffering from the [[MC-194811] Missing structures will destroy saved worlds](https://bugs.mojang.com/browse/MC-194811) bug, where uninstalling a mod which generated custom structures causes the world to become unstable.

Fixes errors such as `Unknown structure start: <missing structure>`, `Failed to save chunk`

## Installation

⚠ This does not work on 1.18.x worlds. ⚠

1. Install [Python 3.x](https://www.python.org/) Currently not compatible with Python versions past 3.10
2. Install the requirements [Matcool's Anvil Parser](https://github.com/matcool/anvil-parser) and [Gooey](https://github.com/chriskiehl/Gooey). This can be done with the following commands:

```bash
pip install anvil-parser
pip install Gooey
```
   
3. Download the latest release (*MCStructureCleaner_v16.zip*) from the [releases page](https://github.com/Nyveon/MCStructureCleaner/releases) and extract it.

## How to Use (Instructions)

1. Find the names of the structure tags you want to remove. I recommend using [NBTExplorer](https://github.com/jaquadro/NBTExplorer).
2. **Install MCStructureCleaner** then double click on `main.py` to run the program.
3. You should see an interface like this.

![MC Structure Cleaner GUI](images/screenshot1.png)

4. Now, you can fill out each section:
   1. `tag`: The exact name of the structure tag you want to remove. This is case sensitive. You can input many tags at once, separated by spaces. If the names have spaces in them, you can surround them with quotes. For example, `"my structure" "another structure"`. Leave this field blank if you want to delete **ALL NON-VANILLA STRUCTURE TAGS**.
   2. `jobs`: The number of threads you want to run it on. Default: 2 x CPU logical processors. In my experience, the default works well enough.
   3. `path`: The path to the world folder. (The whole folder, not just the `region` folder)
   4. `output`: The path to the output folder. This is where the cleaned `new_region` will be saved. If you leave this blank, the cleaned world will be saved in the same folder as MCStructureCleaner.
   5. `region`: The dimension you want to clean. If you leave this **blank** it will clean the overworld. `DIM-1` is the nether, `DIM1` is the end.
5. *For example, this input will delete all occurances of "Better Mineshaft" and of "Better Stronghold" in the world "MyWorld", in the Nether (DIM-1), using 8 threads. The world folder is located in the user's minecraft saves, and the output will be saved to the desktop.*

![MC Structure Cleaner GUI](images/screenshot2.png)

6. Once you have filled out all the sections, click `Start` to begin the process. This may take a while, especially if you have a larger world.
7. If there is an error, it will be displayed in the `Output` section. If there is no error, the program will say `Done!` and you can close the program.
8. Now you may rename the output folder (called `new_region`) to `region` and **replace** the old `region` folder in your world. **Don't forget to backup your world first!**
9. Enjoy your now working world 😊

### Command Line

<details>
  <summary>Only recommended if the GUI does not work on your device</summary>

1. Run main.py with any of the following parameters. I recommend using [NBTExplorer](https://github.com/jaquadro/NBTExplorer) to find the name, or just letting the program fix all non-vanilla names by not inputting any tag.
   - `-h` For help on command line arguments.
   - `-t` For the tag you want removed, in quotes. Leave empty if you wish to remove ALL NON-VANILLA TAGS.
   - `-j` For the number of threads you want to run it on. Default: 2 x CPU logical processors.
   - `-w` For the name of the world you want to process. Default: "world".
   - `-p` For the path to the world you want to process. Default: current directory.
   - `-r` For the name of the sub-folder (dimension) in the world. Default: "".
   - `-o` For the path of the folder where the new region folder will be saved to. Default: current directory.
   - **Example 1:** This command will delete all non-vanilla structures (defined up to 1.17) in the overworld of the world "SMP"

   ```bash
   python main.py -w "SMP"
   ```

   - **Example 2:** This command will delete all occurances of "Better Mineshaft" and of "Better Stronghold" in the world "MyWorld", in the Nether (DIM-1), using 8 threads. The world folder is located in the user's minecraft saves, and the output will be saved to the desktop.

   ```bash
   python main.py -t "Better Mineshaft" "Better Stronghold" -j 8 -r "DIM-1" -p "C:\Users\X\AppData\Roaming\.minecraft\saves\MyWorld" -o "C:\Users\X\Desktop"
   ```

   If you are on windows, I recommend using PowerShell.
2. Let it run. This may take a while, depending on the power of your computer and the size of your world.
3. Replace the contents of your region folder with the contents of new_region.
4. Enjoy your now working world 😊

</details>

## Warnings

1. Always back up your worlds before making any changes to them.
2. Structure specific effects that remained after uninstalling the mod will no longer work for the removed structures (This includes locating structures and custom loot tables).
3. If you have corrupted region files (With the wrong data format, or a size of 0b) the script may crash.

## Developers

### Installation & Testing

#### Installation

Clone the repository, then install requirements:

```bash
pip install -r requirements.txt
pip install -r tests/requirements.txt
```

#### Linting and style

Most standard linters are fine as long as the code is readable, the project files are currently linted with [flake8](https://flake8.pycqa.org/en/latest/).

#### Running tests

- **VSCode**: the testing environment is already configured, simply press the `Run Tests` button added by the [official Python Extension](https://code.visualstudio.com/docs/python/testing).
- **Command Line**:

```bash
pytest -v --cov=. tests/ --cov-report xml:cov.xml
```

- **Expected coverage:** The `structurecleaner` folder should have 100% coverage.

#### Making your own tests

1. Generate your expected input files and output files. This can be done easily by running the program on a world, and then copying the region folder to the `tests` folder, and renaming it to `expected_input` and `expected_output` respectively. However, for new formats it is important to thoroughly check the output or make it by hand with NBTExplorer!
2. Place them in the directory `tests/data/X` where X is the name of the test. (See other tests for reference)
3. Use `remove_tags_test` in the `tests` directory to create your test. (See other tests for reference)
4. Run pytest. The coverage should be the same as before, and the test should pass.

#### Todo & Contribution

Contributions are always welcome! See the [issues page](https://github.com/Nyveon/MCStructureCleaner/issues) for ideas, or feel free to suggest your own ideas.

## Notes

- Feel free to message me on discord (Nyveon#9999) or twitter (Nyveon) if you need help using it.
- **Why did we make this?** To save our own SMP world after uninstalling some mods and getting the MC-194811 error. We had spent a lot of time on it, and didn't want anyone else to have to lose their world to the same bug.
- Thanks to @DemonInTheCloset for contributing to multiprocessing and command line arugments.
- Thanks to @lleheny0 for contributing to file validation.

### Versions tested

- Pre 1.12: The bug does not apply to these versions.
- 1.13.x: 🟡 Manually
- 1.14.x: 🟠 Untested, but should work
- 1.15.x: 🟢 Automatically
- 1.16.x: 🟡 Manually
- 1.17.x: 🟠 Untested, but should work
- 1.18.x: 🔴 Not working. anvil-parser is not compatible with 1.18.x yet.
- 1.19.x: ❔ The bug might be fixed in this version. If anyone has information, please let me know c:

![MC Structure Cleaner](images/mc-structure-cleaner.png)
