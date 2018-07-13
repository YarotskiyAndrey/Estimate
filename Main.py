import wx


class Form(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.works = []
        self.createControls()
        self.doLayout()

    def createControls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.saveButton = wx.Button(self, label="Сохранить в файл")
        self.addButton = wx.Button(self, label="Добавить")
        self.worksLabel = wx.StaticText(self, label="Виды работы:")
        self.amountLabel = wx.StaticText(self, label="Кол-во")
        self.priceLabel = wx.StaticText(self, label="Цена:")
        self.amountValue = wx.TextCtrl(self, value="1")
        self.worksComboBox = wx.ComboBox(self, choices=self.works,
                                            style=wx.CB_DROPDOWN,)
        self.priceValue = wx.StaticText(self, label="0")



    def doLayout(self):
        raise NotImplementedError


class FormWithSizer(Form):
    def doLayout(self):

        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        gridSizer = wx.FlexGridSizer(rows=4, cols=3, vgap=10, hgap=20)


        expandOption = dict(flag=wx.EXPAND)
        noOptions = dict()
        emptySpace = ((0, 0), noOptions)


        for control, options in \
                [(self.worksLabel, noOptions),
                 (self.amountLabel, noOptions),
                 (self.priceLabel, noOptions),
                 (self.worksComboBox, noOptions),
                 (self.amountValue, expandOption),
                 (self.priceValue, expandOption),
                 emptySpace,
                 (self.addButton, dict(flag=wx.ALIGN_LEFT)),
                 (self.saveButton, dict(flag=wx.ALIGN_CENTER))]:
            gridSizer.Add(control, **options)

        for control, options in \
                [(gridSizer, dict(border=5, flag=wx.ALL)),
                 (self.logger, dict(border=5, flag=wx.ALL | wx.EXPAND,
                                    proportion=1))]:
            boxSizer.Add(control, **options)

        self.SetSizerAndFit(boxSizer)


class FrameWithForms(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(FrameWithForms, self).__init__(*args, **kwargs)
        notebook = wx.Notebook(self)
        form = FormWithSizer(notebook)
        notebook.AddPage(form, 'File')
        self.SetClientSize(notebook.GetBestSize())


if __name__ == '__main__':
    app = wx.App(0)
    frame = FrameWithForms(None, title='Estimate')
    frame.Show()
    app.MainLoop()
