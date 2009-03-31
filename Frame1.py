#Boa:Frame:Frame1

import wx, evotankclasses, pickle, os
from evotankclasses import robot
def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1AMMO, wxID_FRAME1AMMOTHRESHOLD, 
 wxID_FRAME1ARMORTHRESHOLD, wxID_FRAME1BOTFILE, wxID_FRAME1BOTNAME, 
 wxID_FRAME1CHOICE10, wxID_FRAME1CHOICE11, wxID_FRAME1CHOICE12, 
 wxID_FRAME1CHOICE13, wxID_FRAME1CHOICE6, wxID_FRAME1CHOICE7, 
 wxID_FRAME1CHOICE8, wxID_FRAME1CHOICE9, wxID_FRAME1CURRENTSTATE, 
 wxID_FRAME1FUELTHRESHOLD, wxID_FRAME1LOADBUTTON, wxID_FRAME1MINDISTTHRESHOLD, 
 wxID_FRAME1SAVEBUTTON, wxID_FRAME1STATICBOX1, wxID_FRAME1STATICBOX2, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT6, 
] = [wx.NewId() for _init_ctrls in range(27)]

class Frame1(wx.Frame):
    states = ['search', 'getarmor', 'getfuel', 'getammo', 'kill']
    stspinners = ['armorthreshold', 'fuelthreshold', 'ammothreshold', 'mindistthreshold']
    stthresholds = ['minarmor', 'minfuel', 'minammo', 'mindist']
    tankbot = robot()

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.menu1 = wx.Menu(title=u'File')

        self.menuFile = wx.MenuBar()
        self.menuFile.SetTitle(u'File')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(256, 131), size=wx.Size(684, 470),
              style=wx.DEFAULT_FRAME_STYLE,
              title=u'Tankbot Operational Core Programmer')
        self._init_utils()
        self.SetClientSize(wx.Size(684, 470))

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Name:', name='staticText1', parent=self, pos=wx.Point(88,
              40), size=wx.Size(31, 12), style=0)

        self.botname = wx.TextCtrl(id=wxID_FRAME1BOTNAME, name=u'botname',
              parent=self, pos=wx.Point(136, 40), size=wx.Size(80, 20), style=0,
              value=u'')
        self.botname.Bind(wx.EVT_TEXT_ENTER, self.OnBotnameTextEnter,
              id=wxID_FRAME1BOTNAME)
        self.botname.Bind(wx.EVT_TEXT, self.OnBotnameText,
              id=wxID_FRAME1BOTNAME)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label=u'State Thresholds', name='staticBox1', parent=self,
              pos=wx.Point(96, 80), size=wx.Size(200, 328), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Armor', name='staticText2', parent=self, pos=wx.Point(112,
              104), size=wx.Size(29, 12), style=0)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Fuel', name='staticText3', parent=self, pos=wx.Point(112,
              128), size=wx.Size(29, 12), style=0)

        self.Ammo = wx.StaticText(id=wxID_FRAME1AMMO, label=u'Ammo',
              name=u'Ammo', parent=self, pos=wx.Point(112, 152),
              size=wx.Size(32, 12), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Target Distance', name='staticText4', parent=self,
              pos=wx.Point(112, 176), size=wx.Size(76, 12), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_FRAME1STATICBOX2,
              label=u'State Code', name='staticBox2', parent=self,
              pos=wx.Point(344, 96), size=wx.Size(200, 312), style=0)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'For State', name='staticText5', parent=self,
              pos=wx.Point(360, 120), size=wx.Size(46, 12), style=0)

        self.currentstate = wx.Choice(choices=['Search Drone', 'Low Armor',
              'Low Fuel', 'Low ammo', 'In Target Dist'],
              id=wxID_FRAME1CURRENTSTATE, name=u'currentstate', parent=self,
              pos=wx.Point(416, 120), size=wx.Size(120, 24), style=0)
        self.currentstate.Bind(wx.EVT_CHOICE, self.OnCurrentstateChoice,
              id=wxID_FRAME1CURRENTSTATE)

        self.choice6 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'], id=wxID_FRAME1CHOICE6,
              name='choice6', parent=self, pos=wx.Point(416, 152),
              size=wx.Size(120, 24), style=0)
        self.choice6.Bind(wx.EVT_CHOICE, self.OnChoice6Choice,
              id=wxID_FRAME1CHOICE6)

        self.choice7 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'], id=wxID_FRAME1CHOICE7,
              name='choice7', parent=self, pos=wx.Point(416, 176),
              size=wx.Size(120, 24), style=0)
        self.choice7.Bind(wx.EVT_CHOICE, self.OnChoice7Choice,
              id=wxID_FRAME1CHOICE7)

        self.choice8 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'], id=wxID_FRAME1CHOICE8,
              name='choice8', parent=self, pos=wx.Point(416, 200),
              size=wx.Size(120, 24), style=0)
        self.choice8.Bind(wx.EVT_CHOICE, self.OnChoice8Choice,
              id=wxID_FRAME1CHOICE8)

        self.choice9 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'], id=wxID_FRAME1CHOICE9,
              name='choice9', parent=self, pos=wx.Point(416, 224),
              size=wx.Size(120, 24), style=0)
        self.choice9.Bind(wx.EVT_CHOICE, self.OnChoice9Choice,
              id=wxID_FRAME1CHOICE9)

        self.choice10 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE10, name='choice10', parent=self,
              pos=wx.Point(416, 248), size=wx.Size(120, 24), style=0)
        self.choice10.Bind(wx.EVT_CHOICE, self.OnChoice10Choice,
              id=wxID_FRAME1CHOICE10)

        self.choice11 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE11, name='choice11', parent=self,
              pos=wx.Point(416, 272), size=wx.Size(120, 24), style=0)
        self.choice11.Bind(wx.EVT_CHOICE, self.OnChoice11Choice,
              id=wxID_FRAME1CHOICE11)

        self.choice12 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE12, name='choice12', parent=self,
              pos=wx.Point(416, 296), size=wx.Size(120, 24), style=0)
        self.choice12.Bind(wx.EVT_CHOICE, self.OnChoice12Choice,
              id=wxID_FRAME1CHOICE12)

        self.choice13 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Target', 'Face Fuel', 'Face Armor', 
              'Face Ammo', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE13, name='choice13', parent=self,
              pos=wx.Point(416, 320), size=wx.Size(120, 24), style=0)
        self.choice13.Bind(wx.EVT_CHOICE, self.OnChoice13Choice,
              id=wxID_FRAME1CHOICE13)

        self.armorthreshold = wx.SpinCtrl(id=wxID_FRAME1ARMORTHRESHOLD,
              initial=0, max=100, min=0, name=u'armorthreshold', parent=self,
              pos=wx.Point(224, 104), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)
        self.armorthreshold.Bind(wx.EVT_SPIN_DOWN,
              self.OnArmorthresholdSpinDown, id=wxID_FRAME1ARMORTHRESHOLD)
        self.armorthreshold.Bind(wx.EVT_SPIN_UP, self.OnArmorthresholdSpinUp,
              id=wxID_FRAME1ARMORTHRESHOLD)
        self.armorthreshold.Bind(wx.EVT_SPIN, self.OnArmorthresholdSpin,
              id=wxID_FRAME1ARMORTHRESHOLD)
        self.armorthreshold.Bind(wx.EVT_SPINCTRL, self.OnArmorthresholdSpinctrl,
              id=wxID_FRAME1ARMORTHRESHOLD)

        self.fuelthreshold = wx.SpinCtrl(id=wxID_FRAME1FUELTHRESHOLD, initial=0,
              max=5000, min=0, name=u'fuelthreshold', parent=self,
              pos=wx.Point(224, 128), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)
        self.fuelthreshold.Bind(wx.EVT_SPIN_DOWN, self.OnFuelthresholdSpinDown,
              id=wxID_FRAME1FUELTHRESHOLD)
        self.fuelthreshold.Bind(wx.EVT_SPIN_UP, self.OnFuelthresholdSpinUp,
              id=wxID_FRAME1FUELTHRESHOLD)
        self.fuelthreshold.Bind(wx.EVT_SPIN, self.OnFuelthresholdSpin,
              id=wxID_FRAME1FUELTHRESHOLD)
        self.fuelthreshold.Bind(wx.EVT_SPINCTRL, self.OnFuelthresholdSpinctrl,
              id=wxID_FRAME1FUELTHRESHOLD)

        self.ammothreshold = wx.SpinCtrl(id=wxID_FRAME1AMMOTHRESHOLD, initial=0,
              max=100, min=0, name=u'ammothreshold', parent=self,
              pos=wx.Point(224, 152), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)
        self.ammothreshold.Bind(wx.EVT_SPIN_DOWN, self.OnAmmothresholdSpinDown,
              id=wxID_FRAME1AMMOTHRESHOLD)
        self.ammothreshold.Bind(wx.EVT_SPIN_UP, self.OnAmmothresholdSpinUp,
              id=wxID_FRAME1AMMOTHRESHOLD)
        self.ammothreshold.Bind(wx.EVT_SPIN, self.OnAmmothresholdSpin,
              id=wxID_FRAME1AMMOTHRESHOLD)
        self.ammothreshold.Bind(wx.EVT_SPINCTRL, self.OnAmmothresholdSpinctrl,
              id=wxID_FRAME1AMMOTHRESHOLD)

        self.mindistthreshold = wx.SpinCtrl(id=wxID_FRAME1MINDISTTHRESHOLD,
              initial=0, max=100, min=0, name=u'mindistthreshold', parent=self,
              pos=wx.Point(224, 176), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)
        self.mindistthreshold.Bind(wx.EVT_SPIN_DOWN,
              self.OnMindistthresholdSpinDown, id=wxID_FRAME1MINDISTTHRESHOLD)
        self.mindistthreshold.Bind(wx.EVT_SPIN_UP,
              self.OnMindistthresholdSpinUp, id=wxID_FRAME1MINDISTTHRESHOLD)
        self.mindistthreshold.Bind(wx.EVT_SPIN, self.OnMindistthresholdSpin,
              id=wxID_FRAME1MINDISTTHRESHOLD)
        self.mindistthreshold.Bind(wx.EVT_SPINCTRL,
              self.OnMindistthresholdSpinctrl, id=wxID_FRAME1MINDISTTHRESHOLD)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'Tankbot File:', name='staticText6', parent=self,
              pos=wx.Point(104, 424), size=wx.Size(61, 12), style=0)

        self.botfile = wx.TextCtrl(id=wxID_FRAME1BOTFILE, name=u'botfile',
              parent=self, pos=wx.Point(176, 416), size=wx.Size(128, 20),
              style=0, value=u'')

        self.loadbutton = wx.Button(id=wxID_FRAME1LOADBUTTON, label=u'Load',
              name=u'loadbutton', parent=self, pos=wx.Point(328, 416),
              size=wx.Size(85, 22), style=0)
        self.loadbutton.Bind(wx.EVT_BUTTON, self.OnLoadbuttonButton,
              id=wxID_FRAME1LOADBUTTON)

        self.savebutton = wx.Button(id=wxID_FRAME1SAVEBUTTON, label=u'Save',
              name=u'savebutton', parent=self, pos=wx.Point(424, 416),
              size=wx.Size(85, 22), style=0)
        self.savebutton.Bind(wx.EVT_BUTTON, self.OnSavebuttonButton,
              id=wxID_FRAME1SAVEBUTTON)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnLoadbuttonButton(self, event):
        try:
            f = open('savedbots/' + self.botfile.GetValue(), 'r')
            self.tankbot = pickle.load(f)
            self.botname.SetValue(self.tankbot.name)
            self.armorthreshold.SetValue(self.tankbot.minarmor)
            self.fuelthreshold.SetValue(self.tankbot.minfuel)
            self.ammothreshold.SetValue(self.tankbot.minammo)
            self.mindistthreshold.SetValue(self.tankbot.mindist)
            for i in range(8):
                exec('self.choice' + str(i + 6) + '.SetSelection(self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[' + str(i) + '])')
        finally:    
            event.Skip()

    def OnSavebuttonButton(self, event):
        try:
            filename = 'savedbots/' + self.botfile.GetValue()
            if os.path.exists(filename):
                filename = filename + '.new'                
            f = open(filename, 'w')
            pickle.dump(self.tankbot, f)
            f.close
        finally:
            event.Skip()

    def OnCurrentstateChoice(self, event):
        try:
            for i in range(8):
                exec('self.choice' + str(i + 6) + '.SetSelection(self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[' + str(i) + '])')

        finally:
            event.Skip()

    def OnArmorthresholdSpinDown(self, event):
        try:
            self.tankbot.minarmor -= 1
        finally:
            event.Skip()

    def OnArmorthresholdSpinUp(self, event):
        try:
            self.tankbot.minarmor += 1
        finally:
            event.Skip()

    def OnFuelthresholdSpinDown(self, event):
        try:
            self.tankbot.minfuel -= 1
        finally:
            event.Skip()

    def OnFuelthresholdSpinUp(self, event):
        try:
            self.tankbot.minfuel += 1
        finally:
            event.Skip()

    def OnAmmothresholdSpinDown(self, event):
        try:
            self.tankbot.minammo -= 1
        finally:
            event.Skip()

    def OnAmmothresholdSpinUp(self, event):
        try:
            self.tankbot.minammo += 1
        finally:
            event.Skip()

    def OnMindistthresholdSpinDown(self, event):
        try:
            self.tankbot.mindist -= 1
        finally:
            event.Skip()

    def OnMindistthresholdSpinUp(self, event):
        try:
            self.tankbot.mindist += 1
        finally:
            event.Skip()

    def OnBotnameTextEnter(self, event):
        try:
            self.tankbot.name = self.botname.GetValue()
        finally:
            event.Skip()

    def OnChoice6Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[0] = self.choice6.GetSelection()')
        finally:
            event.Skip()

    def OnChoice7Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[1] = self.choice7.GetSelection()')
        finally:
            event.Skip()

    def OnChoice8Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[2] = self.choice8.GetSelection()')
        finally:
            event.Skip()

    def OnChoice9Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[3] = self.choice9.GetSelection()')
        finally:
            event.Skip()

    def OnChoice10Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[4] = self.choice10.GetSelection()')
        finally:
            event.Skip()

    def OnChoice11Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[5] = self.choice11.GetSelection()')
        finally:
            event.Skip()

    def OnChoice12Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[6] = self.choice12.GetSelection()')
        finally:
            event.Skip()

    def OnChoice13Choice(self, event):
        try:
            exec('self.tankbot.' + self.states[self.currentstate.GetSelection()] + '[7] = self.choice13.GetSelection()')
        finally:
            event.Skip()

    def OnBotnameText(self, event):
        try:
            self.tankbot.name = self.botname.GetValue()
        finally:
            event.Skip()

    def OnArmorthresholdSpin(self, event):
        try:
            self.tankbot.minammo = self.armorthreshold.GetValue()
        finally:
            event.Skip()

    def OnFuelthresholdSpin(self, event):
        try:
            self.tankbot.minfuel = self.fuelthreshold.GetValue()
        finally:
            event.Skip()

    def OnAmmothresholdSpin(self, event):
        try:
            self.tankbot.minammo = self.ammothreshold.GetValue()
        finally:
            event.Skip()

    def OnMindistthresholdSpin(self, event):
        try:
            self.tankbot.mindist = self.mindistthreshold.GetValue()
        finally:
            event.Skip()

    def OnArmorthresholdSpinctrl(self, event):
        try:
            self.tankbot.minarmor = self.armorthreshold.GetValue()
        finally:
            event.Skip()

    def OnFuelthresholdSpinctrl(self, event):
        try:
            self.tankbot.minfuel = self.fuelthreshold.GetValue()
        finally:
            event.Skip()

    def OnAmmothresholdSpinctrl(self, event):
        try:
            self.tankbot.minammo = self.ammothreshold.GetValue()
        finally:
            event.Skip()

    def OnMindistthresholdSpinctrl(self, event):
        try:
            self.tankbot.mindist = self.mindistthreshold.GetValue()
        finally:
            event.Skip()
