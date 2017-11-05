A discord bot for the private server "The Campfire"

&nbsp;

## Adding Libraries

1. Make a copy of either `database.py` or `general.py` in the `libs` folder.
2. Open `__all_imports.py` and add `import lib.name_of_your_library_file` to the bottom.
3. Edit your library file. See **Editing a Library File** for instructions.
4. Open `bot.py` and add `lib.name_of_your_library_file.name_of_your_class()` to the end of the list on line 3.

&nbsp;

## Editing a Library File

* Ensure that `import lib.globalvars` is at the top of your file. This is very important.
* Edit the name of the class. It can be anything, as long as you use this same name in `bot.py` (see **Adding Libraries**, step 4).
* Optional but HIGHLY recommended: Doctypes.
  * Give your class a doctype; this will show up when a user runs `!commands`:
```
class generic_class_name:
	```Generic Commands```
```
  * Give each command a doctype, too; this will show up when a user runs `!commands <command_name>`.
```
async def command_name(self, message):
	```Description of the command.
Type any extra information for the user here.

If you want the command to show up as admin-only, end the doctype with:
Requires Admin priveleges.```
```
* Create each command with `ascync def name_of_command(self, message)`.
  * To give your command arguments, add them after `message`, like so:
```
async def name_of_command(self, message, argument1, argument2, kwarg1="Default Value")
```
* To access the bot client, use `lib.globalvars.client`.
* To check if the command caller has bot priveleges, use this:
```
if lib.globalvars.isAdmin(message.author):
```

&nbsp;

## Setting Up the Bot

1. Just download all the files and extract them to a folder somewhere.
2. In the folder `data`, create a file named `botfire.sqlite`.
3. Find an SQLite file editor such as [DB Browser for SQLite](http://sqlitebrowser.org/).
4. Open the .sqlite file with it and add the following:
* Table: `Users`
  * `TEXT` value: `ID`
  * `INTEGER` value: `playing` (default value: `0`)
5. Create a file named `token.txt` inside of `data`. Inside of it, paste the token of the Discord account you want the bot to run in.

&nbsp;

## Running the Bot

Just open `bot.py`. Alternatively, open one of the two included `.bat` files.
