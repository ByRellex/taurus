#!/usr/bin/env python

##############################################################################
##
## This file is part of Sardana
##
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

""" """

__docformat__ = 'restructuredtext'

from .PoolDevice import *
from .Controller import *
from .Motor import *
from .MotorGroup import *
from .CTExpChannel import *
from .MeasurementGroup import *
from .Pool import *

def prepare_pool(util):
    util.add_class(PoolClass, Pool)
    util.add_class(ControllerClass, Controller)
    util.add_class(MotorClass, Motor)
    util.add_class(CTExpChannelClass, CTExpChannel)
    util.add_class(MotorGroupClass, MotorGroup)
    util.add_class(MeasurementGroupClass, MeasurementGroup)

def main_pool():
    import sardana.tango.util
    sardana.tango.util.run(prepare_pool)

