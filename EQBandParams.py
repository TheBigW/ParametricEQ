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
	
