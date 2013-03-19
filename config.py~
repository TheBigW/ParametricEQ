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
			params.append( param )
		print "num params : ", len(params)
		return params
	def save( self, params ):
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

