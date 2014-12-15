# config.py
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

from EQBandParams import EQBandParams, Presets, Preset
from gi.repository import GConf

EQUALIZER_GCONF_PREFIX = '/apps/rhythmbox/plugins/ParametricEQ'

class Config:

    @staticmethod
    def loadPreset(preset):
        conf = GConf.Client.get_default()
        params = []
        baseCfgPath = EQUALIZER_GCONF_PREFIX + '/' + preset
        numBands = conf.get_int( baseCfgPath + '/num_bands' )
        if numBands == None:
            numBands = 0
        print("numbands : ", numBands)
        for i in range(0, numBands):
            param = EQBandParams(0.0, 0.0, 0.0)
            currCfgKey = baseCfgPath + '/EQBand' + str(i)
            param.bandwidth = conf.get_float( currCfgKey + '/bandWidth' )
            param.frequency = conf.get_float( currCfgKey + '/frequency' )		
            param.gain = conf.get_float( currCfgKey + '/gain' )
            eqType = conf.get_int( currCfgKey + '/type' )
            param.bandType = eqType
            param.maxGain = conf.get_float( currCfgKey + '/loudnesMaxGain' )
            param.maxVolumePercentage = conf.get_float( currCfgKey + '/maxVolumePercentage' )
            param.minVolumePercentage = conf.get_float( currCfgKey + '/minVolumePercentage' )
            param.loudnesEnabled = conf.get_bool(currCfgKey + '/loudnesEnabled')

            params.append( param )
        params.sort()#ascending order for frequency
        return Preset(preset, params)
    @staticmethod
    def saveParams(params):
        params.sort()#ascending order for frequency
        conf = GConf.Client.get_default()
        numBands = params.getNumBands()
        baseCfgPath = EQUALIZER_GCONF_PREFIX + '/' + params.presetName
        conf.set_int( baseCfgPath + '/num_bands', numBands )
        for i in range(0, numBands):
            currCfgKey = baseCfgPath + '/EQBand' + str(i)
            conf.set_float( currCfgKey + '/bandWidth', params.bandParams[i].bandwidth )
            conf.set_float( currCfgKey + '/frequency', params.bandParams[i].frequency )
            conf.set_float( currCfgKey + '/gain', params.bandParams[i].gain )
            conf.set_int( currCfgKey + '/type', params.bandParams[i].bandType )
            conf.set_float( currCfgKey + '/loudnesMaxGain', params.bandParams[i].maxGain )
            conf.set_float( currCfgKey + '/maxVolumePercentage', params.bandParams[i].maxVolumePercentage)
            conf.set_float( currCfgKey + '/minVolumePercentage', params.bandParams[i].minVolumePercentage)
            conf.set_bool( currCfgKey + '/loudnesEnabled', params.bandParams[i].loudnesEnabled)

    @staticmethod
    def load():
        conf = GConf.Client.get_default()
        numPresets = conf.get_int( EQUALIZER_GCONF_PREFIX + '/num_presets')
        print( "numPresets : ", numPresets )
        presets = Presets()
        print( "numPresets before loop: ", presets.getNumPresets() )
        actPreset = conf.get_string( EQUALIZER_GCONF_PREFIX + '/current_preset' )
        for i in range(0, numPresets):
            currPreset = conf.get_string( EQUALIZER_GCONF_PREFIX + '/preset' + str(i) )
            newPreset = Config.loadPreset( currPreset )
            isActivePreset = currPreset == actPreset
            print( currPreset, " is active : ", isActivePreset )
            presets.appendPreset( newPreset, isActivePreset )
            print("loop index : ", i)
        print( "numPresets after loop: ", presets.getNumPresets() )
        return presets

    @staticmethod
    def save(presets):
        print ("saving presets")
        conf = GConf.Client.get_default()
        numPresets = presets.getNumPresets()
        print("numPresets : ", numPresets)
        conf.set_int( EQUALIZER_GCONF_PREFIX + '/num_presets', numPresets)
        for i in range(0, numPresets):
            currCfgKey = EQUALIZER_GCONF_PREFIX + '/preset' + str(i)
            preset = presets[i]
            conf.set_string(currCfgKey, preset.presetName )
            Config.saveParams(preset)
        conf.set_string( EQUALIZER_GCONF_PREFIX + '/current_preset', presets.getActivePreset().presetName )