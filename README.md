# Assorted Obsidian.md utilities
An [Alfred](https://www.alfredapp.com) workflow focusing on quick entry and logging.

| ⚠️ PLEASE BACKUP YOUR VAULT ⚠️        |
|:---------------------------|
| I can't stress this enough. Bad things can happen when you manipulate files with poorly tested scripts. I've messed up my own vault many times while testing these actions. Dropbox's history and Git were my friends; they should be yours too.    |

## Setup

You must configure the following Environment variables before using the workflow:

### daily_folder
The name of the folder where you keep your daily notes (eg. "Dailies").

### journal_tag
The tag that will be appended to your journal entries. Without the octothorpe. (eg. "journal")

### searches_heading
The H2 heading that will be created/appended to inside your daily notes. Without the octothorpe. (eg. "Google Searches")

### task_tag
The tag that will be appended to your task entries. Without the octothorpe. (eg. "task")

### tasks_file
The filename of the note where you will store your tasks. Without the .md extension. (eg. "Tasks")

### title
Placeholder for the Clip action. Leave empty.

### url
Placeholder for the Clip action. Leave empty.

### tasks_heading
The H2 heading inside your tasks file that tasks will be appended to. Without the octothorpe. (eg. "To-Do").

This allows you to have other headings for differente task groups, like "Done" or "Archived". You can, for example, embed only your current tasks in your daily notes. ![[Tasks#To-Do]]

### vault_name
The name of your vault (obsidian's root folder name). (eg. "Notes")

### vault_path
The path to your vault. This workflow assumes that your vault resides somewhere inside your home folder. However, the home segment must be ommited.

Example:

If your vault is in "/Users/yourname/Dropbox/Notes", you should set vault_path to "/Dropbox/Notes" (without quotes).

## Usage

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
I use this when I'm already looking at the block I wish to reference, bypassing the need to go elsewhere and rely on Obsidian's autocomplete.

1. Place the cursor at the end of the block you wish to reference
2. Use the shortcut. A reference code is added at the cursor position.
3. When the success notification appears, the referencing code is ready to be pasted.

This generates a link, but you can easily turn it into a transclusion by adding "!" before "[[".

### clip (no arguments)
1. Takes the web page open in Safari's active tab and saves it as a new note in markdown format.
3. Places a link to it in the daily note.

### Logged Google Search
Add it in `Features -> Setup fallback results -> + -> Workflow Trigger`
Logs every Google search you perform in Alfred, under the configured `searches_heading` in the daily note.

---

## Feedback
I'm macedotavares over at the Obsidian forum. Feel free to PM me for whatever reason.
