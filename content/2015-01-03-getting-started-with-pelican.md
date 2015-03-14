Title: Getting started with Pelican and IPython notebooks
Date: 2015-01-03 09:19
Tags: python


This site was created with the static site generator, [Pelican](http://docs.getpelican.com/en/3.5.0/).  I chose Pelican in order to use [jakevdp's](https://jakevdp.github.io) liquid_tags notebook [plugin](https://github.com/getpelican/pelican-plugins/blob/master/liquid_tags/notebook.py) that allows for posting a subset of [IPython](http://ipython.org/) notebook cells.  The comments below are for Pelican v3.5.0, IPython v1.2, and a December 30, 2014 clone of pelican-plugins.  

Below are steps used to install Pelican.  [Python](https://www.python.org/downloads/) and [node.js](http://nodejs.org/download/) must be installed (I was unable to generate posts containing IPython notebook files without node.js).  Console/terminal commands are contained in brackets.  

An older version of IPython is needed because the CSS class names used for python syntax highlighting changed in IPython v2.3.  The liquid_tags notebook plugin appears to only know about the v1.2 CSS class names.  For example, in an IPython notebook, a function named <code>foo</code> gets wrapped in a class by way of a <code>&lt;span&gt;</code> element.  In IPython v1.2 this becomes <code>&lt;span class="nf"&gt;foo&lt;/span&gt;</code>, but in v2.3 this is <code>&lt;span class="cm-def"&gt;foo&lt;/span&gt;</code> (I used Chrome to inspect the elements).  I'm not smart enough to fix it, but I assume the problem begins in the plugin's notebook.custom_highlighter() function.  Inside this function a call is made to <code>HtmlFormatter(cssclass='highlight-ipynb')</code> where <code>HtmlFormatter</code> comes from the [Pygments](http://pygments.org/) library.  



Quick pelican setup
----------------

1. Make a dedicated directory to house the site's contents and change into it.  
2. Set up a virtual environment  
  a. __[virtualenv env]__  
  b. __\[env\scripts\activate\]__   
  c. __[pip install pelican markdown ipython==1.2]__  
3. Install plugins/themes  
  a. __[git clone https://github.com/getpelican/pelican-plugins.git]__  
  b. __[git clone https://github.com/getpelican/pelican-themes.git]__  
  c. Find other themes by looking at other users' github repositories (e.g. [octopress](https://github.com/jakevdp/pelican-octopress-theme), [middle-theme](https://github.com/danielfrg/middle-theme))  
4. __[pelican-quickstart]__  // see [here](http://mathamy.com/migrating-to-github-pages-using-pelican.html) for a list of questions that are asked  
5. Configure Pelican via pelicanconf.py  
  a. _DELETE_OUTPUT_DIRECTORY = False_  
  b. _PLUGIN_PATHS = ['path/to/pelican-plugins']_  
  c. _PLUGINS = ['liquid_tags.notebook', 'liquid_tags.literal']_  
  d. _EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8') if os.path.exists('_nb_header.html') else None_  
  e. _NOTEBOOK_DIR = 'notebooks'_  
  f. _THEME = 'path/to/theme'_  
  g. _LOAD_CONTENT_CACHE = False_  
6. Edit the chosen theme's 'base.html' and add <code>{% if EXTRA_HEADER %}{{ EXTRA_HEADER }}{% endif %}</code> to the <code>&lt;head&gt;</code> block  
7. Configure 'content' directory  
  a. __[mkdir content/images]__  
  b. __[mkdir content/notebooks]__  
8. Run the site generator with __[make html]__ or __[make regenerate]__
9. Serve the site locally with __[make serve]__ or regenerate files + serve with __[make devserver]__ if not on Windows.  


Posts are written in markdown by the user and stored in content/, where each post's filename should have extension 'md'.  Notebooks are incorporated in a markdown post with:

	{% literal notebook file.ipynb cells[i:j] %} 

The 'cells' argument is optional and can be omitted; the slices are standard python syntax.  The _LOAD_CONTENT_CACHE_ setting should be False if notebooks are edited after they're added to content/notebooks/.  Otherwise, the cached version is used by Pelican.  

Initially, __[make html]__ must be run twice because '\_nb_header.html' is only generated after the first run.  This file contains all the CSS/JS present in an IPython notebook.  

Math blocks were left-aligned in IPython v1.2 but are centered in IPython v2.3, which is the preferred behavior.  To force centering of math blocks while using v1.2, I made copy of \_nb_header.html, edited it to include the addition below, and pointed to it in pelicanconf.py's _EXTRA_HEADER_ setting.  

	<style type="text/css">
	.MathJax_Display{text-align: center !important;}
	</style>



Repositories
------------
My choice was to have two repositories.  

- Inside the master directory where __[pelican-quickstart]__ is run.  
- A subdirectory of the above that holds the content pushed to the web server.  

The former has a .gitignore file that contains:  

	*.pyc
	cache/
	env/
	output/
	username.github.io/

The latter repository is a [GitHub Pages](https://pages.github.com/) repository.  The 'output/' directory generated by Pelican is copied to this repository.    

This site's repository containing the raw Pelican content can be found [here](https://github.com/h-gens/h-gens.github.io-pelican).  The generated site can be found [here](https://github.com/h-gens/h-gens.github.io).  



Helpful references
--------------
- [Migrating from Octopress to Pelican](https://jakevdp.github.io/blog/2013/05/07/migrating-from-octopress-to-pelican/)  
- [How to setup Github User Page with Pelican](http://ntanjerome.org/blog/how-to-setup-github-user-page-with-pelican/)  
- [Migrating to GitHub Pages using Pelican](http://mathamy.com/migrating-to-github-pages-using-pelican.html)  
- [Getting started](http://docs.getpelican.com/en/3.1.1/getting_started.html) (Pelican docs)
- [tags-vs-categories in Pelican](http://pirsquared.org/blog/pelican-tags-vs-categories.html)



Script to summarize available Pelican themes
----------------------
	"""
	Ugly script used to summarize all pelican-themes.
	https://github.com/getpelican/pelican-themes.

	Place this script one level below THEMES_DIR.
	It will generate summary.html containing the themes.  
	"""
	import os
	from collections import OrderedDict as od

	THEMES_DIR = 'pelican-themes'

	# first, discover all themes that have screenshots
	# each screenshot's filename is stored
	contents = os.listdir(THEMES_DIR)
	accumulated_screenshots = od()
	for entry in contents:
	    theme_directory = os.path.join(THEMES_DIR, entry)
	    if os.path.isdir(theme_directory) and entry != '.git':
	        theme_contents = os.listdir(theme_directory)
	        accumulated_screenshots[entry] = []
	        for theme_file in theme_contents:
	            if theme_file[-3:] in ('jpg', 'png', 'gif'):
	                accumulated_screenshots[entry].append(theme_file)

	# second, create an HTML file
	# the IMG elements point to the accumulated screenshots
	to_write = ['<html><body>\n']
	for theme, screenshots in accumulated_screenshots.iteritems():
	    path = os.path.join(THEMES_DIR, theme)
	    for i, screenshot in enumerate(screenshots):
	        if i == 0:
	            # print the theme's name only once
	            to_write.append('<h1>%s</h1><br />\n' % theme)
	        screenshot_path = os.path.join(path, screenshot)
	        to_write.append('<center>\n')
	        to_write.append(
	            '<img src="%s" height=500>\n' % screenshot_path
	        )
	        to_write.append('</center><br />\n')
	    to_write.append('<br />\n')
	to_write.append('</body></html>\n')

	with open('summary.html', 'w') as f:
	    f.writelines(to_write)

