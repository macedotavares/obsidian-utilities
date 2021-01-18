#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os, re, sys, json
import random, string
from urllib import parse

# Generate code for block reference #
def get_random_alphanumeric_string(length):
	letters_and_digits = string.ascii_letters + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	return result_str

# Build json with results
def append_json(title, match, icon, arg, quicklook):
	json_obj["items"].append({
	"type": "file:skipcheck",
	"title": title,
	"match": match,
	"icon": {
		"path": icon
	},
	"subtitle": os.path.join(root, file),
	"arg": arg,
	"quicklookurl": quicklook
	})

rootdir = os.path.expanduser(os.environ['vault_path'])

# Don't index files in these locations
exclude = set(['.git', '.obsidian', '.trash', 'Templates'])

json_obj = {"items":[]}

# Go through all the files in the vault (and subfolders)
for root, dirs, files in os.walk(rootdir):
	dirs[:] = [d for d in dirs if d not in exclude] # excluding directories listed above
	for file in files:
		if file[-3:]==".md": # If file is markdown

			# append (title, match, icon, arg, quicklook) to json

			# Titles 
			append_json(
				file,
				file,
				"icons/title.png",
				"[["+file[:-3].strip()+"]]" + "ALFRED_SPLIT" + os.path.join(root, file) + "ALFRED_SPLIT" + "(none)" + "ALFRED_SPLIT" + "(none)",
				"file://" + parse.quote(os.path.join(root, file))
			)

			# Lines

			f = open(os.path.join(root, file))
			lines = f.readlines()
			f.close()

			for line in lines: 
				line = line.strip()
				match = line.translate(str.maketrans('', '', string.punctuation))
			
				# Headings

				if line[:2]=="##":
					
					heading = re.sub(r'^#+ ','',line) # Remove octothorpe from beginning of line

					# append (title, match, icon, arg, quicklook) to json
					append_json(
						line,
						line + ' ' + match,
						"icons/heading.png",
						"[["+file[:-3].strip()+"#"+heading+"]]" + "ALFRED_SPLIT" + os.path.join(root, file) + "ALFRED_SPLIT" + "(none)" + "ALFRED_SPLIT" + "(none)",
						"file://" + parse.quote(os.path.join(root, file))
					)

				# Blocks
					
				else:
					existing_code = re.findall(r'\^[\w\d]{6}', line)
					if existing_code:
						ref_code = existing_code[0][1:]
					else:
						# Generate reference code
						ref_code = get_random_alphanumeric_string(6)

					# append (title, match, icon, arg, quicklook) to json
					append_json(
						line,
						line + ' ' + match,
						"icons/block.png",
						file[:-3].strip() + "ALFRED_SPLIT" + os.path.join(root, file) + "ALFRED_SPLIT" + line + "ALFRED_SPLIT" + ref_code,
						"file://" + parse.quote(os.path.join(root, file))
					)

# No matches
if json_obj["items"] == []:
	json_obj["items"].append({
	"type":"file",
	"title": "No results found",
	"icon": {
		"path": "icons/noresults.png"
	},
	})

sys.stdout.write(json.dumps(json_obj))