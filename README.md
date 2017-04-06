AligorithTools - Sublime Text Plugin
====================================

A random assortment of plugins/tools for improving my workflow in Sublime Text.

There are the following categories of tools:
* **Latex Tools** - Utilities for making it more convenient to work with Latex. Most of these are
  specialist tools for dealing with the particular problems I have in my setup.
  
  * **"Replace Quotes with \enquote{...}" / "Fix Quotes"**  
    This replaces all the manual <code>``...''</code> type quotes with a <code>\enquote{...}</code> call, 
    and all <code>`...'</code> quotes with <code>\squote{...}</code>. Also, it fixes any quotes which use
    Unicode curly quotes (e.g. copy-and-pasted from Word).
    
  * **"Preview Quotes to \\enquote{...}"**  
    This highlights all the changes that the *"Fix Quotes"* tool will apply, making it easier to check if it
    will be well behaved in your file.
    
  * **"Clear \\enquote{...} Preview"**
    This clears all the highlights that the *"Preview"* tool added (in case you decide to not go ahead).

* **General Tools** - General text manipulation tools

* **Color Tools** - Tools to make it easier to work with colours


Requirements
------------

These have only been tested with Sublime Text 2. It may be possible to run this with ST3 too,
but I haven't tested them on there yet.
  

