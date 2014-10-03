#!/usr/bin/env python
# -*- coding: utf-8 -*-
##    Copyright 2014 Rasmus Scholer Sorensen, rasmusscholer@gmail.com
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=W0142,C0103

"""

Common module for parsing and handling arguments.


"""
import argparse
from itertools import chain


def make_parser(prog='gelannotator'):
    """

    Default values if not specified are None for most arguments,
    except for switches (store_true/false), where it is the default is the opposite of the first given switch.
    E.g. if add_argument(--dothis, action='store_true'), dothis will default to False, unless
    of course, you specifically also add default=True. You can also add default=None for switches!

    When two switches with same destination are defined, the first will define the default value.
    E.g. below, both linearize and no-linearize are defined having dest=linearize.
    Because linearize is defined first, the default value of linearize will be False.

    """
    ap = argparse.ArgumentParser()


    ap.add_argument('gelfile')


    ## For geltransformer -- also nice for gel annotator

    ap.add_argument('--linearize', action='store_true', default=None, help="Linearize gel (if e.g. typhoon).")
    ap.add_argument('--no-linearize', action='store_false', dest='linearize', help="Linearize gel (if e.g. typhoon).")
    ap.add_argument('--dynamicrange', nargs=2, help="""
                    Specify dynamic range (contrast). Valid argumets are '<min> <max>', '<max>' and 'auto'.
                    <min> and <max> can be provided as absolute values e.g. '300 5000',
                    or as percentage values, e.g. '0.1% 99%'.
                    If percentage values are given, the dynamic range are set so the <min> of the pixels are below the range
                    and 100%-<max> of the pixels are above the dynamic range.
                    If only one integer argument is given if is assumed to be the max, and min is set to 0.
                    If specifying 'auto', the software automatically try to determine a suitable contrast range.""")
    #ap.add_argument('--autorange', action='store_true', help="Dynamic range, min max, e.g. 300 5000.")
    ap.add_argument('--crop', nargs=4, type=int, metavar=('left', 'upper', 'right', 'lower'), help="Crop image to this box (left upper right lower) aka (x1 y1 x2 y2), e.g. 500 100 1200 400.")
    ap.add_argument('--invert', action='store_true', default=None, help="Invert gel data, so zero is white, high intensity black.")
    ap.add_argument('--no-invert', action='store_false', dest='invert', help="Do not invert image data. Zero will be black, high intensity white.")
    ap.add_argument('--convertgelto', default='png', help="Convert gel to this format.")
    #ap.add_argument('--png', action='store_true', help="Save as png.")
    ap.add_argument('--overwrite', action='store_true', default=True, help="Overwrite existing png.")
    ap.add_argument('--no-overwrite', action='store_false', dest='overwrite', help="Do not overwrite existing png.")
    ap.add_argument('--rotategel', type=int, dest='textrotation', help="Angle to rotate gel (counter-clockwise).")


    if prog == 'gelannotator':
        ap.add_argument('--pngfile', help="Use this pngfile instead of the specified gelfile.")
        ap.add_argument('--reusepng', action='store_true', dest='reusepng', help="Prefer png file over the specified gelfile.")
        ap.add_argument('--no-reusepng', action='store_false', dest='reusepng', help="Do not use pngfile, even if it is specified.")

        ap.add_argument('--yoffset', type=int, help="Y offset (how far down the gel image should be).") #, default=100
        ap.add_argument('--ypadding', type=int, help="Vertical space between gel image and annotations.") #, default=100
        ap.add_argument('--xmargin', nargs=2, type=int, help="Margin (right and left).") # , default=(30, 40)
        ap.add_argument('--xspacing', type=int, help="Force a certain x spacing.")
        ap.add_argument('--extraspaceright', type=int, help="Add additional padding/whitespace to the right (if the gel is not wide enought for the last annotation).")

        ap.add_argument('--textrotation', type=int, dest='textrotation', help="Angle to rotate text (counter-clockwise).")
        ap.add_argument('--fontsize', type=int, help="Specify default font size.")
        ap.add_argument('--fontfamily', help="Specify default font family, e.g. arial or MyriadPro.")
        ap.add_argument('--fontweight', help="Font weight: normal | bold | bolder | lighter | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | inherit.")

        ap.add_argument('--textfmt', help="How to format the lane annotations, e.g. '{idx} {name}'. Format keys include: idx, name")

        ap.add_argument('--yamlfile', help="Load options from YAML file, update and save.")
        ap.add_argument('--saveyamlto', help="Force saving yaml to this file when complete.")
        ap.add_argument('--no-update-yaml', dest='updateyaml', action='store_false', help="Do not update yaml settings after run to reflect the settings used.")
        ap.add_argument('--update-yaml', dest='updateyaml', action='store_true', help="Update yaml settings after run to reflect the settings used.")

        ap.add_argument('--no-embed', dest='embed', action='store_false', help="Do not embed image data in svg file, link to the file instead. (default is to embed)")
        ap.add_argument('--embed', action='store_true', help="Embed image data in svg file. (default)")

        ap.add_argument('--annotationsfile', help="Load lane annotations from this file. If not specified, will try to guess the right file.")

        ap.add_argument('--openwebbrowser', action='store_true', help="Open annotated svg file in default webbrowser.")


        #ap.add_argument('--svgtopng', action='store_true', help="Save svg as png (requires cairo package).")

    #xmargin=(40, 30), xspacing=None, yoffset=100
    #textfmt="{idx} {name}", laneidxstart=0

    return ap

def parseargs(prog='gelannotator'):#, partial=False, mockstring=None):
    """
    Perform parsing.
    """
    ap = make_parser(prog=prog)
    #if partial:
    #    # parse_known_args will not raise errors if sys.argv arguments not recognized by this parser.
    #    # This is useful if you have several parts of the program parsing the arguments.
    #    return ap.parse_known_args()
    return ap.parse_args()


def mergedicts(*dicts):
    """
    Merges dictionaries in dicts.
    <dicts> is a sequence of dictionaries.
    The returned dict will have all keys from all dictionaries in dicts.
    The latter items in dicts take precedence of earlier, i.e.:
    >>> mergedicts({3:1, {3:2})
    {3:2}
    However only non-None items take precedence:
    >>> mergedicts({4:1}, {4:None})
    {4:1}
    However, the returned dict *will* have all keys from all dicts, even if they are None:
    >>> mergedicts({6:None, 7:None}, {6:None, 8:None})
    {6:None, 7:None, 8:None}
    In total:
    >>> mergedicts({1:1, 3:1, 4:1, 5:None, 6:None, 7:None}, {2:2, 3:2, 4:None, 5:2, 6:None, 8:None})
    {1:1, 2:2, 3:2, 4:1, 5:2, 6:None, 7:None, 8:None}
    """
    # Make dict with all keys from all keys, set to None:
    #print "dicts:", dicts
    ret = dict.fromkeys(set(chain(*(d.keys() for d in dicts))))
    #print "mergedicts: initial dict:", ret
    for d in dicts:
        ret.update({k: v for k, v in d.items() if v is not None})
    return ret


def mergeargs(argsns, argsdict=None, excludeNone=True, precedence='argsdict'):
    """
    Merges arguments from <argsdict> and <argsns> (argparse Namespace or similar object).
    The returned dict is guaranteed to have all keys from both argsns and argsdict,
    even if they are None and <excludeNone> is True.
    <excludeNone> only refers to whether elements with value of None still takes
    preference when the dicts are merged.
    * argns can be either an object or a dict.
    * argsdict, if specified must be a dict or None.
    * If argsdict is not specified, an empty dict is used. The result is then simply
        argsns.__dict__.copy().
    * If excludeNone is set to True (default), only non-None values from argsns is loaded to argsdict.
    * <precedence> can be either 'argsns' or 'argsdict'. If 'argsdict' is specified (default),
        entries in the argsdict take precedence over entries in argsns.
        If specifying 'argsns', entries in argsns will override entries in argsdict.
    Be careful if you specify default values for argparse and set presedence='argsns' !

    Typical usage is a function that that takes both an argsns argument and has **kwargs:
        def mock(a, b=None, argsns=None, **kwargs)
            kwargs = argsnstodict(argsns, kwargs)

    Note that when 'drippling down' kwargs:
    * a function should only specify keys that it does not pass on and which it does not intend to
        get from argsns.
    * If a function needs to use a variable but also pass this on, it should use it as a kwargs item.
    * Does that make sense?
    """
    if argsdict is None:
        argsdict = {}
    if argsns is None:
        nsdict = {}
    else:
        try:
            nsdict = argsns.__dict__
        except AttributeError:
            nsdict = argsns
    ret = dict.fromkeys(set(argsdict.keys()) | set(nsdict.keys()))
    # Specify which order to merge depending on which dict takes precedence (should be the last)
    mergeorder = (nsdict, argsdict) if precedence == 'argsdict' else (argsdict, nsdict)
    if excludeNone:
        return mergedicts(*mergeorder)
    for d in mergeorder:
        ret.update({k: v for k, v in d.items() if v is not None} if excludeNone else d)
    return ret


def argsnstodict(argsns):
    return argsns.__dict__