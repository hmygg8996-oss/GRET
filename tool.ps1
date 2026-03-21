$Host.UI.RawUI.WindowTitle = "roxi Tool - by roxi"
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "White"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Clear-Host

function Show-Menu {
    Clear-Host
    $width = $Host.UI.RawUI.WindowSize.Width

    Write-Host ""

    $stars = ".       *       .         *        .            .         *      ."
    $pad = [math]::Max(0, [math]::Floor(($width - $stars.Length) / 2))
    Write-Host (" " * $pad + $stars) -ForegroundColor White

    Write-Host ""

    $logo = @(
        ' _______                       __          __                          __ ',
        '|       \                     |  \        |  \                        |  \',
        '| $$$$$$$\  ______   __    __  \$$       _| $$_     ______    ______  | $$',
        '| $$__| $$ /      \ |  \  /  \|  \      |   $$ \   /      \  /      \ | $$',
        '| $$    $$|  $$$$$$\ \$$\/  $$| $$       \$$$$$$  |  $$$$$$\|  $$$$$$\| $$',
        '| $$$$$$$\| $$  | $$  >$$  $$ | $$        | $$ __ | $$  | $$| $$  | $$| $$',
        '| $$  | $$| $$__/ $$ /  $$$$\ | $$        | $$|  \| $$__/ $$| $$__/ $$| $$',
        '| $$  | $$ \$$    $$|  $$ \$$\| $$         \$$  $$ \$$    $$ \$$    $$| $$',
        ' \$$   \$$  \$$$$$$  \$$   \$$ \$$          \$$$$   \$$$$$$   \$$$$$$  \$$'
    )
    foreach ($line in $logo) {
        $p = [math]::Max(0, [math]::Floor(($width - $line.Length) / 2))
        Write-Host (" " * $p + $line) -ForegroundColor White
    }

    Write-Host ""
    Write-Host (" " * $pad + $stars) -ForegroundColor White
    Write-Host ""

    $c = @("White","White","White","White","White","White","White","White","White")

    Write-Host "  ( MALWARE Build          )  ( Scam                   )  ( Panel and Tools        )  ( NETWORK                )" -ForegroundColor White
    Write-Host ""

    Write-Host "  " -NoNewline; Write-Host "[01] Discord Token Tool  " -NoNewline -ForegroundColor $c[0]; Write-Host "  " -NoNewline; Write-Host "[10] Self Bot             " -NoNewline -ForegroundColor $c[0]; Write-Host "  " -NoNewline; Write-Host "[19] 1                    " -NoNewline -ForegroundColor $c[0]; Write-Host "  " -NoNewline; Write-Host "[28] 1                    " -ForegroundColor $c[0]
    Write-Host "  " -NoNewline; Write-Host "[02] Ip Generator        " -NoNewline -ForegroundColor $c[1]; Write-Host "  " -NoNewline; Write-Host "[11] Infection Builder    " -NoNewline -ForegroundColor $c[1]; Write-Host "  " -NoNewline; Write-Host "[20] 1                    " -NoNewline -ForegroundColor $c[1]; Write-Host "  " -NoNewline; Write-Host "[29] 1                    " -ForegroundColor $c[1]
    Write-Host "  " -NoNewline; Write-Host "[03] Webhook Spammer     " -NoNewline -ForegroundColor $c[2]; Write-Host "  " -NoNewline; Write-Host "[12] Local IP Changer     " -NoNewline -ForegroundColor $c[2]; Write-Host "  " -NoNewline; Write-Host "[21] 1                    " -NoNewline -ForegroundColor $c[2]; Write-Host "  " -NoNewline; Write-Host "[30] 1                    " -ForegroundColor $c[2]
    Write-Host "  " -NoNewline; Write-Host "[04] Channel Nuker       " -NoNewline -ForegroundColor $c[3]; Write-Host "  " -NoNewline; Write-Host "[13] MAC Changer          " -NoNewline -ForegroundColor $c[3]; Write-Host "  " -NoNewline; Write-Host "[22] 1                    " -NoNewline -ForegroundColor $c[3]; Write-Host "  " -NoNewline; Write-Host "[31] 1                    " -ForegroundColor $c[3]
    Write-Host "  " -NoNewline; Write-Host "[05] TempMail            " -NoNewline -ForegroundColor $c[4]; Write-Host "  " -NoNewline; Write-Host "[14] 1                    " -NoNewline -ForegroundColor $c[4]; Write-Host "  " -NoNewline; Write-Host "[23] 1                    " -NoNewline -ForegroundColor $c[4]; Write-Host "  " -NoNewline; Write-Host "[32] 1                    " -ForegroundColor $c[4]
    Write-Host "  " -NoNewline; Write-Host "[06] HWID Change         " -NoNewline -ForegroundColor $c[5]; Write-Host "  " -NoNewline; Write-Host "[15] 1                    " -NoNewline -ForegroundColor $c[5]; Write-Host "  " -NoNewline; Write-Host "[24] 1                    " -NoNewline -ForegroundColor $c[5]; Write-Host "  " -NoNewline; Write-Host "[33] 1                    " -ForegroundColor $c[5]
    Write-Host "  " -NoNewline; Write-Host "[07] IP Changer          " -NoNewline -ForegroundColor $c[6]; Write-Host "  " -NoNewline; Write-Host "[16] 1                    " -NoNewline -ForegroundColor $c[6]; Write-Host "  " -NoNewline; Write-Host "[25] 1                    " -NoNewline -ForegroundColor $c[6]; Write-Host "  " -NoNewline; Write-Host "[34] 1                    " -ForegroundColor $c[6]
    Write-Host "  " -NoNewline; Write-Host "[08] exe-to-image        " -NoNewline -ForegroundColor $c[7]; Write-Host "  " -NoNewline; Write-Host "[17] 1                    " -NoNewline -ForegroundColor $c[7]; Write-Host "  " -NoNewline; Write-Host "[26] 1                    " -NoNewline -ForegroundColor $c[7]; Write-Host "  " -NoNewline; Write-Host "[35] 1                    " -ForegroundColor $c[7]
    Write-Host "  " -NoNewline; Write-Host "[09] Killing VPN/proxy   " -NoNewline -ForegroundColor $c[8]; Write-Host "  " -NoNewline; Write-Host "[18] 1                    " -NoNewline -ForegroundColor $c[8]; Write-Host "  " -NoNewline; Write-Host "[27] 1                    " -NoNewline -ForegroundColor $c[8]; Write-Host "  " -NoNewline; Write-Host "[36] 1                    " -ForegroundColor $c[8]

    Write-Host ""
    Write-Host "  [00] Exit" -ForegroundColor White
    Write-Host ""
    Write-Host "  ---->" -NoNewline -ForegroundColor White
    Write-Host " " -NoNewline
}

while ($true) {
    Show-Menu
    $choice = Read-Host

    switch ($choice) {
        "1"  { Clear-Host; python "$ScriptDir\1.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "01" { Clear-Host; python "$ScriptDir\1.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "2"  { Clear-Host; python "$ScriptDir\2.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "02" { Clear-Host; python "$ScriptDir\2.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "3"  { Clear-Host; python "$ScriptDir\3.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "03" { Clear-Host; python "$ScriptDir\3.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "4"  { Clear-Host; python "$ScriptDir\4.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "04" { Clear-Host; python "$ScriptDir\4.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "5"  { Clear-Host; python "$ScriptDir\5.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "05" { Clear-Host; python "$ScriptDir\5.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "6"  { Clear-Host; python "$ScriptDir\6.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "06" { Clear-Host; python "$ScriptDir\6.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "7"  { Clear-Host; python "$ScriptDir\7.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "07" { Clear-Host; python "$ScriptDir\7.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "8"  { Clear-Host; python "$ScriptDir\8.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "08" { Clear-Host; python "$ScriptDir\8.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "9"  { Clear-Host; python "$ScriptDir\9.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "09" { Clear-Host; python "$ScriptDir\9.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "10" { Clear-Host; python "$ScriptDir\10.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "11" { Clear-Host; python "$ScriptDir\11.PY"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "12" { Clear-Host; python "$ScriptDir\12.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        "13" { Clear-Host; python "$ScriptDir\13.py"; Write-Host "Press any key..." -ForegroundColor White; $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") }
        default {
            if ($choice -eq "0" -or $choice -eq "00") {
                Clear-Host
                Write-Host "Thanks for using Roxtool!" -ForegroundColor White
                Start-Sleep -Seconds 2
                exit
            } elseif ($choice -match "^\d+$" -and [int]$choice -ge 1 -and [int]$choice -le 36) {
                Clear-Host
                Write-Host "Coming soon..." -ForegroundColor White
                Start-Sleep -Seconds 2
            } else {
                Write-Host "Invalid choice!" -ForegroundColor White
                Start-Sleep -Seconds 2
            }
        }
    }
}