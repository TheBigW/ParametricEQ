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

class EQBandParams:
    EQBANDTYPES = ['Peak', 'Low shelf', 'High shelf']
    @staticmethod
    def get_string_from_band_type( bandType ):
        print( EQBandParams.EQBANDTYPES )
        return EQBandParams.EQBANDTYPES[bandType]
    def __init__(self, freq, width, gain, bandType = 0):
        self.frequency = freq
        self.bandwidth = width
        self.gain = gain
        self.bandType = bandType
    def __lt__(self, other):
         return self.frequency < other.frequency

class Preset:
    def __init__(self, name, params):
        self.presetName = name
        self.bandParams = params
    def getNumBands(self):
        return len(self.bandParams)
    def sort(self):
        self.bandParams.sort()
    presetName = ""
    bandParams = []

class LoudnesParams:
    def getEQBand(self, volume):
        #calculate eqBand gain
        print("self.maxVolumePercentage ", self.maxVolumePercentage)
        print("self.minVolumePercentage ", self.minVolumePercentage)
        minVolFact = (float(self.minVolumePercentage)/100)
        maxVolFact = (float(self.maxVolumePercentage)/100)
        calculatedGainFactor = (1.0 / (maxVolFact - minVolFact) ) * (volume-minVolFact)
        print("calculatedGainFactor : ", calculatedGainFactor)
        calculatedGain = (self.maxGain - (calculatedGainFactor * self.maxGain))
        self.eqBand.gain = max( min( calculatedGain, 12.0), 0 )
        print("loudnessGain:",self.eqBand.gain)
        return self.eqBand
    def loudnessEnabled(self):
        return self.maxGain != 0
    eqBand = EQBandParams(0,0,0)
    maxGain = 0.0
    maxVolumePercentage = 1.0
    minVolumePercentage = 0.0

class Presets:
    def __init__(self):
        self.presets = []
        self.activePresetIndex = -1
        self.loudnesParams=LoudnesParams()
    def appendPreset(self, preset, makeAtive):
        self.presets.append( preset )
        if True == makeAtive:
            self.activePresetIndex=self.getNumPresets()-1
            print("activePresetIndex : ", self.activePresetIndex)
        print("number of presets : ", self.getNumPresets() )
    def getActivePreset(self) :
        return self.presets[self.activePresetIndex]
    def getNumPresets(self) :
        return len( self.presets )
    def __getitem__(self,index):
        return self.presets[index]
    activePresetIndex = -1
    presets = []
    loudnesParams=LoudnesParams()
