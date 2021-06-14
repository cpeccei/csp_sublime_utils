import sublime
import sublime_plugin

import re
import json
import collections
import subprocess

# This code is from the very helpful page https://gist.github.com/rgl/7895875

class FormatJsonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            selections = self.view.sel()

            # if there is no selected text, apply to all text.
            if len(selections) == 1 and selections[0].empty():
                selections = [sublime.Region(0, self.view.size())]

            for sel in selections:
                text = self.view.substr(sel)
                obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
                formatted_json = json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
                self.view.replace(edit, sel, formatted_json)

        except Exception as e:
            sublime.error_message(u"ERROR formating JSON: %s" % e)

    def clear(self):
        self.view.erase_status('tidy_json')


class FormatRcodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            selections = self.view.sel()

            # if there is no selected text, apply to all text.
            if len(selections) == 1 and selections[0].empty():
                selections = [sublime.Region(0, self.view.size())]

            for sel in selections:
                text = self.view.substr(sel)
                cmd = ["C:/Program Files/R/R-4.0.3/bin/Rscript.exe", "-e",
                        "f <- file('stdin'); ft <- styler::style_text(readChar(f, n = 1e6)); close(f); print(ft)"]
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=text.encode())
                formatted_r = '\n'.join(stdout.decode().splitlines())
                self.view.replace(edit, sel, formatted_r)

        except Exception as e:
            sublime.error_message(u"ERROR formatting R code: %s" % e)

    def clear(self):
        self.view.erase_status('tidy_r')