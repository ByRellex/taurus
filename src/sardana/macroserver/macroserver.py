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

import re

from taurus import Device, Factory
from taurus.core import TaurusEventType
from taurus.core.util import CaselessDict, ThreadPool
from taurus.core.tango.sardana.motion import Motion, MotionGroup
from taurus.core.tango.sardana.pool import registerExtensions

from sardana import InvalidId, ElementType
from sardana.sardanaevent import EventType
from sardana.sardanamodulemanager import ModuleManager
from sardana.sardanamanager import SardanaElementManager, SardanaIDManager

from msbase import MSObject
from mscontainer import MSContainer
from msdoor import MSDoor
from msmacromanager import MacroManager
from mstypemanager import TypeManager
from msenvmanager import EnvironmentManager
from msparameter import ParamType

CHANGE_EVT_TYPES = TaurusEventType.Change, TaurusEventType.Periodic

ET = ElementType
#: dictionary dict<:data:`~sardana.ElementType`, :class:`tuple`> 
#: where tuple is a sequence:
#: 
#: #. type string representation
#: #. family
#: #. internal macro server class
#: #. automatic full name
TYPE_MAP = {
    ET.Door : ("Door", "Door", MSDoor, "door/{macro_server.name}/{name}"),
}

class TypeData(object):
    """Information for a specific Element type"""
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

#: dictionary
#: dict<:data:`~sardana.ElementType`, :class:`~sardana.macroserver.macroserver.TypeData`>
TYPE_MAP_OBJ = {}
for t, d in TYPE_MAP.items():
    o = TypeData(type=t, name=d[0], family=d[1], klass=d[2] ,
                 auto_full_name=d[3])
    TYPE_MAP_OBJ[t] = o


class MacroServer(MSContainer, MSObject, SardanaElementManager, SardanaIDManager):
    
    All = "All"
    
    MaxParalellMacros = 5
    
    def __init__(self, full_name, name=None, macro_path=None,
                 environment_db=None):
        # dict<str, Pool>
        # key   - device name (case insensitive)
        # value - Pool object representing the device name
        self._pools = CaselessDict()
        self._max_parallel_macros = self.MaxParalellMacros
        self._path_id = None
        
        MSContainer.__init__(self)
        MSObject.__init__(self, full_name=full_name, name=name, id=InvalidId,
                          macro_server=self)
        
        self._thread_pool = ThreadPool(name="MacServTP",
                                       Psize=self.get_max_parallel_macros(),
                                       Qsize=50)
        
        registerExtensions()
        
        self._type_manager = TypeManager(self)
        self._environment_manager = EnvironmentManager(self,
                                        environment_db=environment_db)
        self._macro_manager = MacroManager(self, macro_path=macro_path)

    def serialize(self, *args, **kwargs):
        kwargs = MSObject.serialize(self, *args, **kwargs)
        kwargs['type'] = self.__class__.__name__
        kwargs['id'] = InvalidId
        kwargs['parent'] = None
        return kwargs
    
    def get_type(self):
        return ElementType.MacroServer
    
    def get_thread_pool(self):
        """Returns the global pool of threads for the Pool
        
        :return: the global pool of threads object
        :rtype: taurus.core.util.ThreadPool"""
        return self._thread_pool
    
    thread_pool = property(get_thread_pool)
    
    def add_job(self, job, callback=None, *args, **kw):
        self._thread_pool.add(job, callback, *args, **kw)
    
    def set_environment_db(self, environment_db):
        """Sets the environment database.
        
        :param env_db:
            environment database name
        :type env_db:
            str
        """
        self.environment_manager.setEnvironmentDb(environment_db)
    
    def set_python_path(self, path):
        mod_man = ModuleManager()
        if self._path_id is not None:
            mod_man.remove_python_path(self._path_id)
        self._path_id = mod_man.add_python_path(path)

        
    def set_macro_path(self, macro_path):
        """Sets the macro path.
        
        :param macro_path:
            macro path
        :type macro_path:
            seq<str>
        """
        self.macro_manager.setMacroPath(macro_path)
    
    # --------------------------------------------------------------------------
    # Pool related methods
    # --------------------------------------------------------------------------
    
    def set_pool_names(self, pool_names):
        """Registers a new list of device pools in this manager
        
        :param pool_names: sequence of pool names
        :type pool_names: seq<str>"""
        for pool in self._pools.values():
            elements_attr = pool.getAttribute("Elements")
            elements_attr.removeListener(self.on_pool_elements_changed)
        
        for name in pool_names:
            self.debug("Creating pool %s", name)
            pool = Device(name)
            if pool is None:
                self.error('Could not create Pool object for %s' % name)
                continue
            self._pools[name] = pool
            elements_attr = pool.getAttribute("Elements")
            elements_attr.addListener(self.on_pool_elements_changed)
    
    def get_pool_names(self):
        """Returns the list of names of the pools this macro server is connected
        to.
        
        :return:
            the list of names of the pools this macro server is connected to
        :rtype:
            seq<str>"""
        return self._pools.keys()
    
    def get_pool(self, pool_name):
        """Returns the device pool object corresponding to the given device name
        or None if no match is found.
        
        :param pool_name: device pool name
        :type pool_name: str
        :return: Pool object or None if no match is found"""
        return self._pools.get(pool_name)
    
    def get_pools(self):
        """Returns the list of pools this macro server is connected to.
        
        :return: the list of pools this macro server is connected to
        :rtype: seq<Pool>"""
        return self._pools.values()
    
    def on_pool_elements_changed(self, evt_src, evt_type, evt_value):
        if evt_type not in CHANGE_EVT_TYPES:
            return
        self.fire_event(EventType("PoolElementsChanged"), evt_value)
    
    # --------------------------------------------------------------------------
    # Door related methods
    # --------------------------------------------------------------------------
    
    def create_element(self, **kwargs):
        type = kwargs['type']
        elem_type = ElementType[type]
        name = kwargs['name']
        
        kwargs['macro_server'] = self
        
        td = TYPE_MAP_OBJ[elem_type]
        klass = td.klass
        auto_full_name = td.auto_full_name
        
        full_name = kwargs.get("full_name", auto_full_name.format(**kwargs))
        
        self.check_element(name, full_name)
        
        id = kwargs.get('id')
        if id is None:
            kwargs['id'] = id = self.get_new_id()
        else:
            self.reserve_id(id)
        elem = klass(**kwargs)
        ret = self.add_element(elem)
        self.fire_event(EventType("ElementCreated"), elem)
        return ret
    
    def create_door(self, **kwargs):
        return self.create_element(type="Door", **kwargs)
        
    # --------------------------------------------------------------------------
    # General access to elements
    # --------------------------------------------------------------------------
    
    def get_elements_info(self):
        return self.get_remote_elements_info() + self.get_local_elements_info()
    
    def get_remote_elements_info(self):
        return [ elem.serialize()
            for pool in self.get_pools()
                for elem in pool.getElements() ]
    
    def get_local_elements_info(self):
        # fill macro library info
        ret = [ macrolib.serialize()
            for macrolib in self.get_macro_libs().values() ]
        # fill macro info
        ret += [ macro.serialize()
            for macro in self.get_macros().values() ]
        # fill parameter type info
        ret += [ paramtype.serialize()
            for paramtype in self.get_data_types().values() ]
        
        return ret
    
    # --------------------------------------------------------------------------
    # macro execution
    # --------------------------------------------------------------------------
    
    def set_max_parallel_macros(self, nb):
        assert nb > 0, "max parallel macros number must be > 0"
        self.thread_pool.size = nb
        self._max_parallel_macros = nb
        
    def get_max_parallel_macros(self):
        return self._max_parallel_macros
    
    max_parallel_macros = property(get_max_parallel_macros,
        set_max_parallel_macros, doc="maximum number of macros which can "
        "execute at the same time")
    
    @property
    def macro_manager(self):
        return self._macro_manager
    
    @property
    def environment_manager(self):
        return self._environment_manager
    
    @property
    def type_manager(self):
        return self._type_manager
    
    # --------------------------------------------------------------------------
    # (Re)load code
    # --------------------------------------------------------------------------
    
    def reload_macro_lib(self, lib_name):
        manager = self.macro_manager
        
        old_lib = manager.getMacroLib(lib_name)
        new_elements, changed_elements, deleted_elements = [], [], []
        if old_lib is not None:
            changed_elements.append(old_lib)
        
        new_lib = manager.reloadMacroLib(lib_name)
        
        if old_lib is None:
            new_elements.extend(new_lib.get_macros())
            new_elements.append(new_lib)
        else:
            new_names = set([ macro.name for macro in new_lib.get_macros() ])
            old_names = set([ macro.name for macro in old_lib.get_macros() ])
            changed_names = set.intersection(new_names, old_names)
            deleted_names = old_names.difference(new_names)
            new_names = new_names.difference(old_names)
            
            for new_name in new_names:
                new_elements.append(new_lib.get_macro(new_name))
            for changed_name in changed_names:
                changed_elements.append(new_lib.get_macro(changed_name))
            for deleted_name in deleted_names:
                deleted_elements.append(old_lib.get_macro(deleted_name))
        
        evt = { "new" : new_elements, "change" : changed_elements,
                "del" : deleted_elements }
        self.fire_event(EventType("ElementsChanged"), evt)
    reload_macro_lib.__doc__ = MacroManager.reloadMacroLib.__doc__
    
    def reload_macro_libs(self, lib_names):
        for lib_name in lib_names:
            self.reload_macro_lib(lib_name)
    
    def reload_macro(self, macro_name):
        macro_info = self.macro_manager.getMacro(macro_name)
        lib_name = macro_info.module_name
        self.reload_macro_lib(lib_name)
    
    def reload_macros(self, macro_names):
        lib_names = set()
        for macro_name in macro_names:
            macro_info = self.macro_manager.getMacro(macro_name)
            lib_names.add(macro_info.module_name)
        self.reload_macro_libs(lib_names)
    
    def get_macro_lib(self, lib_name):
        return self.macro_manager.getMacroLib(lib_name)
    get_macro_lib.__doc__ = MacroManager.getMacroLib.__doc__
    
    def get_macro_libs(self, filter=None):
        return self.macro_manager.getMacroLibs(filter=filter)
    get_macro_libs.__doc__ = MacroManager.getMacroLibs.__doc__
    
    def get_macro_lib_names(self):
        return self.macro_manager.getMacroLibNames()
    get_macro_lib_names.__doc__ = MacroManager.getMacroLibNames.__doc__
    
    def get_macro(self, name):
        return self.macro_manager.getMacro(name)
    get_macro.__doc__ = MacroManager.getMacro.__doc__

    def get_macros(self, filter=None):
        return self.macro_manager.getMacros(filter=filter)
    get_macros.__doc__ = MacroManager.getMacros.__doc__
    
    def get_macro_names(self):
        return self.macro_manager.getMacroNames()
    get_macro_names.__doc__ = MacroManager.getMacroNames.__doc__
    
    def get_macro_libs_summary_info(self):
        libs = self.get_macro_libs()
        ret = []
        for module_name, macro_lib_info in libs.items():
            elem = "%s (%s)" % (macro_lib_info.name, macro_lib_info.file_path)
            ret.append(elem)
        return ret
    
    def get_macro_classes_summary_info(self):
        macros = self.get_macros()
        ret = []
        for macro_info in macros:
            elem = "%s (%s)" % (macro_info.name, macro_info.file_path)
            ret.append(elem)
        return ret
    
    def get_or_create_macro_lib(self, lib_name, macro_name=None):
        """Gets the exiting macro lib or creates a new macro lib file. If
        name is not None, a macro template code for the given macro name is 
        appended to the end of the file.
        
        :param lib_name:
            module name, python file name, or full file name (with path)
        :type lib_name: str
        :param macro_name:
            an optional macro name. If given a macro template code is appended
            to the end of the file (default is None meaning no macro code is
            added)
        :type macro_name: str
        
        :return:
            a sequence with three items: full_filename, code, line number is 0
            if no macro is created or n representing the first line of code for
            the given macro name.
        :rtype: seq<str, str, int>"""
        return self.macro_manager.getOrCreateMacroLib(lib_name,
                                                      macro_name=macro_name)
    get_or_create_macro_lib.__doc__ = MacroManager.getOrCreateMacroLib.__doc__
    
    def set_macro_lib(self, lib_name, code, auto_reload=True):
        module_name = self.macro_manager.setMacroLib(lib_name, code,
                                                     auto_reload=False)
        if auto_reload:
            self.reload_macro_lib(module_name)
        
    set_macro_lib.__doc__ = MacroManager.setMacroLib.__doc__
    
    # --------------------------------------------------------------------------
    # Data types
    # --------------------------------------------------------------------------
    
    def get_data_types(self):
        return self.type_manager.getTypes()
    get_data_types.__doc__ = TypeManager.getTypes.__doc__
    
    def get_data_type(self, type_name):
        return self.type_manager.getTypeObj(type_name)
    get_data_type.__doc__ = TypeManager.getTypeObj.__doc__
    
    def get_data_type_names(self):
        return self.type_manager.getTypeNames()
    get_data_type_names.__doc__ = TypeManager.getTypeNames.__doc__
    
    def get_data_type_names_with_asterisc(self):
        return self.type_manager.getTypeListStr()
    get_data_type_names_with_asterisc.__doc__ = TypeManager.getTypeListStr.__doc__
    
    # --------------------------------------------------------------------------
    # Doors
    # --------------------------------------------------------------------------
    
    def get_doors(self):
        return self.get_elements_by_type(ElementType.Door)
    
    def get_door_names(self):
        return [ door.full_name for door in self.get_doors() ]
    
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # Environment access methods
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    
    def get_env(self, key=None, door_name=None, macro_name=None):
        """Gets the environment matching the given parameters:
        
               - door_name and macro_name define the context where to look for
                 the environment. If both are None, the global environment is
                 used. If door name is None but macro name not, the given macro
                 environment is used and so on...
               - If key is None it returns the complete environment, otherwise
                 key must be a string containing the environment variable name.
        
        :param key:
            environment variable name [default: None, meaning all environment]
        :type key: str
        :param door_name:
            local context for a given door [default: None, meaning no door
            context is used]
        :type door_name: str
        :param macro_name:
            local context for a given macro [default: None, meaning no macro
            context is used]
        :type macro_name: str
        
        :return: a :obj:`dict` containing the environment
        :rtype: :obj:`dict`
        
        :raises: UnknownEnv"""
        return self.environment_manager.getEnv(key=key, macro_name=macro_name,
                                               door_name=door_name)
    
    def set_env(self, key, value):
        """Sets the environment key to the new value and stores it persistently.
        
        :param key: the key for the environment
        :param value: the value for the environment
        
        :return: a tuple with the key and value objects stored"""
        env_man = self.environment_manager
        if env_man.hasEnv(key):
            evt_type = "change"
        else:
            evt_type = "new"
        
        k,v = self.environment_manager.setEnv(key, value)
        
        evt = { evt_type : { k : v } }
        self.fire_event(EventType("EnvironmentChanged"), evt)
        return k,v
    
    def set_env_obj(self, data):
        """Sets the environment key to the new value and stores it persistently.
        
        :param key: the key for the environment
        :param value: the value for the environment
        
        :return: a tuple with the key and value objects stored"""
        env_man = self.environment_manager
        
        new, change = {}, {}
        for key, value in data.items():
            d = new
            if env_man.hasEnv(key):
                d = change
            d[key] = value
        
        ret = env_man.setEnvObj(data)
        
        evt = dict(new=new, change=change)
        self.fire_event(EventType("EnvironmentChanged"), evt)
        return ret
    
    def change_env(self, data):
        env_man = self.environment_manager
        new_change_env = data.get('new', {})
        new_change_env.update(data.get('change', {}))
        del_env = data.get('del', [])
        
        new, change = {}, {}
        for key, value in new_change_env.items():
            d = new
            if env_man.hasEnv(key):
                d = change
            d[key] = value
        
        del_keys = env_man.unsetEnv(del_env)
        env_man.setEnvObj(new_change_env)
        
        evt = dict(new=new, change=change)
        evt['del'] = del_keys
        self.fire_event(EventType("EnvironmentChanged"), evt)
    
    def unset_env(self, key):
        """Unsets the environment for the given key.
        
        :param key: the key for the environment to be unset"""
        ret = self.environment_manager.unsetEnv(key)
        evt = { 'del' : { key : None } }
        self.fire_event(EventType("EnvironmentChanged"), evt)
        return ret
        
    def has_env(self, key, macro_name=None, door_name=None):
        return self.environment_manager.hasEnv(key,
            macro_name=macro_name, door_name=door_name)
    
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # General object access methods
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    
    def get_object(self, name, type_class=All, subtype=All, pool=All):
        objs = self.find_objects(name, type_class, subtype, pool)
        if len(objs) == 0:
            return None
        if len(objs) > 1:
            raise AttributeError('More than one object named "%s" found' % name)
        return objs[0]

    def get_objects(self, names, type_class=All, subtype=All, pool=All):
        return self.find_objects(names, type_class=type_class, subtype=subtype,
                                 pool=pool)

    def find_objects(self, param, type_class=All, subtype=All, pool=All):
        if isinstance(param, (str, unicode)):
            param = param,
        
        if type_class == MacroServer.All:
            type_name_list = self.get_data_type_names()
        else:
            if isinstance(type_class, (str, unicode)):
                type_name_list = type_class,
            else:
                type_name_list = type_class
        obj_set = set()
        param = [ '^%s$' % x for x in param ]
        re_objs = map(re.compile, param, len(param)*(re.IGNORECASE,))
        re_subtype = re.compile(subtype, re.IGNORECASE)
        for type_name in type_name_list:
            type_class_name = type_name
            if type_class_name.endswith('*'):
               type_class_name = type_class_name[:-1]
            type_inst = self.get_data_type(type_class_name)
            if not type_inst.hasCapability(ParamType.ItemList):
                continue
            for name, obj in type_inst.getObjDict(pool=pool).items():
                for re_obj in re_objs:
                    if re_obj.match(name) is not None:
                        obj_type = obj.getType()
                        if (subtype is MacroServer.All or \
                            re_subtype.match(obj.getType())) and \
                           obj_type != "MotorGroup":
                            obj_set.add(obj)
        return list(obj_set)
    
    def get_motion(self, elems, motion_source=None, read_only=False, cache=True,
                   decoupled=False):
        if motion_source is None:
            motion_source = self.get_pools()
        
        motion_klass = Motion
        if decoupled: # and len(elems)>1:
            motion_klass = MotionGroup
        return motion_klass(elems, motion_source)
    
    def get_elements_with_interface(self, interface):
        ret=CaselessDict()
        for pool in self.get_pools():
            ret.update(pool.getElementsWithInterface(interface))
        return ret

    def get_element_with_interface(self, name, interface):
        for pool in self.get_pools():
            element = pool.getElementWithInterface(name, interface)
            if element is not None:
                return element
    
    def get_controllers(self):
        return self.get_elements_with_interface("Controller")
    
    def get_moveables(self):
        return self.get_elements_with_interface("Moveable")
    
    def get_motors(self):
        return self.get_elements_with_interface("Motor")
    
    def get_pseudo_motors(self):
        return self.get_elements_with_interface("PseudoMotor")
    
    def get_io_registers(self):
        return self.get_elements_with_interface("IORegister")
    
    def get_measurement_groups(self):
        return self.get_elements_with_interface("MeasurementGroup")
    
    def get_exp_channels(self):
        return self.get_elements_with_interface("ExpChannel")
        
    def get_counter_timers(self):
        return self.get_elements_with_interface("CTExpChannel")
    
    def get_0d_exp_channels(self):
        return self.get_elements_with_interface("ZeroDExpChannel")
    
    def get_1d_exp_channels(self):
        return self.get_elements_with_interface("OneDExpChannel")
    
    def get_2d_exp_channels(self):
        return self.get_elements_with_interface("TwoDExpChannel")
    
    def get_pseudo_counters(self):
        return self.get_elements_with_interface("PseudoCounter")
    
    def get_instruments(self):
        return self.get_elements_with_interface("Instrument")
    
    def get_controller(self, name):
        return self.get_element_with_interface(name, "Controller")
    
    def get_moveable(self, name):
        return self.get_element_with_interface(name, "Moveable")
    
    def get_motor(self, name):
        return self.get_element_with_interface(name, "Motor")
    
    def get_pseudo_motor(self, name):
        return self.get_element_with_interface(name, "PseudoMotor")
    
    def get_io_register(self, name):
        return self.get_element_with_interface(name, "IORegister")
    
    def get_measurement_group(self, name):
        return self.get_element_with_interface(name, "MeasurementGroup")
    
    def get_exp_channel(self, name):
        return self.get_element_with_interface(name, "ExpChannel")
        
    def get_counter_timer(self, name):
        return self.get_element_with_interface(name, "CTExpChannel")
    
    def get_0d_exp_channel(self, name):
        return self.get_element_with_interface(name, "ZeroDExpChannel")
    
    def get_1d_exp_channel(self, name):
        return self.get_element_with_interface(name, "OneDExpChannel")
    
    def get_2d_exp_channel(self, name):
        return self.get_element_with_interface(name, "TwoDExpChannel")
    
    def get_pseudo_counter(self, name):
        return self.get_element_with_interface(name, "PseudoCounter")
    
    def get_instrument(self, name):
        return self.get_element_with_interface(name, "Instrument")