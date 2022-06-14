README for mnemo-beeminder-plugin
=====================================

# Summary

- Created on: Apr 17, 2021
- Created by: gojun077@gmail.com

Send data to a Beeminder goal the via Beeminder API every time a Mnemosyne
card has been successfully reviewed (score of 2, 3, 4, or 5).

According to the Mnemosyne
[docs](https://github.com/mnemosyne-proj/mnemosyne/tree/master/mnemosyne/example_plugins)
on plugins:

```
In order to package a plugin for easy installation by the user, just
compress your .py file and all the other files it requires in a zip file,
and change the extension from .zip to .plugin
```

## Pre-Setup: Create `beeminder.json`

This file should be created in the Mnemosyne config folder, which is in
different locations depending on your OS. The following link
https://mnemosyne-proj.org/help/advanced-preferences.php shows the path to
Mnemosyne configs on Linux, MacOS, and Windows:

- `~/.config/mnemosyne/` Linux
- `~/Library/Mnemosyne/` MacOS
- `C:\Users\<your user name>\Application Data\Roaming\Mnemosyne`

In the appropriate path above depending on your OS, create the file
`beeminder.json`. Note that all strings in JSON must be *double* quoted!
The JSON file will contain 4 keys, `username`, `auth_token`, `goalname` and
`comment`.

- `username`: a valid username on beeminder.com
- `auth_token`: API token from beeminder
  + see https://api.beeminder.com/#auth for how to get an API token
- `goalname`: the name of your beeminder goal
- `comment`: string you want to appear in the added datapoint
  + if you have no comment, use `""`

Here's an example `beeminder.json` file

```json
{
"username": "alice",
"auth_token": "abc123",
"goalname": "exercise",
"comment": "sweat a lot today"
}
```


## Setup and Usage

After cloning this repository, cd into the repo folder. First create a
zip archive with the name `beeminder_plus_one.zip` and add the file
`beeminder_plus_one.py` to the new zip. Next rename your zip file to
`beeminder_plus_one.plugin`.


Below is an example using the shell for users on MacOS or Linux:

```sh
git clone git@github.com:gojun077/mnemo-beeminder-plugin.git
cd mnemo-beeminder-plugin
zip beeminder_plus_one.zip beeminder_plus_one.py
mv beeminder_plus_one.zip beeminder_plus_one.plugin
```
If you are on Windows you can try the following PowerShell snippets:

```powershell
cd mnemo-beeminder-plugin
Copy-ToZip "beeminder_plus_one.py" -ZipFile beeminder_plus_one.zip
Rename-Item beeminder_plus_one.zip beeminder_plus_one.plugin
```

Launch mnemosyne (the first time I suggest running it from the command line
time so you can see any errors dumped to the CLI). At the top menu select
*Settings* -> *Manage plugins*. At the bottom of the next dialog window,
click the button *Install new plugin* and a file explorer window will
open. Navigate to the directory into which you cloned
`mnemo_beeminder_plugin` and select `beeminder_plus_one.plugin` and click
the button *Open*. You should now see a new entry *Update Beeminder after
Rep* in the list of plugins. Click the box next to this entry to enable it.

Do a card review. If you grade the card a '2' or higher, on the command
line you should see something like:

```
Data successfully submitted to Beeminder
{'timestamp': 1618639201,
'value': 1.0,
'comment': 'submitted by Mnemosyne beeminder_plus_one.py | card grade was 4',
'id': '607af7f255c133055e000000',
'updated_at': 1618671602,
'requestid': None,
'canonical': '17 1 "submitted by Mnemosyne beeminder_plus_one.py"',
'fulltext': '2021-Apr-17 entered at 00:00 on 2021-Apr-18  via api',
'origin': 'api',
'daystamp': '20210417',
'status': 'created'}
```


## Python dependencies

This plugin requires that the `requests` library for Python 3 be
installed in your Python environment. Your version of Python 3
should be 3.8 or higher.
