function scripts { set-location "C:\Users\Evo1264\Documents\script" }
function bus { Start-Process "https://www.oxfordbus.co.uk/stops/3400030036" }
function busstop { python "C:\Users\Evo1264\Documents\script\busstop.py" }
function bs { 
	clear
	busstop
}
New-Alias choco 'C:\ProgramData\chocoportable\choco.exe'
New-Alias vim 'C:\tools\vim\vim90\vim.exe'
New-Alias edge Start-Process
New-Alias pandoc 'C:\Users\EVO1264\AppData\Local\Pandoc\pandoc.exe'
