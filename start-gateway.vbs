Set ws = CreateObject("WScript.Shell")
ws.CurrentDirectory = "C:\Users\leon\AppData\Local\hermes"
ws.Run "cmd /c C:\Users\leon\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes gateway run", 0, False
