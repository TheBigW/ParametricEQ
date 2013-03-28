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

EQUALIZER_GCONF_PREFIX = '/apps/rhythmbox/plugins/equalizer'
EQUALIZER_NUM_BANDS = 'num_bands'

class Config:
	def load(self):	
		conf = GConf.Client.get_default() 		
		params = []
		numBands = conf.get_int(EQUALIZER_GCONF_PREFIX + '/' + EQUALIZER_NUM_BANDS)
		if numBands == None:
			numBands = 0
		print "numbands : ", numBands
		for i in range(0, numBands):
			param = EQBandParams(0.0, 0.0, 0.0)
			currCfgKey = EQUALIZER_GCONF_PREFIX + '/EQBand' + str(i)
			print "reading config from :", currCfgKey
			param.bandwidth = conf.get_float( currCfgKey + '/bandWidth' )
			print "param.bandwidth : ", param.bandwidth
			param.frequency = conf.get_float( currCfgKey + '/frequency' )
			print "param.frequency : ", param.frequency			
			param.gain = conf.get_float( currCfgKey + '/gain' )
			print "param.gain : ", param.gain
			eqType = conf.get_int( currCfgKey + '/type' )
			if None == eqType:			
				param.bandType = 0
			else:
				param.bandType = eqType
			params.append( param )
		print "num params : ", len(params)
		params = sorted(params, key=lambda par: par[0])#ascending order for frequency
		return params
	def save( self, params ):
		params = sorted(params, key=lambda par: par[0])#ascending order for frequency
		conf = GConf.Client.get_default()
		numBands = len(params)
		print "numbands : ", numBands
		conf.set_int(EQUALIZER_GCONF_PREFIX + '/' + EQUALIZER_NUM_BANDS, numBands)
		for i in range(0, numBands):			
			currCfgKey = EQUALIZER_GCONF_PREFIX + '/EQBand' + str(i)
			print "saving config to :", currCfgKey
			conf.set_float( currCfgKey + '/bandWidth', params[i].bandwidth )
			conf.set_float( currCfgKey + '/frequency', params[i].frequency )
			conf.set_float( currCfgKey + '/gain', params[i].gain )
			conf.set_int( currCfgKey + '/type', params[i].bandType )
