# Assorted Obsidian.md utilities

| ⚠️ PLEASE BACKUP YOUR VAULT ⚠️        |
|:---------------------------|
| I can't stress this enough. Bad things can happen when you manipulate files with poorly tested scripts. I've messed up my own vault many times while testing these actions. Dropbox's history and Git were my friends; they should be yours too.    |

This is an [Alfred](https://alfredapp.com) workflow containing various actions that help you interact with [Obsidian](https://obsidian.md). 

---

## System requirements
- macOS 10.15 (Catalina) or above
- Python3 installation in default location (`/usr/bin/python3`)

## Change Log

### v2.3.0
- Refactored Related Notes so that it doesn't depend so much on external python packages.
- Significantly cut back on workflow size.

### v2.2.2
- Fixed some script paths.
- Made some actions fail less catastrophically.
- The Related Notes feature is still very fragile and dependent on each user's specific system configuration. I'll have to seriously refactor it.

### v2.2.0
- Type `/related` anywere on your note and the workflow will insert a list of related notes, based on content similarity. It may take some time, though. Like, 10 seconds on a newish macbook and 2000+ notes.
- Fixed and improved browser support for all major browsers (minus Firefox). Firefox was removed because the hack was too hacky.

### v2.1.0
- The workflow will now auto-update. 
- Improvements to the `clip`action:
	- it now works with all major browsers. However, due to limitations imposed by Mozilla, Firefox support is very hacky and unreliable.
	- it automatically detects the browser being used (it must be the active application). You no longer have to set a `browser` environment variable.

### v2.0.2
- Minor improvements to Global Search.
- Refactored `s`earch to avoid some dependency problems.

### v2.0.1
- Fixed hardcoded scope in `s` search.
- Fixed markdown `clip`ing.

### v2.0.0

### What's changed
- The worklow does not assume the vault is inside your home folder anymore. `vault_path` must now be a full, absolute path.

### What's new
- The `clip` action now works with Google Chrome. (Thanks for the AppleScript, @alvaroybanez!) Don't forget to change the `default_browser` environment variable if you want to use that instead of Safari.

---

## Install

1. Download [this file](https://github.com/macedotavares/obsidian-utilities/releases/latest/download/Obsidian.Utilities.alfredworkflow).
2. Open it.

---

## Setup
You must configure the following environment variables before using the workflow:

### Environment Variables

#### daily_folder
The name of the folder where you keep your daily notes (eg. "Dailies").

#### journal_tag
The tag that will be appended to your journal entries. Without the octothorpe. (eg. "journal")

#### searches_heading
The H2 heading that will be created/appended to inside your daily notes. Without the octothorpe. (eg. "Google Searches")

#### task_tag
The tag that will be appended to your task entries. Without the octothorpe. (eg. "task")

#### tasks_file
The filename of the note where you will store your tasks. Without the .md extension. (eg. "Tasks")

#### title
Placeholder for the Clip action. Leave empty.

#### url
Placeholder for the Clip action. Leave empty.

#### tasks_heading
The H2 heading inside your tasks file that tasks will be appended to. Without the octothorpe. (eg. "To-Do").

This allows you to have other headings for differente task groups, like "Done" or "Archived". You can, for example, embed only your current tasks in your daily notes. ![[Tasks#To-Do]]

#### vault_name
The name of your vault (obsidian's root folder name). (eg. "Notes")

#### vault_path
The path to your vault.

Examples:

- "/Users/yourname/Dropbox/Notes"
- "~/Dropbox/Notes"
- "/Volumes/NAS/Notes

### Related Notes Snippet
You must also configure the snippet object in the Related Notes action. Choose a prefix character and a keyword (e.g. `/related`).

---

## Usage

### Cmd+Shift+L  [search terms] (Global Search & Linking)
This action goes through all your notes and returns a list of titles, headings and/or blocks that fuzzy match the terms you entered, allowing you to **immediatelly link** to them.

Each kind of result will have a different icon:
- `[[]]` for note titles
- `#` for headings
- `^` for blocks/lines

Insert the link by pressing Enter or double-clicking the result.

Cmd+Enter will open the note file in VS Code. (I'm using an external text editor here because I didn't want to replace the active note, and I couldn't find a way of opening a new pane.)
As usual in Alfred, pressing shift with a result highlighted will quick-look into it.

**Note:** The shortcut will only work when Obsidian is the active application and the focus is on an editor pane.

### v (no arguments)
Open vault folder in VS Code

### s [search tearms]
Search note titles and contents with Alfred.
Open results in Obsidian or VS Code (Cmd modifier)

### j [journal entry]
Append journal entry to daily note. Adds timestamped heading and journal tag.

### n [entry]
Append entry to daily note.

### t [task]
Appends tasks to tasks file, under the configured heading. Prefixes tasks with date created.
Transcludes task in the daily note. Adds task tag. Date is ommited.

### Cmd+Shift+R (block referencing helper)
You can use this when you're already looking at the block you wish to reference, bypassing the need to go elsewhere and rely on Obsidian's autocomplete.

1. Place the cursor at the end of the block you wish to reference
2. Use the shortcut. A reference code is added at the cursor position.
3. When the success notification appears, the referencing code is ready to be pasted.

This generates a link, but you can easily turn it into a transclusion by adding "!" before "[[".

### clip (no arguments)
1. Takes the web page open in Safari's active tab and saves it as a new note in markdown format.
3. Places a link to it in the daily note.

### Logged Google Search
Add it in `Features` → `Setup fallback results` → `+` → `Workflow Trigger`

Logs every Google search you perform in Alfred, under the configured `searches_heading` in the daily note.

---

## Updates
I'll fix things occasionally, in small batches. New features usually take longer.
Check the [Github repository](https://github.com/macedotavares/obsidian-utilities) for updates and source code.

## Feedback
Found a bug? Want to make a suggestion? [Open an issue](https://github.com/macedotavares/obsidian-utilities/issues/new) or [PM me in the Obsidian forum](https://forum.obsidian.md/u/macedotavares/summary).
