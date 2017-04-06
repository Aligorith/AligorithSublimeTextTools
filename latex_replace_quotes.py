# -*- coding: utf-8 -*-
#
# Plugin to replace ``blah'' with \enquote{blah}
# and `blah' with \squote{blah}
#
# Original Author: Joshua Leung
# Date: April 2017

import sublime
import sublime_plugin


######################################
# Highlight Region Identifiers (for LatexQuotesToEnquotePreview)

REGIONID_DOUBLE_QUOTES = "DoubleQuotes"
REGIONID_SINGLE_QUOTES = "SingleQuotes"

REGIONID_UNICODE_DOPEN_QUOTES = "UnicodeDOpenQuotes"
REGIONID_UNICODE_DCLOSE_QUOTES = "UnicodeDCloseQuotes"
REGIONID_UNICODE_SOPEN_QUOTES = "UnicodeSOpenQuotes"
REGIONID_UNICODE_SCLOSE_QUOTES = "UnicodeSCloseQuotes"

######################################
# General Utilities

# Find all the double quotes regions
def find_double_quotes(view):
	# Regex expression to find each quote pair + their contents + an extra character
	# Note: This is "v4" below
	matcher = r"([`]{2})([^`])(\\?.)*?([^'])([']{2})([)}\n\]\s])"
	return view.find_all(matcher, 0)
	
# Find all the single quotes regions
def find_single_quotes(view):
	matcher = r"([({\[\s])`([^`])(\\?.)*?([^'])'([)}\n\]\s])"
	return view.find_all(matcher, 0)
	

# ------------------------------------

# Clear all the regions associated with the highlights operator
def clear_quote_highlights(view):
	view.erase_regions(REGIONID_DOUBLE_QUOTES)
	view.erase_regions(REGIONID_SINGLE_QUOTES)
	
	view.erase_regions(REGIONID_UNICODE_DOPEN_QUOTES)
	view.erase_regions(REGIONID_UNICODE_DCLOSE_QUOTES)
	view.erase_regions(REGIONID_UNICODE_SOPEN_QUOTES)
	view.erase_regions(REGIONID_UNICODE_SCLOSE_QUOTES)


######################################
# Commands/Operators

# Run as "latex_quotes_to_enquote"
# TODO: Only apply within selected region - perhaps by intersecting regions?
class LatexQuotesToEnquoteCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		# Clear highlighting - It won't be valid anymore
		clear_quote_highlights(self.view)
		
		# Fix double quotes first, so that it is less likely to get confused
		# with the triple-quoted stuff
		self.fix_double_quotes(edit)
		self.fix_single_quotes(edit)
		
		# Also fix all unicode quotes (for the few files that have them...)
		self.fix_unicode_quotes(edit)
	
	
	# Fix the double quotes -> \enquote{}
	def fix_double_quotes(self, edit, **args):
		# NOTE: We must do this in reverse order, order else the offsets are all wrong
		for match in reversed(find_double_quotes(self.view)):
			# Get the matched string (it includes the paired quotes, and one extra character)
			matched_str = self.view.substr(match)
			
			# Get the "contents" only
			clean_str = matched_str[2:-3]
			
			# Also, grab the last character, since we'll need to tack 
			# it on to the end of the cleaned up tags
			last_ch  = matched_str[-1]
			
			# Construct the result
			result = "\\enquote{%s}%s" % (clean_str, last_ch)
			
			# Replace away!
			self.view.replace(edit, match, result)
			
			#print "Match: %d - %d" % (match.begin(), match.end())
			#print "    -> M \"%s\"" % (matched_str)
			#print "    -> C \"%s\"" % (clean_str)
	
	
	# Fix the single quotes -> \squote{}
	def fix_single_quotes(self, edit, **args):
		# NOTE: We must do this in reverse order, order else the offsets are all wrong
		for match in reversed(find_single_quotes(self.view)):
			# Get the matched string (it includes the paired quotes, and one extra on each side)
			matched_str = self.view.substr(match)
			
			# Get the "contents" only
			clean_str = matched_str[2:-2]
			
			# Also, grab the first+last characters, since we'll need to tack 
			# those on to the ends of the final string
			s_ch  = matched_str[0]
			e_ch  = matched_str[-1]
			
			# Construct the result
			result = "%s\\squote{%s}%s" % (s_ch, clean_str, e_ch)
			
			# Replace away!
			self.view.replace(edit, match, result)
			
			#print "Match: %d - %d" % (match.begin(), match.end())
			#print "    -> M \"%s\"" % (matched_str)
			#print "    -> C \"%s\"" % (clean_str)
	
	
	# Replace unicode curly quotes
	def fix_unicode_quotes(self, edit, **args):
		# Double Open/Close
		for match in reversed(self.view.find_all(u"“", 0)):
			self.view.replace(edit, match, "\\enquote{")
		
		for match in reversed(self.view.find_all(u"”", 0)):
			self.view.replace(edit, match, "}")
			
		
		# Single Pair
		# Note: Do the pair before the singles, so that we can catch the apostrophe's
		#       properly too afterwards
		for match in reversed(self.view.find_all(ur"‘(\\?.)*?’", 0)):
			# Get the matched string
			matched_str = self.view.substr(match)
			
			# Clean up the quotes
			clean_str = matched_str[1:-1]
			
			# Replace
			result = "\\squote{%s}" % (clean_str)
			self.view.replace(edit, match, result)
		
		
		# Left-Over Singles - This should just be for apostrophes
		for match in reversed(self.view.find_all(u"’", 0)):
			self.view.replace(edit, match, "'")



# Run as "preview_latex_quote_fixes"
# TODO: Only apply within selected region - perhaps by intersecting regions?
class PreviewLatexQuoteFixesCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		clear_quote_highlights(self.view)
		
		dcount = self.highlight_double_quotes()
		scount = self.highlight_single_quotes()
		ucount = self.highlight_unicode_quotes()
		
		msg = "Identified: %d Double, %d Single Pairs, %d Unicode..." % (dcount, scount, ucount)
		sublime.status_message(msg)
		print msg
	
	# Highlight the selected quotes
	def highlight_double_quotes(self):
		regions = find_double_quotes(self.view)
		scope = "string" # XXX
		icon = "circle"
		flags = sublime.DRAW_OUTLINED
		
		self.view.add_regions(REGIONID_DOUBLE_QUOTES, regions, scope, icon, flags)
		return len(regions)
			
	# Highlight the selected quotes
	def highlight_single_quotes(self):
		regions = find_single_quotes(self.view)
		scope = "constant.numeric" # XXX
		icon = "dot"
		flags = sublime.DRAW_OUTLINED
		
		self.view.add_regions(REGIONID_SINGLE_QUOTES, regions, scope, icon, flags)
		return len(regions)
	
	# Highlight the unicode quotes
	def highlight_unicode_quotes(self):
		# Common drawing options -> Basically, we want to mark these as errors that we're trying to fix
		scope = "invalid.deprecated"
		icon = "cross"
		flags = 0
		
		count = 0
		
		# Double-Quotes - Open
		regions = self.view.find_all(u"“", 0)
		count  += len(regions)
		self.view.add_regions(REGIONID_UNICODE_DOPEN_QUOTES, regions, scope, icon, flags)
		
		# Double Quotes - Close
		regions = self.view.find_all(u"”", 0)
		count  += len(regions)
		self.view.add_regions(REGIONID_UNICODE_DCLOSE_QUOTES, regions, scope, icon, flags)
		
		# Single-Quotes - Open
		regions = self.view.find_all(u"‘", 0)
		count  += len(regions)
		self.view.add_regions(REGIONID_UNICODE_SOPEN_QUOTES, regions, scope, icon, flags)
		
		# Single-Quotes - Close
		regions = self.view.find_all(u"’", 0)
		count  += len(regions)
		self.view.add_regions(REGIONID_UNICODE_SCLOSE_QUOTES, regions, scope, icon, flags)
		
		# Return the number of errors identified
		return count
		
	
# Run as "clear_latex_quote_preview"
class ClearLatexQuotePreviewCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		clear_quote_highlights(self.view)
	
	
######################################


tips = """
	# Get cursor position
	pos = self.view.sel()[0].begin()

	# Get range of first selection
	self.view.sel()[0].begin()/.end()
"""

double_match_notes = """
Test Suite -------------------------------------
1) Capture ``blah''
2) Capture ``blah blah''
3) Capture ``blah blagh bleh''
4) Don't capture ```blah'''
5) Should capture ``blah `bleh' blargh''
6) Capture (``blah'')
7) Capture {``blah''}
8) Capture ``blah'' blah

Attempts --------------------------------------
V1: Correct (1,2,3,6,7), Incorrect (4), Missed (5)
V1: "``([^`']+)''"
i.e.  `` (everything that isn't start/end quotes)  ''

V2: Correct(1,2,3,5,6,7), Incorrect (4 - All but last quote)
V2: ([`]{2})(\\?.)*?([']{2})

V3: Captures all, with excess
V3: ([`]{2})(\\?.)*?([']{2})([)}\n\]\s])

V4: All except 4
V4: ([`]{2})([^`])(\\?.)*?([^'])([']{2})([)}\n\]\s])
i.e. ([`]{2})     ([^`])           (\\?.)*?         ([^'])     ([']{2})  ([)}\n\]\s])
     Start pair | Skip 3rd | Match Contents as #3 | Skip 3rd | End pair | Excess "Word End"
"""

single_match_notes = """
Test Suite ------------------------------------------
1) Capture  `blah'
2) Capture  `blah blah blah'
3) Capture (`blah')
4) Capture {`blah'}
5) Don't capture ```noob'''
6) Don't capture ``nada''
7) Don't capture   don't worry''
8) Don't capture ``blah `bleh' blargh''

-----------------------------------------------------

V1: Incorrect (8)
V1: `([^`])(\\?.)*?([^'])'([)}\n\]\s])

V2: ([({\[\s])`([^`])(\\?.)*?([^'])'([)}\n\]\s])

"""		
		
