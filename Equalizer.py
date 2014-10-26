# MyEqualizer.py
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

from gi.repository import Gtk
from config import Config
from EQBandParams import EQBandParams, Preset, LoudnesParams
#import os, sys, inspect

class LabeledEdit:
    def __init__(self, box, text, value):
        label = Gtk.Label( text )
        box.add(label)
        self.entry = Gtk.Entry()
        self.entry.set_text( value )
        box.add( self.entry )

class AddDialog(Gtk.Dialog):
    params = EQBandParams(0,0,0)
    def __init__(self, parent):
        super(Gtk.Dialog, self).__init__()
        okBtn = self.add_button(Gtk.STOCK_OK,Gtk.ResponseType.OK)
        okBtn.connect( "clicked", self.on_ok )
        self.set_default_size(150, 100)
        box = self.get_content_area()
        self.bandWidthLE = LabeledEdit( box, "Bandwidth", "10" );
        self.freqLE = LabeledEdit( box, "frequency", "100" );
        self.gainLE = LabeledEdit( box, "Gain", "0" );
        name_store = Gtk.ListStore(int, str)
        name_store.append([ 0, EQBandParams.get_string_from_band_type(0)] )
        name_store.append([ 1, EQBandParams.get_string_from_band_type(1)] )
        name_store.append([ 2, EQBandParams.get_string_from_band_type(2)] )
        self.comboType = Gtk.ComboBox.new_with_model_and_entry(name_store)
        self.comboType.set_entry_text_column(1)
        self.comboType.set_active(0)
        box.add(self.comboType)
        self.show_all()
    def on_ok(self, param):
        self.params.gain = int(self.gainLE.entry.get_text())
        self.params.frequency = int(self.freqLE.entry.get_text())
        self.params.bandwidth = int(self.bandWidthLE.entry.get_text())
        self.params.bandType = self.comboType.get_active()

class LoudnessDialog(Gtk.Dialog):
    params = LoudnesParams()
    def __init__(self, parent):
        super(Gtk.Dialog, self).__init__()
        okBtn = self.add_button(Gtk.STOCK_OK,Gtk.ResponseType.OK)
        okBtn.connect( "clicked", self.on_ok )
        self.set_default_size(150, 100)
        box = self.get_content_area()
        loudnesParams = Config.LoadLoudnesParams()
        self.bandWidthLE = LabeledEdit( box, "Bandwidth", str(int(loudnesParams.eqBand.bandwidth)) )
        self.freqLE = LabeledEdit( box, "frequency", str(int(loudnesParams.eqBand.frequency)) )
        self.maxGainLE = LabeledEdit( box, "max gain", str(loudnesParams.maxGain) )
        self.minVolumePercentageLE = LabeledEdit( box, "max dB volume percentage", str(loudnesParams.minVolumePercentage) );
        self.maxVolumePercentageLE = LabeledEdit( box, "0dB volume percentage", str(loudnesParams.maxVolumePercentage) );
        name_store = Gtk.ListStore(int, str)
        name_store.append([ 0, EQBandParams.get_string_from_band_type(0)] )
        name_store.append([ 1, EQBandParams.get_string_from_band_type(1)] )
        name_store.append([ 2, EQBandParams.get_string_from_band_type(2)] )
        self.comboType = Gtk.ComboBox.new_with_model_and_entry(name_store)
        self.comboType.set_entry_text_column(1)
        self.comboType.set_active(loudnesParams.eqBand.bandType)
        box.add(self.comboType)
        self.show_all()
    def on_ok(self, param):
        self.params.maxGain = float(self.maxGainLE.entry.get_text())
        self.params.eqBand.frequency = float(self.freqLE.entry.get_text())
        self.params.eqBand.bandwidth = float(self.bandWidthLE.entry.get_text())
        self.params.eqBand.bandType = self.comboType.get_active()
        self.params.minVolumePercentage = float(self.minVolumePercentageLE.entry.get_text() )
        self.params.maxVolumePercentage = float(self.maxVolumePercentageLE.entry.get_text() )

class EQGroupControl(Gtk.VBox):
    def __init__(self, params, parent):
        super(Gtk.VBox, self).__init__(False)
        self.params = EQBandParams( params.frequency, params.bandwidth, params.gain, params.bandType )
        self.parent = parent
        adjustment = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
        slider = Gtk.VScale()
        slider.set_range( -24, 12 )
        slider.set_inverted(True)
        slider.set_value_pos( Gtk.PositionType.TOP )
        slider.set_value(self.params.gain)
        slider.set_size_request( 100, 300 )
        slider.connect( "value_changed", self.slider_changed )
        labelFreq = Gtk.Label( "f=" + str(self.params.frequency) + "Hz" )
        labelBw = Gtk.Label( "w=" + str(self.params.bandwidth) + "Hz" )
        labelType = Gtk.Label( EQBandParams.get_string_from_band_type(self.params.bandType) )
        self.add(slider)
        self.add(labelFreq);
        self.add(labelBw);
        self.add(labelType)
        remBtn = Gtk.Button( "Remove" )
        remBtn.connect( "clicked", self.on_remove_band )
        self.add(remBtn)
        self.show_all()
    def slider_changed(self, hscale):
        print("hscale : ", hscale)
        self.params.gain = hscale.get_value();
        print('slider changed for ' + str(self.params.frequency) + ' Hz to ' + str(self.params.gain))
        self.parent.gain_changed()
    def on_remove_band(self, param):
        self.parent.on_remove_band(self)

class EQControl(Gtk.Dialog):
    def update_from_preset(self, preset):
        numEqBands = preset.getNumBands()
        print("numEqBands : ", numEqBands)
        self.set_default_size( numEqBands * 100, 350)
        self.rebuild_eq_controls(preset.bandParams)
    def loadPresets(self):
        presetStore = self.comboPresets.get_model()
        presetStore.clear()
        loadedPresets = Config.load()
        num_presets = loadedPresets.getNumPresets()
        for i in range(0, num_presets):
            currPreset = loadedPresets[i]
            presetStore.append([ i, currPreset.presetName ] )
            print("adding preset : ", currPreset.presetName, currPreset )
        self.comboPresets.set_entry_text_column(1)
        currPresetIndex = loadedPresets.activePresetIndex
        print("preset index : ", currPresetIndex)
        self.comboPresets.set_active(currPresetIndex)
        self.update_from_preset( loadedPresets.getActivePreset() )
    def __init__(self, eq):
        super(Gtk.Dialog, self).__init__()
        self.volume = 1.0
        self.set_deletable(False)
        self.eq = eq
        self.connect( "delete-event", self.on_destroy )
        self.set_title( "N Bands parametric EQ" )
        closeBtn = self.add_button(Gtk.STOCK_CLOSE,Gtk.ResponseType.CLOSE)
        closeBtn.connect( "clicked", self.on_close )
        buttonBox = Gtk.HBox(False)
        addBtn = Gtk.Button( "Add band" )
        addBtn.connect( "clicked", self.add_new_eq_band )
        buttonBox.add(addBtn);
        applyBtn = Gtk.Button( "Save" )
        applyBtn.connect( "clicked", self.on_apply_settings )
        buttonBox.add(applyBtn)
        loudnessButton=Gtk.Button( "Loudness" )
        loudnessButton.connect( "clicked", self.on_config_loudness )
        buttonBox.add(loudnessButton)
        #combo box for presets
        self.newHBox = None
        self.comboPresets = Gtk.ComboBox.new_with_model_and_entry( Gtk.ListStore(int, str) )
        self.comboPresets.connect( "changed", self.onPresetChanged )
        buttonBox.add( Gtk.Label( "preset : " ) )
        buttonBox.add(self.comboPresets)
        #add a link button to the github for documentation
        linkButton = Gtk.LinkButton("https://github.com/TheBigW/ParametricEQ/blob/master/README.md", label="HowTo")
        buttonBox.add(linkButton)
        self.vbox.add(buttonBox)
        self.loadPresets()
    def onPresetChanged(self, comboPresets):
        tree_iter = comboPresets.get_active_iter()
        if tree_iter != None:
            model = comboPresets.get_model()
            row_id, preset = model[tree_iter][:2]
            print("Selected: id=%d, preset=%s" % (row_id, preset))
            presets = Config.load()
            presets.activePresetIndex = row_id
            Config.save(presets)
            self.update_from_preset(presets.getActivePreset())
    def rebuild_eq_controls(self, params):
        numEqBands = len(params)
        if self.newHBox != None:
            self.vbox.remove(self.newHBox)
            self.newHBox.destroy()
        self.newHBox = Gtk.HBox(False)
        for i in range(0,numEqBands):
            self.newHBox.add(EQGroupControl( params[i], self ))
        self.vbox.add(self.newHBox)
        self.newHBox.show_all()
        self.eq.apply_settings(params)
    def onVolumeChanged(self,volume):
        self.volume = volume
        self.gain_changed()
    def on_destroy(self, widget, data):
        self.on_close(None)
        return True
    def gain_changed(self):
        params = self.getEqParamListFromUI()
        self.eq.apply_settings( params )
    def on_apply_settings(self, some_param):
        params = self.getEqParamListFromUI(True)
        self.eq.apply_settings( params )
        print("num params to save : ", len(params))
        tree_iter = self.comboPresets.get_active_iter()
        presetName = ""
        if tree_iter != None:
            model = self.comboPresets.get_model()
            row_id, name = model[tree_iter][:2]
            presetName=name
        else:
            entry = self.comboPresets.get_child()
            presetName=entry.get_text()
        print("curr preset: ",presetName)
        allPresets = Config.load()
        allPresets.appendPreset( Preset(presetName, params), True )
        Config.save( allPresets )
        self.loadPresets()
    def getEqParamListFromUI(self, ignoreLoudness = False):
        params = []
        eqBandctrls = self.newHBox.get_children()
        print("children : ", len(eqBandctrls))
        numBands = len(eqBandctrls)
        for i in range(0,numBands):
            params.append( eqBandctrls[i].params )
        loudnesParams = Config.LoadLoudnesParams()
        if True == loudnesParams.loudnessEnabled() and not ignoreLoudness :
            print("applying loudness")
            #add the loudness EQ channel and calculate gain first
            params.append( loudnesParams.getEQBand(self.volume) )
        print("num bands :", len(params) )
        return params
    def on_config_loudness(self, param):
        dlg = LoudnessDialog(self)
        if dlg.run() == Gtk.ResponseType.OK :
            #save params
            Config.SaveLoudnesParams(dlg.params)
            self.onVolumeChanged(self.volume)
        dlg.destroy()
    def add_new_eq_band(self, param):
        dlg = AddDialog(self)
        if dlg.run() == Gtk.ResponseType.OK :
            params=self.getEqParamListFromUI(True)
            params.append( dlg.params )
            numBands = len(params)
            for i in range(0,numBands):
                print("before sort : Param %f, %f" % (params[i].frequency, params[i].bandwidth))
            params.sort()#ascending order for frequency
            for i in range(0,numBands):
                print("Param %f, %f" % (params[i].frequency, params[i].bandwidth))
            self.rebuild_eq_controls(params)
        dlg.destroy()
    def on_remove_band(self,eqbandCtrl):
        params=self.getEqParamListFromUI(True)
        numParams = len(params)
        param = None
        for i in range(0,numParams):
            if eqbandCtrl.params.frequency == params[i].frequency:
                param = params[i]
                break
        params.remove(param)
        self.rebuild_eq_controls(params)
    def on_close(self, shell):
        print("closing ui")
        self.set_visible(False)
        return True
    def show_ui(self, *args):
        print("showing UI")
        self.show_all()
        self.present()
        print("done showing UI")
