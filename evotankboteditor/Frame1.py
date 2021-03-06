#Boa:Frame:Frame1

import wx, evotankclasses, pickle
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
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self._init_utils()
        self.SetClientSize(wx.Size(684, 470))

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Name:', name='staticText1', parent=self, pos=wx.Point(88,
              40), size=wx.Size(31, 12), style=0)

        self.botname = wx.TextCtrl(id=wxID_FRAME1BOTNAME, name=u'botname',
              parent=self, pos=wx.Point(136, 40), size=wx.Size(80, 20), style=0,
              value=u'')

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
              pos=wx.Point(416, 120), size=wx.Size(80, 24), style=0)

        self.choice6 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'], id=wxID_FRAME1CHOICE6,
              name='choice6', parent=self, pos=wx.Point(416, 152),
              size=wx.Size(80, 24), style=0)

        self.choice7 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'], id=wxID_FRAME1CHOICE7,
              name='choice7', parent=self, pos=wx.Point(416, 176),
              size=wx.Size(80, 24), style=0)

        self.choice8 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'], id=wxID_FRAME1CHOICE8,
              name='choice8', parent=self, pos=wx.Point(416, 200),
              size=wx.Size(80, 24), style=0)

        self.choice9 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'], id=wxID_FRAME1CHOICE9,
              name='choice9', parent=self, pos=wx.Point(416, 224),
              size=wx.Size(80, 24), style=0)

        self.choice10 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE10, name='choice10', parent=self,
              pos=wx.Point(416, 248), size=wx.Size(80, 24), style=0)

        self.choice11 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE11, name='choice11', parent=self,
              pos=wx.Point(416, 272), size=wx.Size(80, 24), style=0)

        self.choice12 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE12, name='choice12', parent=self,
              pos=wx.Point(416, 296), size=wx.Size(80, 24), style=0)

        self.choice13 = wx.Choice(choices=['NOP', 'Turn Right', 'Turn Left',
              'Throttle Up', 'Throttle Down', 'Face Armor', 'Face Fuel',
              'Face Ammo', 'Face Target', 'Fire Cannon'],
              id=wxID_FRAME1CHOICE13, name='choice13', parent=self,
              pos=wx.Point(416, 320), size=wx.Size(80, 24), style=0)

        self.armorthreshold = wx.SpinCtrl(id=wxID_FRAME1ARMORTHRESHOLD,
              initial=0, max=100, min=0, name=u'armorthreshold', parent=self,
              pos=wx.Point(224, 104), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)

        self.fuelthreshold = wx.SpinCtrl(id=wxID_FRAME1FUELTHRESHOLD, initial=0,
              max=5000, min=0, name=u'fuelthreshold', parent=self,
              pos=wx.Point(224, 128), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)

        self.ammothreshold = wx.SpinCtrl(id=wxID_FRAME1AMMOTHRESHOLD, initial=0,
              max=100, min=0, name=u'ammothreshold', parent=self,
              pos=wx.Point(224, 152), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)

        self.mindistthreshold = wx.SpinCtrl(id=wxID_FRAME1MINDISTTHRESHOLD,
              initial=0, max=100, min=0, name=u'mindistthreshold', parent=self,
              pos=wx.Point(224, 176), size=wx.Size(40, 16),
              style=wx.SP_ARROW_KEYS)

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
            f = open('savedbots/' + self.botfile.GetValue(), 'f')
            tankbot = pickle.load(f)
            self.botname.SetValue(tankbot.name)
        finally:    
            event.Skip()

    def OnSavebuttonButton(self, event):
        event.Skip()
