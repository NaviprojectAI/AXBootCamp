# Pretendard 폰트 자동 설치 스크립트 (Windows)
# 사용법: powershell -ExecutionPolicy Bypass -File scripts/install-fonts.ps1

$FontName = "Pretendard"
$FontUrl = "https://github.com/orioncactus/pretendard/releases/download/v1.3.9/Pretendard-1.3.9.zip"
$TempDir = "$env:TEMP\pretendard-install"
$FontDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"

# 이미 설치되어 있는지 확인
$installed = Get-ChildItem "$FontDir\Pretendard*" -ErrorAction SilentlyContinue
if ($installed.Count -gt 0) {
    Write-Host "Pretendard 폰트가 이미 설치되어 있습니다." -ForegroundColor Green
    exit 0
}

Write-Host "Pretendard 폰트를 다운로드합니다..." -ForegroundColor Cyan

# 다운로드
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
$ZipPath = "$TempDir\pretendard.zip"
Invoke-WebRequest -Uri $FontUrl -OutFile $ZipPath

# 압축 해제
Write-Host "압축을 해제합니다..." -ForegroundColor Cyan
Expand-Archive -Path $ZipPath -DestinationPath $TempDir -Force

# OTF 폰트 설치 (사용자 폰트 디렉토리)
$otfFiles = Get-ChildItem "$TempDir" -Recurse -Filter "*.otf" | Where-Object { $_.Name -match "Pretendard-" -and $_.Name -notmatch "Variable" }
if ($otfFiles.Count -eq 0) {
    $otfFiles = Get-ChildItem "$TempDir" -Recurse -Filter "*.ttf" | Where-Object { $_.Name -match "Pretendard-" -and $_.Name -notmatch "Variable" }
}

New-Item -ItemType Directory -Force -Path $FontDir | Out-Null

foreach ($font in $otfFiles) {
    Copy-Item $font.FullName -Destination "$FontDir\$($font.Name)" -Force
    # 레지스트리에 폰트 등록
    $regPath = "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    $fontTitle = $font.BaseName + " (TrueType)"
    New-ItemProperty -Path $regPath -Name $fontTitle -Value "$FontDir\$($font.Name)" -PropertyType String -Force | Out-Null
    Write-Host "  설치: $($font.Name)" -ForegroundColor Gray
}

# 정리
Remove-Item -Recurse -Force $TempDir

Write-Host "`nPretendard 폰트 $($otfFiles.Count)개 파일 설치 완료!" -ForegroundColor Green
Write-Host "참고: 일부 프로그램에서는 재시작이 필요할 수 있습니다." -ForegroundColor Yellow
