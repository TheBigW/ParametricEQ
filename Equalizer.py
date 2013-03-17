from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, Gst
from config import Config
from EQBandParams import EQBandParams

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
        self.show_all()
    def on_ok(self, param):
	self.params.gain = int(self.gainLE.entry.get_text())
	self.params.frequency = int(self.freqLE.entry.get_text())
	self.params.bandwidth = int(self.bandWidthLE.entry.get_text())
        
class EQGroupControl(Gtk.VBox):
    def __init__(self, params, parent):
	super(Gtk.VBox, self).__init__(False)       
	self.params = params
	self.parent = parent
        adjustment = Gtk.Adjustment(0, 0, 100, 5, 10, 0)
        slider = Gtk.VScale()
        slider.set_range( -24, 12 )
        #slider.set_update_policy( Gtk.UpdatePolicy.DISCONTINUOUS )
        slider.set_inverted(True)
        slider.set_value_pos( Gtk.PositionType.TOP )
        slider.set_value(self.params.gain)
        slider.set_size_request( 100, 300 )
        slider.connect( "value_changed", self.slider_changed )
        labelFreq = Gtk.Label( "f=" + str(self.params.frequency) + "Hz" )
        labelBw = Gtk.Label( "w=" + str(self.params.bandwidth) + "Hz" )
        self.add(slider)
        self.add(labelFreq);
        self.add(labelBw);
        remBtn = Gtk.Button( "Remove" )
	remBtn.connect( "clicked", self.on_remove_band )
        self.add( remBtn )
	self.show_all()
    def slider_changed(self, hscale):
        print "hscale : ", hscale
	self.params.gain = hscale.get_value();
        print 'slider changed for ' + str(self.params.frequency) + ' Hz to ' + str(self.params.gain)
	self.parent.gain_changed()
    def on_remove_band(self, param):
	self.parent.on_remove_band(self)
#TODO: as per eq: derive from object; make dialog a member
class EQControl(Gtk.Dialog):
    def __init__(self, eq, params):
	super(EQControl,self).__init__()
	self.eq = eq
	self.params = params
	self.set_title( "N Bands parametric EQ" )	
	closeBtn = self.add_button(Gtk.STOCK_CLOSE,Gtk.ResponseType.CLOSE)
	closeBtn.connect( "clicked", self.on_close )
        numEqBands = len(self.params)
	print "numEqBands : ", numEqBands        
	self.set_default_size( numEqBands * 100, 350)
        self.newHBox = Gtk.HBox(False);
        self.vbox.add(self.newHBox)
        addBtn = Gtk.Button( "Add EQ band" )
        addBtn.connect( "clicked", self.add_new_eq_band );
	self.vbox.add(addBtn);
	applyBtn = Gtk.Button( "Apply settings" )
        applyBtn.connect( "clicked", self.on_apply_settings );
        self.vbox.add(applyBtn);
        for i in range(0,numEqBands):
            self.newHBox.add(EQGroupControl( self.params[i], self ))
    def gain_changed(self):
	self.updateParamList()
	self.eq.apply_settings( self.params )
    def on_apply_settings(self, some_param):
	self.updateParamList()
	self.eq.apply_settings( self.params )
	print "num params to save : ", len(self.params)
	cfg = Config()
	cfg.save( self.params )
    def updateParamList(self):
	self.params = []
	eqBandctrls = self.newHBox.get_children()
	print "children : ", len(eqBandctrls)
	numBands = len(eqBandctrls)
	for i in range(0,numBands):
		self.params.append( eqBandctrls[i].params )
	print "num bands :", numBands
    def add_new_eq_band(self, param):
        self.dlg = AddDialog(self)
        if self.dlg.run() == Gtk.ResponseType.OK :
		self.newHBox.add( EQGroupControl( self.dlg.params, self ) )
	self.dlg.destroy()
	self.eq.apply_settings()
    def on_remove_band(self,eqbandCtrl):
	self.newHBox.remove( eqbandCtrl )
	self.eq.apply_settings()
    def on_close(self, shell):
	self.set_visible(False)
    def show_ui(self, shell, state):
        self.show_all()
        self.present()
    def add_ui(self, plugin, shell):
	action = Gtk.Action ('Equalize', 
			_('_Equalizer'), 
			_('N Band Equalizer'),
			plugin.find_file("MyEqualizer.svg"))
	action.connect ('activate', self.show_ui, shell)
	action_group = Gtk.ActionGroup ('EqualizerActionGroup')
	action_group.add_action (action)
        ui_manager = shell.props.ui_manager
        ui_manager.insert_action_group (action_group)
        ui_manager.add_ui_from_file(plugin.find_file("equalizer-ui.xml"))
