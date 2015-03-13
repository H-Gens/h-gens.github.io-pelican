Title: Converting IPython notebooks to PDFs
Date: 2015-01-04 09:35
Tags: python


A few weeks ago I wanted to share an [IPython notebook](http://ipython.org/) with a friend who did not have IPython installed.  The natural choice was to convert it to a PDF, which turned out to be more painful than expected.  The following instructions are written for Windows users and IPython v2.3.  The only dependency is [wkhtmltopdf](http://wkhtmltopdf.org/) (webkit HTML to PDF).  


1.  In the notebook editor, export to HTML.  
  a. File -> Download as -> HTML (.html)  
  b. You will need to manually collect required images and place them in the correct relative path to the exported file or change src="..." paths in the HTML.  
2.  If you use a custom.css file then either edit the exported HTML file to point to it or copy the file to the expected path.  
  a. custom.css lives in _~/.ipython/profile_default/static/custom/_  
3. Open the exported HTML file in your browser and save it (_File -> Save As_).  
  a. While this step seems unnecessary, without it my MathJax markup was the wrong font size in the resulting PDF.  
4. Run wkhtmltopdf on the saved copy from the previous step.  
  a. __wkhtmltopdf.exe -s Letter -L 40mm -R 40mm -T 20mm -B 20mm --javascript-delay 5000 infile.html outfile.pdf__  

The __-s__ argument sets the page size.  The __-L, -R, -T, -B__ arguments set the left/right/top/bottom margins.  The __--javascript-delay__ argument gives the MathJax javascript time to run (the time required probably depends on document size).  There are many options available in wkhtmltopdf, which can be viewed by calling the executable from the command line without any arguments.  


