
TYPICAL USAGE AND SETUP
========================

The easiest way to invoke the Gel Annotator GUI is to create a shortcut
on your desktop to one of the shell scripts in the bin/ folder,
and then drag your gel files onto this shortcut.

For windows you should use the .bat file in bin/, while
on OS X and Linux you use the file ending with '.sh'.

Gel files can be either GEL/TIF files, or PNG/JPG.
The software will linearize GEL files by default.

You write the lanes in the text input area to the left.

The text area to the right shows a long list of options.

But, before we go through these, it might be informative to go through
the program's workflow:

 1. First, if you have a GEL or TIF file, or if you have asked
    the program to perform transformations (crop, rotate, scale, etc),
    then the program will create a PNG file that it can use for annotation.
    (If you are starting from a PNG file, this is simply used as-is.)

 2. Second, the program create a SVG file with the PNG file and the
    annotations from the left text area.

 3. Third, the program can use the SVG file to create a
    PNG image with annotations.

The third step is optional; the generated SVG file with annotations
is perfectly fine for most purposes, except the file size is a little large.



 PROGRAM OPTIONS
====================

Image related options:

    * crop: <left>, <top>, <right>, <bottom> to crop the gel.
        if you set cropfromedges to true, right and bottom are from the edge,
        otherwise they are absolute coordinates.
    * rotate: <angle> will rotate the gel.
        if you set rotateexpands to true, the image is expanded to accomodate
        the full image after rotation.
    * dynamicrange: <min>, <max> will set the minimum and maximum values
        of the dynamic range. Also known as adjusting the contrast ;-)

    * invert: If you set invert to true, the image is inverted. This is the default for GEL files.
    * linearize: perform linearization of GEL data. This is also default for GEL files.

Text annotation options:

    * fontfamily, fontsize, fontweight: used to change the font (duh)

    * textrotation: <angle> controls the angle of the lane annotations.

    * textfmt: can be used to format the lane annotation string.
        Default is "{name}", which just adds the annotation.
        Changing this to e.g. "{idx:02} - {name}" would add the lane
        number to the annotation: "01 - 10 bp marker".
        You can use laneidxstart to change the idx start number (default: 0)

    * yoffset and ypadding are used to control the vertical position of the
        lane annotations: Increasing yoffset will add more whitespace above the
        gel, making more room for the annotations. ypadding controls the
        vertical space between the top of the gel and the annotations.

    * xmargin, xspacing, extraspaceright are used to control the horizontal
        position of the annotations.
    * xmargin: <left>, <right> controls the horizontal position of the first
        and last annotation.
    * extraspacingright can be used to add a bit of extra space to the right,
        to avoid the rightmost annotations to be cropped.
    * xspacing can be used to manually override the horizontal distance
        between annotations.



Files and workflow options:

    * openwebbrowser : open the generated files when complete.

    * pngfile : use this png file for annotations (instead of the GEL file).

    * reusepng : if set to true, the program re-uses the previously generated PNG file
        if available, thus skipping the (somewhat slow) conversion of GEL data.

    * svgtopng : convert the annotated SVG file as PNG image.

    * annotationsfile : the file to read and write annotations to/from.

    * yamlfile : the file to read and write yaml settings to.





DEPENDENCIES:
===============

To run the program, you need Python. Python is very widely used and may already be
present on your system. (Open a terminal and type 'python' to check.)

    * GelUtils have been developed for python 2.7
    * It might work on python 3+, but it is a pain to ensure that it runs on both python 2 and 3.

If it is not present, use your package manager to install it.
If you are on Windows, you can either download the default python distribution
or one of the "fully featured" distributions:
    * python.org/download       - The "official" distribution.
    * continuum.io/downloads    - Anaconda, my favorite distribution.
    * enthought.com/downloads   - Enthought Canopy, another good distribution.
    * winpython.sourceforge.net - WinPython is another, slightly older distribution.


The primary dependencies are:
    * yaml (pyyaml)
    * Python Image Library, PIL - or Pillow.
    * numpy  (to linearize GEL data)
    * svgwrite (to create svg file with annotations)
    * cairo, cairosvg and cairocffi  -- or alternatively just imagemagick  (to generate the last, annotated PNG image)
    * six (for python 2 & 3 compatability)

You should be able to generate most of these through your distribution's package manager.
If it is not available through the package manager, use pip:
    >>> pip search <package>        - to search for packages.
    >>> pip install <package>       - to install a package.

For generating the last PNG image with annotations, the best results are produced
with cairosvg+cairocffi, and the Cairo toolkit.
However, these can be a bit tricky to install, especially on windows.

Here are some useful links to get Cairo installed on Windows:
* http://gtk-win.sourceforge.net/home/index.php/Main/Downloads
* https://pythonhosted.org/cairocffi/overview.html

Steps:
# Download and install Alexander Shaduri�s GTK+ installer from above. (Make sure to let the installer set PATH variable.)
# pip install cairocffi cairosvg

If you get "OSError: cannot load library libcairo.so.2: error 0x7e":
# Tried to install with compatability DLLs, tried to install in folder without spaces (C:\runtimes\),
    tried to install in lib\ dir rather than bin\, nothing helps...
    It could be an issue with compiler (VS 2007 vs 2010, for python 2 vs 3)
# Try to edit all cairocffi\__init__.py so it only has the .dll name.
# OSError: cannot load library C:\runtimes\GTK2-Runtime\lib\libcairo-2.dll: error 0xc1
# Install pycairo from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycairo ?
# Or tutorial: http://digitalpbk.blogspot.com.au/2012/03/installing-pygtk-pypango-and-pycairo-on.html
# Download from http://www.gtk.org/download/win64.php  -- downloading the "all-in-one" zip did the job,
## http://win32builder.gnome.org/gtk+-bundle_3.6.4-20131201_win64.zip - extract and add the \bin\ folder to your path.

If you already have ImageMagick installed you might want to just use this.
(ImageMagick  is one of the best and ubiquitous tools for converting and
transforming images - highly recommended.)