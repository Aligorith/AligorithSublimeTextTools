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
# Toggle between arrow/dot accessors for C/C++

class ToggleArrowDotAccessorsCommand(sublime_plugin.TextCommand):
	"""
	Toggle between dot and arrow accessors for C/C++ code.
	 * Dot Example:   test.data
	 * Arrow Example: test.data
	
	Multiple Edit Test:
	 * Put multiple cursors:  test.data.data2
	 * Select both regions:   test->data().not_data
	"""
	
	def run(self, edit, **args):
		for region in reversed(self.view.sel()):
			if region.size() == 0:
				# Try one character beside the region to see what we've got
				next_char = self.view.substr(region.begin())
				if next_char == ".":
					# Replace with arrow
					edit_region = sublime.Region(region.begin(), region.end() + 1)
					self.view.replace(edit, edit_region, "->")
				elif next_char == "-":
					# Check if it's an arrow
					edit_region = sublime.Region(region.begin(), region.end() + 2)
					if self.view.substr(edit_region) == "->":
						self.view.replace(edit, edit_region, ".")
						# TODO: Switch back to behind the edit point
				elif next_char == ">":
					# Check if it's an arrow (we might be in the middle, e.g. after dot conversion)
					edit_region = sublime.Region(region.begin() - 1, region.end() + 1)
					if self.view.substr(edit_region) == "->":
						self.view.replace(edit, edit_region, ".")
			else:
				# Try to see if the selected text is something we want to replace
				sel_text = self.view.substr(region)
				if sel_text == ".":
					self.view.replace(edit, region, "->")
				elif sel_text == "->":
					self.view.replace(edit, region, ".")

###########################################

