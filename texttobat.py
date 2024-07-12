import wx
import os
import re
import zipfile

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        self.txtPath = wx.TextCtrl(panel, style=wx.TE_READONLY)
        btnOpen = wx.Button(panel, label="打开文件")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txtPath, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btnOpen, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.onOpenFile, btnOpen)

    def onOpenFile(self, event):
        wildcard = "Text files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open Text File", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            self.txtFilePath = dialog.GetPath()
            if self.txtFilePath.endswith(".txt"):
                self.txtPath.SetValue(self.txtFilePath)
                self.processFile()
                wx.MessageBox("文件处理完成", "提示", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("文件类型错误，请重新选择", "错误", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def sanitizeFileName(self, name):
        return re.sub(r'[\s,.!@#$%^&*()\-+=~`[\]{}|\\:;\'"<>?/]+', '_', name)

    def processFile(self):
        with open(self.txtFilePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        base_dir = os.path.dirname(self.txtFilePath)
        zip_file_path = os.path.join(base_dir, "处理后的文件.zip")

        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for line in lines:
                trimmedLine = line.strip()
                if trimmedLine:
                    match = re.search(r'00:\d{2}:\d{2}\.\d{3}\s+(.*)', trimmedLine)
                    if match:
                        fileNamePart = self.sanitizeFileName(match.group(1))
                        fileName = f"{fileNamePart}.bat"
                        content = trimmedLine
                        file_path = os.path.join(base_dir, fileName)
                        with open(file_path, 'w', encoding='utf-8') as outFile:
                            outFile.write(content)
                        zipf.write(file_path, fileName)
                        os.remove(file_path)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="文件处理器", size=(400, 200))
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()