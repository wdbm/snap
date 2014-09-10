#!/usr/bin/python

"""
################################################################################
#                                                                              #
# snap                                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# The program snap can move and resize windows.                                #
#                                                                              #
# copyright (C) 2014 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for    #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

Usage:
    snap.py [options]

Options:
    -h, --help    Show this help message.
    --version     Show the version and exit.
    -l, --left    Snap window left.
    -r, --right   Snap window right.
    -u, --up      Snap window up.
    -d, --down    Snap window down.
    --upleft      Snap window top left.
    --upright     Snap window top right.
    --downleft    Snap window bottom left.
    --downright   Snap window bottom right.
    --maximise    Maximise window.
    --minimise    Minimise window.
"""

version = "2014-09-10T2349"

from docopt import docopt
import logging
import Xlib
import Xlib.display
import subprocess

def main(options):

    global program
    program = Program()

    logger.info("dispay resolution: {displayResolutionWidth} * {displayResolutionHeight}".format(
        displayResolutionWidth = displayInformation(dimension = "width"),
        displayResolutionHeight = displayInformation(dimension = "height")
    ))

    if options["--left"]:
        snapWindow(position = "left")
    elif options["--right"]:
        snapWindow(position = "right")
    elif options["--up"]:
        snapWindow(position = "up")
    elif options["--down"]:
        snapWindow(position = "down")
    elif options["--upleft"]:
        snapWindow(position = "upleft")
    elif options["--upright"]:
        snapWindow(position = "upright")
    elif options["--downleft"]:
        snapWindow(position = "downleft")
    elif options["--downright"]:
        snapWindow(position = "downright")
    elif options["--minimise"]:
        snapWindow(position = "minimise")
    elif options["--maximise"]:
        snapWindow(position = "maximise")

class Program(object):

    def __init__(
        self,
        parent = None
        ):
        # name
        self.name = "snap"
        # logging
        global logger
        logger = logging.getLogger(__name__)
        logging.basicConfig()
        logger.level = logging.INFO
        logger.info("running {name}".format(name = self.name))

def displayInformation(
    dimension = None
    ):
    displayResolution = Xlib.display.Display().screen().root.get_geometry()
    if dimension == "width":
        return(displayResolution.width)
    elif dimension == "height":
        return(displayResolution.height)
    else:
        return(displayResolution.width, displayResolution.height)

def IDWindowFocus():
    return str(subprocess.check_output(["xdotool", "getwindowfocus"])).rstrip()

def snapWindow(
    windowID = IDWindowFocus(),
    position = None
    ):
    displayResolutionWidth = displayInformation(dimension = "width")
    displayResolutionHeight = displayInformation(dimension = "height")
    snapConfiguration = {
        "position": {
            "left": {
                "coordinatex": 0,
                "coordinatey": 0,
                "dimensionx": displayResolutionWidth/2,
                "dimensiony": displayResolutionHeight
            },
            "right": {
                "coordinatex": displayResolutionWidth/2,
                "coordinatey": 0,
                "dimensionx": displayResolutionWidth/2,
                "dimensiony": displayResolutionHeight
            },
            "up": {
                "coordinatex": 0,
                "coordinatey": 0,
                "dimensionx": displayResolutionWidth,
                "dimensiony": displayResolutionHeight/2
            },
            "down": {
                "coordinatex": 0,
                "coordinatey": displayResolutionHeight/2,
                "dimensionx": displayResolutionWidth,
                "dimensiony": displayResolutionHeight/2
            },
            "upleft": {
                "coordinatex": 0,
                "coordinatey": 0,
                "dimensionx": displayResolutionWidth/2,
                "dimensiony": displayResolutionHeight/2
            },
            "upright": {
                "coordinatex": displayResolutionWidth/2,
                "coordinatey": 0,
                "dimensionx": displayResolutionWidth/2,
                "dimensiony": displayResolutionHeight/2
            },
            "downleft": {
                "coordinatex": 0,
                "coordinatey": displayResolutionHeight/2,
                "dimensionx": displayResolutionWidth/2,
                "dimensiony": displayResolutionHeight/2
            },
            "downright": {
                "coordinatex": displayResolutionWidth/2,
                "coordinatey": displayResolutionHeight/2,
                "dimensionx": displayResolutionWidth/2,
                "dimensiony": displayResolutionHeight/2
            },
            "maximise": {
                "coordinatex": 0,
                "coordinatey": 0,
                "dimensionx": displayResolutionWidth,
                "dimensiony": displayResolutionHeight
            },
        }
    }
    if position == "minimise":
        logger.info(u"moving {position} window {windowID}".format(
            position = position,
            windowID = windowID
        ))
        subprocess.call([
            "xdotool",
            "windowminimize",
            windowID
        ])
    else:
        coordinatex = snapConfiguration["position"][position]["coordinatex"]
        coordinatey = snapConfiguration["position"][position]["coordinatey"]
        dimensionx  = snapConfiguration["position"][position]["dimensionx"]
        dimensiony  = snapConfiguration["position"][position]["dimensiony"]
        logger.info(u"moving {position} window {windowID} to co\u00F6rdinates ({coordinatex}, {coordinatey}) and resizing to {dimensionx} * {dimensiony}".format(
            position = position,
            windowID = windowID,
            coordinatex = coordinatex,
            coordinatey = coordinatey,
            dimensionx = dimensionx,
            dimensiony = dimensiony
        ))
        subprocess.call([
            "xdotool",
            "windowmove",
            windowID,
            str(coordinatex),
            str(coordinatey)
        ])
        subprocess.call([
            "xdotool",
            "windowsize",
            windowID,
            str(dimensionx),
            str(dimensiony)
        ])

if __name__ == '__main__':
    options = docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
