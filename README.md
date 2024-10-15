# Mixamo Downloader
GUI to bulk download animations from [Mixamo](https://www.mixamo.com/).

This repository contains the Python source code in the `/src` folder. The `.exe` file in the `/dist` folder has been removed.

### Main Fork Changes
This fork introduces the following main changes from the original [juanjo4martinez/mixamo-downloader](https://github.com/juanjo4martinez/mixamo-downloader):
- updates `mixamo_anims.json` to contain all animations as of *October 14th, 2024*, which is 100 more than the original repo, for a total of **2446**.
- provides a script `getids.py` to scrape all new animations and create updated `mixamo_anims.json`
- fixes an error that was causing the script to getting stuck on a few animations. If an animation cannot be downloaded after 10 tries, it's logged as a warning and skipped.
   - currently, the following 3 animations seem to be non-downloadable: `c9c7386d-b96c-11e4-a802-0aaa78deedf9`, `c9c936bd-b96c-11e4-a802-0aaa78deedf9`, `fc6ff619-4203-40a8-b19b-b0d0712ddf0f`
- prints errors, if any, in the console
- saves files as `{index}_{anim_desc}.fbx`, to avoid animations with the same description from overwriting each other
- has a more robust request mechanism (inspired from [jonnytracker/mixamo-downloader](https://github.com/jonnytracker/mixamo-downloader/tree/patch-1))
- sanitizes animation names when saving to prevent errors (inspired from [ALK222/mixamo-downloader](https://github.com/ALK222/mixamo-downloader/tree/main))
- provides a [handy table](src/animations_table.md) with all animation ids, names, descriptions, and media

### Running the script

Make sure you have [Python 3.10+](https://www.python.org/) installed on your computer, as well as the [PySide2](https://pypi.org/project/PySide2/) package:

```bash
pip install PySide2
pip install requests
```

Download the files from the `/src` folder to your own local directory, and double-click on the `main.pyw` script to launch the GUI.

## How to use the Mixamo Downloader

1. Log into your Mixamo account.
2. Select/upload the character you want to animate.
3. Choose between downloading `All animations`, `Animations containing the word` and the `T-Pose (with skin)`.
4. You can optionally set an output folder where all animations will be saved.

   > If no output folder is set, FBX files will be downloaded to the folder where the program is running.
  
5. Press the `Start download` button and wait until it's done.
6. You can cancel the process at any time by pressing the `Stop` button.

> [!IMPORTANT]
> Downloading all animations can be quite slow. We're dealing with a total of 2346 animations, so don't expect it to be lighting fast.
