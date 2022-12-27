#!/usr/bin/env python3
# Copyright (C) 2013-2017 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class Aereni(Boxes):
    """Box for Aereni project"""

    ui_group = "Box"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("outside")
        self.argparser.add_argument(
            '--x', action='store', type=int, default=80,
            help='profondeur of the box'
        )
        self.argparser.add_argument(
            '--y', action='store', type=int, default=130,
            help='large of the box'
        )
        self.argparser.add_argument(
            '--h', action='store', type=int, default=180,
            help='height of the box'
        )
        self.argparser.add_argument(
            "--triangle", action="store", type=float, default=25.,
            help="Sides of the triangles holding the lid in mm")
        self.argparser.add_argument(
            "--d1", action="store", type=float, default=2.,
            help="Diameter of the inner lid screw holes in mm")
        self.argparser.add_argument(
            "--d2", action="store", type=float, default=3.,
            help="Diameter of the lid screw holes in mm")
        self.argparser.add_argument(
            "--d3", action="store", type=float, default=3.,
            help="Diameter of the mounting screw holes in mm")
        self.argparser.add_argument(
            "--d4", action="store", type=float, default=30.,
            help="Diameter of the PM holes in mm")
        self.argparser.add_argument(
            "--outsidemounts", action="store", type=boolarg, default=True,
            help="Add external mounting points")
        self.argparser.add_argument(
            "--holedist", action="store", type=float, default=7.,
            help="Distance of the screw holes from the wall in mm")
        self.argparser.add_argument(
            "--pmdist", action="store", type=float, default=30.,
            help="Distance of the screw holes from the wall in mm")

    def wallMid(self):
        t = self.thickness
        self.fingerHolesAt(self.x-(t*2), self.y * 0.8, self.triangle, 90)
        self.fingerHolesAt(self.x-(t*2), self.y * 0.01, self.triangle, 90)
        self.hole(self.x / 2, self.h - 90, d=self.d4)
        self.hole(self.x / 2, self.h - 140, d=self.d4)

    def wallTop(self):
        t = self.thickness
        self.fingerHolesAt(self.x-t, self.y * 0.8, self.triangle, 90)
        self.fingerHolesAt(self.x-t, self.y * 0.01, self.triangle, 90)

    def wall1(self):
        t = self.thickness
        self.fingerHolesAt(t, self.h*0.3, self.x - t, 0)
        self.hole(self.x / 2, self.h - self.d4, d=25)
        self.fingerHolesAt(self.x-t*1.5, self.h*0.3, 25, 90)
        self.fingerHolesAt(self.x-t*1.5, self.h-25, 25, 90)
        self.hexHolesRectangle(self.x, self.h * 0.3-5)

    def wall2(self):
        t = self.thickness
        self.hexHolesRectangle(self.y, self.h * 0.25+5)
        self.rectangularHole(5, self.h * 0.65, 115, 110, r=0, center_x=False, center_y=True)


    def wall3(self):
        t = self.thickness
        self.fingerHolesAt(t, self.h*0.3, self.x - t, 0)
        self.fingerHolesAt(self.x-t*1.5, self.h*0.3, 25, 90)
        self.fingerHolesAt(self.x-t*1.5, self.h-25, 25, 90)
        self.hexHolesRectangle(self.x, self.h * 0.25+5)

    def wall4(self):
        t = self.thickness
        self.hexHolesRectangle(self.y, self.h * 0.25+5)

    def render(self):

        t = self.thickness
        self.h = h = self.h + 2*t # compensate for lid
        x, y, h = self.x, self.y, self.h
        d1, d2, d3, d4 =self.d1, self.d2, self.d3, self.d4
        hd = self.holedist
        pd = self.pmdist
        tr = self.triangle
        trh = tr / 3.

        if self.outside:
            self.x = x = self.adjustSize(x)
            self.y = y = self.adjustSize(y)
            self.h = h = h - 3*t

        self.rectangularWall(x,
                             h,
                             "efff",
                             callback=[self.wall1],
                             move="right",
                             label="Wall 1")
        self.rectangularWall(y,
                             h,
                             "eFfF",
                             callback=[self.wall2],
                             move="up",
                             label="Wall 2")
        self.rectangularWall(y,
                             h,
                             "eFfF",
                             callback=[self.wall4],
                             label="Wall 4")
        self.rectangularWall(x,
                             h,
                             "efff",
                             callback=[self.wall3],
                             move="left up",
                             label="Wall 3")
        self.rectangularWall(x,
                             y,
                             "fefe",
                             callback=[self.wallMid],
                             move="right",
                             label="middle")
        self.rectangularWall(x,
                             y,
                             "FFFF",
                             callback=[self.wallTop],
                             move='up',
                             label="Top")

        self.rectangularTriangle(tr, tr, "ffe", num=4,
            callback=[None, lambda: self.hole(trh, trh, d=d1)])
