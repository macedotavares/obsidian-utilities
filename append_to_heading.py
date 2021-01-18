#!/usr/bin/python3
# encoding: utf-8

import re, sys, os, unicodedata    

original_content = os.environ['original_content']
heading = os.environ['heading']
entry = os.environ['entry']

find = re.compile(r'^(## ' + re.escape(heading) + r'\n.*?)\n+---', flags = re.MULTILINE|re.DOTALL)
replace = '\\1\n- '+entry+'\n\n---'

if re.findall(find, original_content) == []:
	new_content = original_content + '## ' + heading + '\n- ' + entry + '\n\n---'
else:
	new_content = re.sub(find, replace, original_content)

sys.stdout.write(unicodedata.normalize("NFC",new_content))