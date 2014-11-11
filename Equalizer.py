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
from ParametricEQconfig import Config
from EQBandParams import EQBandParams
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
        self.add( remBtn )
        self.show_all()
    def slider_changed(self, hscale):
        print("hscale : ", hscale)
        self.params.gain = hscale.get_value();
        print('slider changed for ' + str(self.params.frequency) + ' Hz to ' + str(self.params.gain))
        self.parent.gain_changed()
    def on_remove_band(self, param):
        self.parent.on_remove_band(self)

class EQControl(Gtk.Dialog):
    def update_from_preset(self,preset, cfg):
        self.params = cfg.load(preset)
        numEqBands = len(self.params)
        print("numEqBands : ", numEqBands)
        self.set_default_size( numEqBands * 100, 350)
        self.rebuild_eq_controls()
    def loadPresets(self):
        presetStore = self.comboPresets.get_model()        
        presetStore.clear()
        cfg = Config()
        presets = cfg.getAllPresets()    
        num_presets = len(presets)
        for i in range(0, num_presets):
            presetStore.append([ i, presets[i] ] )
            print("adding preset : ", presets[i])
        self.comboPresets.set_entry_text_column(1)
        currPreset = cfg.getCurrPreset()
        currPresetIndex = 0
        if num_presets > 0:
            currPresetIndex = presets.index( currPreset )    
        print("preset index : ", currPresetIndex)    
        self.comboPresets.set_active(currPresetIndex)
        self.update_from_preset( currPreset, cfg )
    def __init__(self, eq):
        super(Gtk.Dialog, self).__init__()
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
            cfg = Config()
            self.update_from_preset(preset, cfg)
    def rebuild_eq_controls(self):
        numEqBands = len(self.params)
        if self.newHBox != None:    
            self.vbox.remove(self.newHBox)    
            self.newHBox.destroy()
        self.newHBox = Gtk.HBox(False)
        for i in range(0,numEqBands):
            self.newHBox.add(EQGroupControl( self.params[i], self ))
        self.vbox.add(self.newHBox)
        self.newHBox.show_all()
        self.eq.apply_settings(self.params)
    def on_destroy(self, widget, data):
        self.on_close(None)
        return True
    def gain_changed(self):
        self.updateParamList()
        self.eq.apply_settings( self.params )
    def on_apply_settings(self, some_param):
        self.updateParamList()
        self.eq.apply_settings( self.params )
        print("num params to save : ", len(self.params))
        cfg = Config()
        tree_iter = self.comboPresets.get_active_iter()
        preset = ""        
        if tree_iter != None:
            model = self.comboPresets.get_model()
            row_id, name = model[tree_iter][:2]
            preset = name
        else:
            entry = self.comboPresets.get_child()
            preset = entry.get_text()
        #gconf does not allow spaces -> so we replace with _    
        preset = preset.replace( " ", "_" )
        print("curr preset: ", preset)
        cfg.save( self.params, preset )  
        self.loadPresets()
    def updateParamList(self):
        self.params = []
        eqBandctrls = self.newHBox.get_children()
        print("children : ", len(eqBandctrls))
        numBands = len(eqBandctrls)
        for i in range(0,numBands):
            self.params.append( eqBandctrls[i].params )
        print("num bands :", numBands)
    def add_new_eq_band(self, param):
        self.dlg = AddDialog(self)
        if self.dlg.run() == Gtk.ResponseType.OK : 
            self.updateParamList()        
            self.params.append( self.dlg.params )
            numBands = len(self.params)        
            for i in range(0,numBands):
                print("before sort : Param %f, %f" % (self.params[i].frequency, self.params[i].bandwidth))        
            self.params.sort()#ascending order for frequency
            for i in range(0,numBands):
                print("Param %f, %f" % (self.params[i].frequency, self.params[i].bandwidth))
            self.rebuild_eq_controls()
        self.dlg.destroy()
    def on_remove_band(self,eqbandCtrl):
        numParams = len(self.params)
        param = None
        for i in range(0,numParams):
            if eqbandCtrl.params.frequency == self.params[i].frequency:
                param = self.params[i]
                break    
        self.params.remove(param)
        self.rebuild_eq_controls()
    def on_close(self, shell):
        print("closing ui")
        self.set_visible(False)
        return True
    def show_ui(self, *args):
        print("showing UI")
        self.show_all()
        self.present()
        print("done showing UI")
