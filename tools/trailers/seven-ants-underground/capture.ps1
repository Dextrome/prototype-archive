param(
    [string]$SourceProject = 'E:/Oreil/OreilChaos',
    [string]$ProductionRoot = 'E:/trailer-production/seven-ants',
    [string]$Godot = 'E:/Godot/Godot_v4.6.1-stable_mono_win64_console.exe'
)
$ErrorActionPreference = 'Stop'
$sourceFull = [IO.Path]::GetFullPath($SourceProject).TrimEnd('\')
$productionFull = [IO.Path]::GetFullPath($ProductionRoot).TrimEnd('\')
if ($productionFull.StartsWith($sourceFull, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The production copy must be outside the source game project.'
}
$captureProject = Join-Path $productionFull 'game'
New-Item -ItemType Directory -Path $captureProject -Force | Out-Null
& robocopy $sourceFull $captureProject /E /XD .git .godot .claude .codex tmp_reference /NFL /NDL /NJH /NJS /NP
if ($LASTEXITCODE -gt 7) { throw 'Project copy failed.' }
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'CaptureDirector.cs') -Destination $captureProject
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Capture.tscn') -Destination $captureProject
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'SessionManager.Capture.cs') -Destination (Join-Path $captureProject 'autoloads')
$projectConfig = Join-Path $captureProject 'project.godot'
(Get-Content -Raw -LiteralPath $projectConfig).Replace('config/name="OreilChaos"','config/name="SevenAntsTrailerCapture"') | Set-Content -LiteralPath $projectConfig
$sessionFile = Join-Path $captureProject 'scripts/game/GameSession.cs'
(Get-Content -Raw -LiteralPath $sessionFile).Replace('Time.GetTicksMsec()', '(Engine.GetProcessFrames() * 1000UL / 60UL)') | Set-Content -LiteralPath $sessionFile
Push-Location $captureProject
try {
    & dotnet build OreilChaos.csproj -v:q
    if ($LASTEXITCODE -ne 0) { throw 'Capture project build failed.' }
    & $Godot --headless --path $captureProject --editor --import --quit *> (Join-Path $productionFull 'import.log')
    if ($LASTEXITCODE -ne 0) { throw 'Godot import failed.' }
    $shots = @('clamp','breach','spring','bounce','echo','panic','rocket','chaos','rope0','rope2')
    foreach ($shotName in $shots) {
        $sceneShot = $shotName
        $variant = 0
        if ($shotName -like 'rope*') { $sceneShot = 'rope'; $variant = [int]$shotName.Substring(4) }
        Write-Host "Rendering $shotName"
        & $Godot --path $captureProject --rendering-method gl_compatibility --position 4000,2000 --resolution 1600x900 --fixed-fps 60 --write-movie (Join-Path $productionFull "$shotName.avi") res://Capture.tscn -- "shot=$sceneShot" "variant=$variant" "out=$productionFull" *> (Join-Path $productionFull "$shotName.log")
        if ($LASTEXITCODE -ne 0) { throw "Capture failed: $shotName" }
    }
} finally { Pop-Location }
