# ParametricEQ.py
# Copyright (C) 2013 - Tobias Wenig
#            tobiaswenig@yahoo.com>
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

import os, sys, inspect, subprocess, re
import threading
from gi.repository import GObject, Gst, Peas
from gi.repository import RB
from Equalizer import EQControl
from EQBandParams import EQBandParams, Preset, Presets
from config import Config

import ParametricEQ_rb3compat
from ParametricEQ_rb3compat import ActionGroup
from ParametricEQ_rb3compat import Action
from ParametricEQ_rb3compat import ApplicationShell

ui_string="""
<ui>
  <menubar name="MenuBar">
    <menu name="ControlMenu" action="Control">
      <placeholder name="PluginPlaceholder">
        <menuitem name="Parametric Equalizer" action="Equalize"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class ParametricEQPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(ParametricEQPlugin, self).__init__()
        print("init done")

    def set_filter(self):
        try:
            print('adding filter')
            self.player.add_filter(self.eq)
            print('done setting filter')
        except Exception as inst:
            print('unexpected exception',  sys.exc_info()[0], type(inst), inst)
            pass

    def do_deactivate(self):
        print('entering do_deactivate')
        try:
            self.player.remove_filter(self.eq)
            print('filter disabled')
            shell = self.object
            self._appshell.cleanup()
        except:
            pass
        del self.shell_player
        del self.shell
        del self.eq

    def apply_settings(self,params):
        numEQBands = len( params )
        #print("num-bands : ", numEQBands)
        if numEQBands > 0:
            #print("got eq bands")
            self.eq.set_property('num-bands', numEQBands)
            for i in range(0,numEQBands):
                band = self.eq.get_child_by_index(i)
                band.props.freq = params[i].frequency
                #print('band.props.freq', band.props.freq)
                band.props.bandwidth = params[i].bandwidth
                #print('band.props.bandwidth', band.props.bandwidth)
                band.props.gain = params[i].gain
                #print('band.props.gain', band.props.gain)
                band.props.type = params[i].bandType
                #print( inspect.getdoc( band.props.type ) )
                #print( "band.props.type", params[i].bandType )

    def show_ui(self, *args):
        self.eqDlg.show_ui(args)

    def add_ui(self, shell):
        print("starting add_ui")
        action_group = ActionGroup(shell, 'ParametricEqualizerActionGroup')
        action_group.add_action(func=self.show_ui,
            action_name='Equalize', label=_('_Equalizer'),
            action_type='app')
        self._appshell = ApplicationShell(shell)
        self._appshell.insert_action_group(action_group)
        self._appshell.add_app_menuitems(ui_string, 'ParametricEqualizerActionGroup')
        print("add_ui done")

    def volume_changed(self, sp, entry):
        print("volume changed")
        rbVolume = self.player.get_volume()
        mainVolume = float(self.mainVolumePercentage) / 100.0
        overallVolume = mainVolume * rbVolume
        self.eqDlg.onVolumeChanged( overallVolume )
        print( "volume:", overallVolume)

    mainVolumePercentage = 0

    @staticmethod
    def alsaVolumeCheckTimer( paramEQPluginInst ):
        threading.Timer(2.0, ParametricEQPlugin.alsaVolumeCheckTimer, [paramEQPluginInst]).start()
        #alsa get volume:
        #mainVolume = check_output(strParams )
        p = subprocess.Popen(["amixer", "sget", " Master"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pattern = re.compile('(\d*)%', re.MULTILINE)
        alsaVolume = int(pattern.findall( str(out) )[0])
        if paramEQPluginInst.mainVolumePercentage  != alsaVolume:
            paramEQPluginInst.mainVolumePercentage = alsaVolume
            print("main volume changed : ", alsaVolume)
            paramEQPluginInst.volume_changed(None, None)

    @staticmethod
    def pulseVolumeCheckTimer( paramEQPluginInst ):
        threading.Timer(2.0, ParametricEQPlugin.pulseVolumeCheckTimer, [paramEQPluginInst]).start()
        #alsa get volume:
        #mainVolume = check_output(strParams )
        p = subprocess.Popen(["pactl", "list", "sinks"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pattern = re.compile('Volume: 0:\s*(\d*)%', re.MULTILINE)
        strOutPut = str(out)
        #print( "pactl says: ", strOutPut )
        allVolumes = pattern.findall( strOutPut )
        print("all volumes : ", allVolumes)
        pulseVolume = int(allVolumes[1])
        if paramEQPluginInst.mainVolumePercentage != pulseVolume:
            paramEQPluginInst.mainVolumePercentage  = pulseVolume
            print("main volume changed : ", pulseVolume)
            paramEQPluginInst.volume_changed(None, None)


    def do_activate(self):
        self.shell = self.object
        print("is RB3 :" + str( ParametricEQ_rb3compat.is_rb3() ) + ", " + str(ParametricEQ_rb3compat.PYVER))
        self.shell_player = self.shell.props.shell_player
        self.player = self.shell_player.props.player
        self.eq = Gst.ElementFactory.make('equalizer-nbands', 'MyEQ')
        self.set_filter()
        currPresets = Config.load()
        if len(currPresets.presets) == 0:
            print("creating default preset")
            #no default config for active preset - create a 10 Band default EQ to get started
            defaultPreset = Preset( "default_10_band",
            [EQBandParams(29, 20, 0),
            EQBandParams(59, 30, 0),
            EQBandParams(119, 60, 0),
            EQBandParams(237, 118, 0),
            EQBandParams(474, 237, 0),
            EQBandParams(947, 473, 0),
            EQBandParams(1889, 942, 0),
            EQBandParams(3770, 1881, 0),
            EQBandParams(7523, 3753, 0),
            EQBandParams(15011, 7488, 0)]
            )
            currPresets.appendPreset(defaultPreset, True)
            Config.save( currPresets )
        self.eqDlg = EQControl(self)
        self.add_ui( self.shell )
        self.filterSet = False
        self.apply_settings(currPresets.getActivePreset().bandParams )
        #add volume changed callback
        self.psc_id = self.player.connect('volume-changed', self.volume_changed)
        ParametricEQPlugin.pulseVolumeCheckTimer(self)
        print("do_activate done")
