Tracker for Gen 6/7 Pokémon Ironmon.

Specifically, this includes:

    --Pokémon X/Y

    --Pokémon Omega Ruby/Alpha Sapphire

    --Pokémon Sun/Moon

    --Pokémon Ultra Sun/Ultra Moon

Tracking options are available as the following:

    --Ability to save details about each mon

    --Details about moves, abilities and mons

    --Display features for your mon(s)
    
    --See coverage for your moves against other mons to help decide on moves

How to Use:

![CitraTrackerGuide_v0 2 0](https://user-images.githubusercontent.com/104039936/236666717-5667d013-5fe8-4dee-86b1-bc046415d930.png)

Citra emulator for 3DS is required. Drop the files in the folder into the citra scripting folder(the one with a citra.py inside, usually in appdata/local) and run the Tracker.py and citra-updater.py simultaneously.


This is currently a separate window that updates automatically every 10 seconds when ran correctly. The party mode(default) automatically displays all the mons in your party, while the left and right arrows scroll between them. The party mode can be updated by pressing it to change to single, double, and triple battles. This allows you to take notes on opponent mons, although it is manual right now. Also, click the button above "party" to change the game being played(defaults to ORAS), which can be XY,ORAS,SM,USUM. 

There are also buttons to open windows for more information, in particular the one with the mon's name, which displays saved info about it as well as the levels it learns moves at. The next move level is automatically displayed on the main screen. Some of these are new tabs, though on the base page the buttons are not explicitly marked.

To change the game, edit the *config.ini* file in the root directory. Replace *game = [gamename]* with the game you will be playing. Be sure to restart the tracker when you do.

To use, run the citra-updater.py file via Python. Then, either direct your favorite browser (tested only on Firefox and Chrome) to http://localhost:8000/tracker.html or add a browser source in OBS directly. Citra must have a ROM open for the tracker to check for data.

Heal slots are added for right now, but are nonfunctional. This functionality will be added later.

A general coverage page is available by hitting the "Types" button in the moves area. This tells the amount of mons you can hit by how hard- basically an adaptation of [this.](https://wesleystedman.github.io/ironmon-moveset-coverage-calc/)

Keep in mind this is an alpha version, do not expect perfection right now.

Thanks to UTDZac for helping with some of the features being imported from Citra, and something_smart_ for the move level up sets. Otherwise, thank Bulbapedia for the helpful lists I used. Additionally, thank [this](https://github.com/EverOddish/PokeStreamer-Tools) for the citra tracking data.

Python interface is required link [here](https://www.python.org/downloads/).

If you were looking for different games, there are trackers available for the [NDS games](https://github.com/Brian0255/NDS-Ironmon-Tracker)(DPPt, HGSS, BW, B2W2) requiring Bizhawk and the [GBA games](https://github.com/besteon/Ironmon-Tracker)(FRLG, RSE) using Bizhawk or mGBA emulator.
