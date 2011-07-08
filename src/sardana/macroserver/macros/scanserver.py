"""
    Macro library containning scanserver related macros for the macros 
    server Tango device server as part of the Sardana project.
    
"""

from macro    import *

class _scanserver:
    """Internal class used as a base class for the scanserver macros"""
 
    
    def prepare(self):
        self.prepared = False
        ctrl_name = self.getEnv('ActiveScanServer')
        
        ctrl_list = self.findObjs('.*', type_class=Type.Controller)

        self.ctrl = None
        if not ctrl_name is None:
            ctrl_name = ctrl_name.lower()
            for c in ctrl_list:
                if c.getName().lower() == ctrl_name:
                    self.ctrl = c
					
        if self.ctrl is None:
            self.output("ActiveScanServer controller not found")
            return
        
        self.pool = self.ctrl.getPool()
        ctrl_klass = self.pool.getCtrlClassByName(self.ctrl.klass)
		
        self.prepared = True
        
    def sendSetToCtrl(self,cmd_line):
        self.debug("invoking pool.SendToController('%s', '%s')" % (self.ctrl.name,cmd_line))
        
        try:
            res = self.pool.SendToController([self.ctrl.name,cmd_line])
            if res.lower() != "true":
                 self.output("Send command to controller was NOT successfull!")
                 self.output("Command result was: %s" % res)
                 self.output("Macro execution had no effect")
                 return None
        except:
            self.output("An error occurred when trying to send command to controller")
            raise
        return res

class start_scan(Macro, _scanserver):
    """The start_scan macro is used to send the command start to the ScanServer."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        self.pool.SendToController([self.ctrl.name, 'start'])

class set_scan_sensors(Macro, _scanserver):
    """The set_scan_sensors macro is used to set the sensors in the scan server."""
    
    param_def = [
       ['sensor_1', Type.String, None, "Sensor to be added"],
       ['sensor_2', Type.String, " ", "Sensor to be added"],
       ['sensor_3', Type.String, " ", "Sensor to be added"],
       ['sensor_4', Type.String, " ", "Sensor to be added"],
       ['sensor_5', Type.String, " ", "Sensor to be added"],
       ['sensor_6', Type.String, " ", "Sensor to be added"],
       ['sensor_7', Type.String, " ", "Sensor to be added"],
       ['sensor_8', Type.String, " ", "Sensor to be added"],
       ['sensor_9', Type.String, " ", "Sensor to be added"],
       ['sensor_10', Type.String, " ", "Sensor to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "sensors %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])
	
class get_scan_sensors(Macro, _scanserver):
    """The get_scan_sensors macro is used to read the sensors set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?sensors'])
        
        self.output(ret)
		
class set_scan_actuators(Macro, _scanserver):
    """The set_scan_actuators macro is used to set the actuators in the scan server."""
    
    param_def = [
       ['actuator_1', Type.String, None, "Actuator to be added"],
       ['actuator_2', Type.String, " ", "Actuator to be added"],
       ['actuator_3', Type.String, " ", "Actuator to be added"],
       ['actuator_4', Type.String, " ", "Actuator to be added"],
       ['actuator_5', Type.String, " ", "Actuator to be added"],
       ['actuator_6', Type.String, " ", "Actuator to be added"],
       ['actuator_7', Type.String, " ", "Actuator to be added"],
       ['actuator_8', Type.String, " ", "Actuator to be added"],
       ['actuator_9', Type.String, " ", "Actuator to be added"],
       ['actuator_10', Type.String, " ", "Actuator to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "actuators %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])
	
class get_scan_actuators(Macro, _scanserver):
    """The get_scan_actuators macro is used to read the actuators set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?actuators'])
        
        self.output(ret)

class set_scan_actuators2(Macro, _scanserver):
    """The set_scan_actuators2 macro is used to set the actuators2 in the scan server."""
    
    param_def = [
       ['actuator_1', Type.String, None, "Actuator to be added"],
       ['actuator_2', Type.String, " ", "Actuator to be added"],
       ['actuator_3', Type.String, " ", "Actuator to be added"],
       ['actuator_4', Type.String, " ", "Actuator to be added"],
       ['actuator_5', Type.String, " ", "Actuator to be added"],
       ['actuator_6', Type.String, " ", "Actuator to be added"],
       ['actuator_7', Type.String, " ", "Actuator to be added"],
       ['actuator_8', Type.String, " ", "Actuator to be added"],
       ['actuator_9', Type.String, " ", "Actuator to be added"],
       ['actuator_10', Type.String, " ", "Actuator to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "actuators2 %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])
	
class get_scan_actuators2(Macro, _scanserver):
    """The get_scan_actuators2 macro is used to read the actuators2 set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?actuators2'])
        
        self.output(ret)


		
class set_scan_integrationTimes(Macro, _scanserver):
    """The set_scan_integrationTimes macro is used to set the integration times in the scan server."""
    
    param_def = [
       ['integrationtime_1', Type.String, None, "Integration Time to be added"],
       ['integrationtime_2', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_3', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_4', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_5', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_6', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_7', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_8', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_9', Type.String, " ", "Integration Time to be added"],
       ['integrationtime_10', Type.String, " ", "Integration Time to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "integrationtimes %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])

class get_scan_integrationTimes(Macro, _scanserver):
    """The get_scan_integrationTimes macro is used to read the integration times set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?integrationtimes'])
        
        self.output(ret)

		
class set_scan_trajectories(Macro, _scanserver):
    """The set_scan_trajectories macro is used to set the trajectories in the scan server."""
    
    param_def = [
       ['points_in_trajectory', Type.String, None, "Points in trajectory"],
       ['number_of_actuators', Type.String, None, "Number of actuators"],
       ['trajectorypoint_1', Type.String, None, "Trajectory Point to be added"],
       ['trajectorypoint_2', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_3', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_4', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_5', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_6', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_7', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_8', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_9', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_10', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_11', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_12', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_13', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_14', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_15', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_16', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_17', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_18', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_19', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_20', Type.String, " ", "Trajectory Point to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "trajectories %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])
		
class get_scan_trajectories(Macro, _scanserver):
    """The get_scan_trajectories macro is used to read the trajectories set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?trajectories'])
        
        self.output(ret)
		
class set_scan_trajectories2(Macro, _scanserver):
    """The set_scan_trajectories2 macro is used to set the trajectories2 in the scan server."""
    
    param_def = [
       ['points_in_trajectory2', Type.String, None, "Points in trajectory2"],
       ['number_of_actuators2', Type.String, None, "Number of actuators2"],
       ['trajectorypoint_1', Type.String, None, "Trajectory Point to be added"],
       ['trajectorypoint_2', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_3', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_4', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_5', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_6', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_7', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_8', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_9', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_10', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_11', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_12', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_13', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_14', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_15', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_16', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_17', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_18', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_19', Type.String, " ", "Trajectory Point to be added"],
       ['trajectorypoint_20', Type.String, " ", "Trajectory Point to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "trajectories2 %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])
		
class get_scan_trajectories2(Macro, _scanserver):
    """The get_scan_trajectories2 macro is used to read the trajectories2 set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?trajectories2'])
        
        self.output(ret)

		
class set_scan_timebases(Macro, _scanserver):
    """The set_scan_timebases macro is used to set the timebases in the scan server."""
    
    param_def = [
       ['timebase_1', Type.String, None, "Timebase to be added"],
       ['timebase_2', Type.String, " ", "Timebase to be added"],
       ['timebase_3', Type.String, " ", "Timebase to be added"],
       ['timebase_4', Type.String, " ", "Timebase to be added"],
       ['timebase_5', Type.String, " ", "Timebase to be added"],
       ['timebase_6', Type.String, " ", "Timebase to be added"],
       ['timebase_7', Type.String, " ", "Timebase to be added"],
       ['timebase_8', Type.String, " ", "Timebase to be added"],
       ['timebase_9', Type.String, " ", "Timebase to be added"],
       ['timebase_10', Type.String, " ", "Timebase to be added"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "timebases %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])
	
class get_scan_timebases(Macro, _scanserver):
    """The get_scan_timebases macro is used to read the timebases set in the scanserver."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?timebases'])
        
        self.output(ret)

        
class scan_start(Macro, _scanserver):
    """The scan_start macro is used to start a scan with the scanserver device."""
	
    def get_state(self):
        ret = self.pool.SendToController([self.ctrl.name, '?state'])
		
        return ret
	
    def get_data(self):
        ret = self.pool.SendToController([self.ctrl.name, '?data'])
		
        return ret
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, 'start'])
        
        self.output(ret)
        
        self.output("Wait scan running")
        self.flushOutput()
   
        ret = self.get_state()
		
        while ret == "6": # MOVING -> Scan Running
            ret = self.get_state()
		
        if ret == "0":
            self.output("Scan finished")
            self.output(self.get_data())
		
        if ret == "7":
            self.output("Scan paused")
            self.output(self.get_data())
		
class scan_pause(Macro, _scanserver):
    """The scan_pause macro is used to pause a scan with the scanserver device."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, 'pause'])
        
        self.output(ret)
		
class scan_resume(Macro, _scanserver):
    """The scan_resume macro is used to resume a scan with the scanserver device."""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, 'resume'])
        
        self.output(ret)
		
class scan_clean(Macro, _scanserver):
    """The scan_clean macro is used to initialize to null the scan server attributes: sensors, actuators, actuators2, timebases, trajectories"""
	
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, 'clean'])
        
        self.output(ret)

class get_scan_extra_attribute(Macro, _scanserver):
    """The get_scan_extra_attribute macro is used to read the value of the ScanServer attribute given as an argument."""
    
    param_def = [
       ['attribute_name', Type.String, None, "Attribute in ScanServer device to be read"]
    ]    
	
    def prepare(self, *pars):
        _scanserver.prepare(self)
    
    def run(self, *pars):
        if not self.prepared:
            return
        cmd_line = "?scan_extra_attribute %s" %" ".join([str(p) for p in pars])
        
        ret = self.pool.SendToController([self.ctrl.name,cmd_line])
        
        self.output(ret)

		
class set_scan_extra_attribute(Macro, _scanserver):
    """The set_scan_extra_attribute macro is used to set attributes of the ScanServer device."""
    
    param_def = [
       ['attribute_name', Type.String, None, "Attribute in ScanServer device to be set"],
       ['value_1', Type.String, None, "Attribute parameter"],
       ['value_2', Type.String, " ", "Attribute parameter"],
       ['value_3', Type.String, " ", "Attribute parameter"],
       ['value_4', Type.String, " ", "Attribute parameter"],
       ['value_5', Type.String, " ", "Attribute parameter"],
       ['value_6', Type.String, " ", "Attribute parameter"],
       ['value_7', Type.String, " ", "Attribute parameter"],
       ['value_8', Type.String, " ", "Attribute parameter"],
       ['value_9', Type.String, " ", "Attribute parameter"],
       ['value_10', Type.String, " ", "Attribute parameter"],
       ['value_11', Type.String, " ", "Attribute parameter"],
       ['value_12', Type.String, " ", "Attribute parameter"],
       ['value_13', Type.String, " ", "Attribute parameter"],
       ['value_14', Type.String, " ", "Attribute parameter"],
       ['value_15', Type.String, " ", "Attribute parameter"],
       ['value_16', Type.String, " ", "Attribute parameter"],
       ['value_17', Type.String, " ", "Attribute parameter"],
       ['value_18', Type.String, " ", "Attribute parameter"],
       ['value_19', Type.String, " ", "Attribute parameter"],
       ['value_20', Type.String, " ", "Attribute parameter"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
    def run(self, * pars):
        if not self.prepared:
            return
        cmd_line = "scan_extra_attribute %s" %" ".join([str(p) for p in pars])
        ret = self.pool.SendToController([self.ctrl.name, cmd_line])

class get_scanserver_config(Macro, _scanserver):
    """The get_scanserver_config macro is used to get information about the configuration."""
    
    def prepare(self):
        _scanserver.prepare(self)
    
    def run(self):
        if not self.prepared:
            return
        
        ret = self.pool.SendToController([self.ctrl.name, '?sensors'])
        
        self.output(ret)
        
        ret = self.pool.SendToController([self.ctrl.name, '?actuators'])
        
        self.output(ret)
        
        ret = self.pool.SendToController([self.ctrl.name, '?actuators2'])
        
        self.output(ret)
        
        ret = self.pool.SendToController([self.ctrl.name, '?integrationtimes'])
        
        self.output(ret)
        
        ret = self.pool.SendToController([self.ctrl.name, '?trajectories'])
        
        self.output(ret)
        
        ret = self.pool.SendToController([self.ctrl.name, '?trajectories2'])
        
        self.output(ret)
        
        ret = self.pool.SendToController([self.ctrl.name, '?timebases'])
        
        self.output(ret)

class scan_save_config(Macro, _scanserver):
    """The scan_save_config macro is used to save the configuration."""
    
    param_def = [
       ['file_name', Type.String, "default_name.config", "Config file name"]
    ]    
    
    def prepare(self, file_name):
        _scanserver.prepare(self)
    
    def run(self, file_name):
        if not self.prepared:
            return
		
        fd = open(file_name,'w')
        
        ret = self.pool.SendToController([self.ctrl.name, '?sensors'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
        
        ret = self.pool.SendToController([self.ctrl.name, '?actuators'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
        
        ret = self.pool.SendToController([self.ctrl.name, '?actuators2'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
        
        ret = self.pool.SendToController([self.ctrl.name, '?integrationtimes'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
        
        ret = self.pool.SendToController([self.ctrl.name, '?trajectories'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
        
        ret = self.pool.SendToController([self.ctrl.name, '?trajectories2'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
        
        ret = self.pool.SendToController([self.ctrl.name, '?timebases'])
        
        self.output(ret)
        fd.write(ret)
        fd.flush()
		
        fd.write("Alternative parameter: \n")		
        fd.write("End \n")
		
        fd.close()     


class scan_load_config(Macro, _scanserver):
    """The scan_load_config macro is used to load the configuration from a file."""
    
    param_def = [
       ['file_name', Type.String, None, "Config file name"]
    ]    
    
    def prepare(self, file_name):
        _scanserver.prepare(self)
    
    def run(self, file_name):
        if not self.prepared:
            return
		
        fd = open(file_name,'r')
		
        ret = fd.readline()
        if ret.find("Sensors:") != -1:
			nb_sensors = 0
			send_str = 'sensors '
			ret = fd.readline()
			send_str += ret
			while ret.find("Actuators:") is -1:
				nb_sensors += 1
				ret = fd.readline()
				if ret.find("Actuators:") is -1:
					send_str += ret
			self.output(send_str)
			self.pool.SendToController([self.ctrl.name, send_str])
        if ret.find("Actuators:") != -1:
			nb_actuators = 0
			send_str = 'actuators '
			ret = fd.readline()
			send_str += ret
			while ret.find("Actuators2 (extern loop):") is -1:
				nb_actuators += 1
				ret = fd.readline()
				if ret.find("Actuators2 (extern loop):") is -1:
					send_str += ret
			self.output(send_str)
			self.pool.SendToController([self.ctrl.name, send_str])
        if ret.find("Actuators2 (extern loop):") != -1:
			nb_actuators2 = 0
			flag_write = 0
			send_str = 'actuators2 '
			ret = fd.readline()
			if ret.find("Integration times:") is -1:
				send_str += ret
				flag_write = 1
			while ret.find("Integration times:") is -1:
				nb_actuators2 += 1
				ret = fd.readline()
				if ret.find("Integration times:") is -1:
					send_str += ret
					flag_write = 1
			self.output(send_str)
			if flag_write is 1:
				self.pool.SendToController([self.ctrl.name, send_str])
        if ret.find("Integration times:") != -1:
			nb_integrationtimes = 0
			send_str = 'integrationtimes '
			ret = fd.readline()
			send_str += ret
			while ret.find("Trajectories:") is -1:
				nb_integrationtimes += 1
				ret = fd.readline()
				if ret.find("Trajectories:") is -1:
					send_str += ret
			self.output(send_str)
			self.pool.SendToController([self.ctrl.name, send_str])
        if ret.find("Trajectories:") != -1:
			nb_trajectories = 0
			send_str = 'trajectories '
			send_str += str(nb_integrationtimes)
			send_str += ' '
			send_str += str(nb_actuators)
			send_str += ' '
			ret = fd.readline()
			send_str += ret
			while ret.find("Trajectories2 (extern loop)") is -1:
				nb_trajectories += 1
				ret = fd.readline()
				if ret.find("Trajectories2 (extern loop)") is -1:
					send_str += ret
			self.output(send_str)
			self.pool.SendToController([self.ctrl.name, send_str])
        if ret.find("Trajectories2 (extern loop):") != -1:
			nb_trajectories2 = 0
			flag_write = 0
			send_str = 'trajectories2 '
			ret = fd.readline()
			tmp_str = ' '
			if ret.find("Timebases:") is -1:
				tmp_str += ret
				flag_write = 1
			while ret.find("Timebases:") is -1:
				nb_trajectories2 += 1
				ret = fd.readline()
				if ret.find("Timebases:") is -1:
					tmp_str += ret
					flag_write = 1
			nb_tmp = 0
			if nb_actuators2 is not 0:
				nb_tmp = nb_trajectories2/nb_actuators2
			send_str += str(nb_tmp)
			send_str += ' '
			send_str += str(nb_actuators2)
			send_str += tmp_str
			self.output(send_str)
			if flag_write is 1:
				self.pool.SendToController([self.ctrl.name, send_str])
        if ret.find("Timebases:") != -1:
			flag_write = 0
			send_str = 'timebases '
			ret = fd.readline()
			if ret.find("Alternative parameter:") is -1:
				send_str += ret
				flag_write = 1
			while ret.find("Alternative parameter:") is -1:
				ret = fd.readline()
				if ret.find("Alternative parameter:") is -1:
					send_str += ret
					flag_write = 1
			self.output(send_str)
			if flag_write is 1:
				self.pool.SendToController([self.ctrl.name, send_str])
        while ret.find("Alternative parameter:") != -1:
			send_str = 'scan_extra_attribute '
			ret = fd.readline()
			send_str += ret
			while ret.find("Alternative parameter:") is -1 and ret.find("End") is -1:
				ret = fd.readline()
				if ret.find("Alternative parameter:") is -1:
					send_str += ret
			self.output(send_str)
			self.pool.SendToController([self.ctrl.name, send_str])

class scan_start_list(Macro, _scanserver):
    """The scan_start_list macro is used to start serie of scans with different configurations."""
    param_def = [
       ['file_name', Type.String, None, "File with the list of configuration files"]
    ]    
	
    def prepare(self, * pars):
        _scanserver.prepare(self)
    
        
    def run_scan(self,cmd_line):
        self.debug("invoking execMacro('%s')" % (cmd_line))

        self.execMacro('scan_load_config',cmd_line)
        
        self.execMacro('scan_start')
	
    def run(self, file_name):


		
        fd = open(file_name,'r')
        
        ret = fd.readline()
        ret = ret.replace( "\n", "" )       
        ret = ret.replace( " ", "" )
		
        while ret.find("End") is -1:
        	self.output("Executing scan with configuration file " + ret)
        	self.flushOutput()
        	self.run_scan(ret)
        
        	ret = fd.readline()	       
        	ret = ret.replace( "\n", "" )       
        	ret = ret.replace( " ", "" )