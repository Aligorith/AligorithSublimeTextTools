# General tools for making it easier to work in Sublime Text
#
# Original Author: Joshua Leung
# Date: April 2017

import sublime
import sublime_plugin

###########################################
# Convert Camel-Case <-> Underscores

# Convert between Camel-Case and Underscores
class ConvertCamelCaseUnderscoresCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		# Figure out the mode for how we're going to do things
		mode = args.get("mode", 'toggle')
		
		# Find selected text to operate on 
		sel_regions = self.view.sel()
		if (len(sel_regions) == 0) or (sel_regions[0].size() == 0):
			sublime.message_dialog("No text selected")
			return;
		
		# Operate on each selected region (from last to first, to avoid errors)
		for sel in reversed(sel_regions):
			# Extract the text in question
			txt = self.view.substr(sel)
			
			if mode == "camel":
				self.convert_to_camel(edit, sel, txt)
			elif mode == "underscores":
				self.convert_to_underscores(edit, sel, txt)
			else:
				self.toggle_case(edit, sel, txt)
	
	# Check what to do with the given region
	def toggle_case(self, edit, region, txt):
		# If it has underscores, it is "underscores", otherwise "camel"
		if "_" in txt:
			self.convert_to_camel(edit, region, txt)
		else:
			self.convert_to_underscores(edit, region, txt)
	
	# Convert to CamelCase
	def convert_to_camel(self, edit, region, txt):
		# Break into segments
		segments = txt.split("_")
		
		# Capitalise start letter of each segment, then join them back together
		result = "".join([s.title() for s in segments])
		self.view.replace(edit, region, result)
		
	# Convert to under_scores_style
	def convert_to_underscores(self, edit, region, txt):
		# Break into segments -> Find the capitals
		segments = []
		current = []
		
		for ch in txt:
			if ch.isupper():
				# Start new segment, but converted to lowercase
				current = [ch.lower()]
				segments.append(current)
			else:
				# Append to existing segment
				current.append(ch)
		
		# Join segments together (but first, we must convert the lists back to strings :)
		result = "_".join([''.join(s) for s in segments])
		self.view.replace(edit, region, result)
		
		

###########################################

