#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os, json, sys, mdfind

# Build json with results
def append_json(filepath):
	json_obj["items"].append({
	"type": "file:skipcheck",
	"title": os.path.basename(filepath[:-3]),
	"subtitle": filepath,
	"arg": filepath,
	"quicklookurl": filepath
	})

query = sys.argv[1]

rootdir = os.path.expanduser(os.environ['vault_path'])

json_obj = {"items":[]}

args = ["-onlyin", rootdir, query]

results = mdfind.mdfind(args)

for result in results.split('\n'):
    append_json(result)

# No matches
if json_obj["items"] == []:
	json_obj["items"].append({
	"type":"file",
	"title": "No results found",
	"icon": {
		"path": "noresults.png"
	},
	})

sys.stdout.write(json.dumps(json_obj))