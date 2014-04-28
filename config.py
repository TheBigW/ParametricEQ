# MyEqualizer.py
# Copyright (C) 2013 - Tobias Wenig
#			tobiaswenig@yahoo.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from EQBandParams import EQBandParams
from gi.repository import GConf

EQUALIZER_GCONF_PREFIX = '/apps/rhythmbox/plugins/ParametricEQ'

class Config:
	def getAllPresets(self):
		conf = GConf.Client.get_default()
		baseCfgPath = EQUALIZER_GCONF_PREFIX
		numPresets = conf.get_int( baseCfgPath + '/num_presets')
		presets = []
		for i in range(0, numPresets):
			currCfgKey = baseCfgPath + '/preset' + str(i)
			presets.append( conf.get_string(currCfgKey) )
		return presets

	def saveAllPresets(self, conf, presets):
		conf = GConf.Client.get_default()
		baseCfgPath = EQUALIZER_GCONF_PREFIX
		numPresets = len(presets)
		conf.set_int( baseCfgPath + '/num_presets', numPresets)
		for i in range(0, numPresets):
			currCfgKey = baseCfgPath + '/preset' + str(i)
			conf.set_string(currCfgKey, presets[i] )
		
	def getCurrPreset(self):
		conf = GConf.Client.get_default()
		return conf.get_string( EQUALIZER_GCONF_PREFIX + '/current_preset' )

	def setCurrPreset(self, conf, preset):
		conf.set_string( EQUALIZER_GCONF_PREFIX + '/current_preset', preset )
		#check if already in presets list - if not add
		presets = self.getAllPresets()
		if preset not in presets:
			presets.append(preset)
			self.saveAllPresets(conf, presets)
	def load(self, preset):	
		conf = GConf.Client.get_default()
		if preset == None:
			preset = self.getCurrPreset()	
		params = []
		if preset == None:
			#no preset: probably no config -> leave
			return params
		baseCfgPath = EQUALIZER_GCONF_PREFIX + '/' + preset
		numBands = conf.get_int( baseCfgPath + '/num_bands' )
		if numBands == None:
			numBands = 0
		print("numbands : ", numBands)
		for i in range(0, numBands):
			param = EQBandParams(0.0, 0.0, 0.0)
			currCfgKey = baseCfgPath + '/EQBand' + str(i)
			print("reading config from :", currCfgKey)
			param.bandwidth = conf.get_float( currCfgKey + '/bandWidth' )
			print("param.bandwidth : ", param.bandwidth)
			param.frequency = conf.get_float( currCfgKey + '/frequency' )
			print("param.frequency : ", param.frequency)		
			param.gain = conf.get_float( currCfgKey + '/gain' )
			print("param.gain : ", param.gain)
			eqType = conf.get_int( currCfgKey + '/type' )
			if None == eqType:			
				param.bandType = 0
			else:
				param.bandType = eqType
			params.append( param )
		print("num params : ", len(params))
		params.sort()#ascending order for frequency
		return params
	def save( self, params, preset ):
		params.sort()#ascending order for frequency
		conf = GConf.Client.get_default()
		self.setCurrPreset(conf, preset)
		numBands = len(params)
		print("numbands : ", numBands)
		baseCfgPath = EQUALIZER_GCONF_PREFIX + '/' + preset
		conf.set_int( baseCfgPath + '/num_bands', numBands )
		for i in range(0, numBands):			
			currCfgKey = baseCfgPath + '/EQBand' + str(i)
			print("saving config to :", currCfgKey)
			conf.set_float( currCfgKey + '/bandWidth', params[i].bandwidth )
			conf.set_float( currCfgKey + '/frequency', params[i].frequency )
			conf.set_float( currCfgKey + '/gain', params[i].gain )
			conf.set_int( currCfgKey + '/type', params[i].bandType )
