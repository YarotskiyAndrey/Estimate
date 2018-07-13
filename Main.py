import wx


class Form(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.works = [
            'Кладка стен (Газобетон до 100мм) м.кв/м.пог',
            'Кладка стен (Газобетон 100мм)(армированная) м.кв/м.пог',
            'Демонтаж стен (Толщина 100 мм) м.кв/м.пог',
            'Монтаж декоративных балок м.пог',
            'Штукатурка стены (откосы) п/маякам м.кв/м.пог',
            'Стяжка пола (до 50мм) черновая м.кв/м.пог',
            'Разводка электроточки (розетеки выключатели) точка',
            'Монтаж кабельканала м.пог',
            'Монтаж щитовой под автоматы (внутренний) до 24 автоматов шт'
        ]
        self.prices = [100, 120, 80, 100, 100, 95, 95, 40, 350]
        self.priceMap = dict(zip(self.works,self.prices))
        self.sumPrice = 0;
        self.createControls()
        self.bindEvents()
        self.doLayout()

    def createControls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.saveButton = wx.Button(self, label="Сохранить в файл")
        self.addButton = wx.Button(self, label="Добавить")
        self.worksLabel = wx.StaticText(self, label="Виды работы:")
        self.amountLabel = wx.StaticText(self, label="Кол-во")
        self.priceLabel = wx.StaticText(self, label="Цена:")
        self.amountValue = wx.TextCtrl(self, value="1")
        self.worksComboBox = wx.ComboBox(self, value=self.works[0], choices=self.works,
                                            style=wx.CB_DROPDOWN,)
        self.priceValue = wx.StaticText(self, label=str(int(self.amountValue.LabelText)*
                                           self.priceMap[self.worksComboBox.GetValue()]))

    def bindEvents(self):
        for control, event, handler in \
                [(self.saveButton, wx.EVT_BUTTON, self.onSave),
                 (self.addButton, wx.EVT_BUTTON, self.onAdd),
                 (self.amountValue, wx.EVT_TEXT, self.onValueChanged),
                 (self.worksComboBox, wx.EVT_COMBOBOX, self.onComboBoxChanged)]:
            control.Bind(event, handler)

    def doLayout(self):
        raise NotImplementedError

       
    def onComboBoxChanged(self, event):
        self.priceValue.SetLabelText(
            str(self.priceMap[self.worksComboBox.GetValue()]*int(self.amountValue.GetValue())))

    def onAdd(self,event):
        self.sumPrice += int(self.priceValue.GetLabelText())
        self.__log(self.worksComboBox.GetValue() + " " +
                   self.amountValue.GetValue() + " ед. " +
                   self.priceValue.GetLabelText() + " грн.")

    def onSave(self, event):
        file = open('output.txt', 'w')
        self.__log("Итого:" + str(self.sumPrice))

        file.write(self.logger.GetValue())
        self.logger.SetLabelText("")
        file.close()


    def onValueChanged(self, event):
        self.priceValue.SetLabelText(
            str(self.priceMap[self.worksComboBox.GetValue()] * int(self.amountValue.GetValue())))

 
    def __log(self, message):
        self.logger.AppendText('%s\n' % message)


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
