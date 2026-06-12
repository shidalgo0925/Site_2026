# Copia la captura del portal Easy NodeOne (calendario) a easynodeone-dashboard.png
$ErrorActionPreference = 'Stop'
$dest = Join-Path $PSScriptRoot 'easynodeone-dashboard.png'
$root = Join-Path $env:USERPROFILE '.cursor\projects'
if (-not (Test-Path $root)) {
  Write-Host "No se encontro la carpeta de proyectos de Cursor."
  exit 1
}
$patterns = @('*image-19c03bd5*.png', '*image-40d97f15*.png', '*image-8e11da96*.png')
$src = $null
foreach ($p in $patterns) {
  $cand = Get-ChildItem $root -Recurse -File -Filter $p -ErrorAction SilentlyContinue |
    Where-Object { Test-Path -LiteralPath $_.FullName } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  if ($cand) { $src = $cand; break }
}
if (-not $src) {
  Write-Host "No se encontro ninguna captura reciente. Guarda tu PNG como:"
  Write-Host $dest
  exit 1
}
Copy-Item -LiteralPath $src.FullName -Destination $dest -Force
Write-Host "Listo: $dest ($((Get-Item -LiteralPath $dest).Length) bytes)"
