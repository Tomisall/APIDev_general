function scripts { set-location "C:\Users\USER\Documents\script" }
function bus { Start-Process "https://www.oxfordbus.co.uk/stops/3400030036" }
function busstop { python "C:\Users\USER\Documents\script\busstop.py" }
function bs { 
	clear
	busstop
}
New-Alias choco 'C:\ProgramData\chocoportable\choco.exe'
New-Alias vim 'C:\tools\vim\vim90\vim.exe'
New-Alias edge Start-Process
New-Alias pandoc 'C:\Users\USER\AppData\Local\Pandoc\pandoc.exe'
New-Alias fzf  'C:\ProgramData\chocolatey\lib\fzf\tools\fzf.exe'
New-Alias word "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
function open() {
	$param1=$args[0] 
	
	if ($args[0] -eq $null)
	{
		ii $(fzf)
	}

	else
	{
	ii $(fzf --query "$param1")
	} 
}
