#!/usr/bin/python3
# encoding: utf-8
 
import sys, html2text

query = sys.argv[1]

h = html2text.HTML2Text()
result = h.handle(query)

sys.stdout.write(result)