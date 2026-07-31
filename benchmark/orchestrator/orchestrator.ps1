# =============================================================================
# Phase 7 Orchestrator
# =============================================================================
# Schedules and executes the full Phase 7 benchmark matrix:
#   7 platforms x 4 scenarios x N replications = total runs
#
# For each run:
#   1. Pre-wake target platform (3-min warm-up to settle cold starts)
#   2. Start docker stats CSV collector on Linux VM (via SSH)
#   3. Launch k6 (CSV + JSON streaming output)
#   4. Wait for k6 to complete
#   5. Stop docker stats collector, fetch CSV
#   6. Parse k6 output via Python -> append master row
#   7. Inter-run cooldown
#
# Author: Chapk Rzgar Mohammed Abdalla
# Thesis: Benchmarking Traditional vs Serverless Web Platforms (Phase 7)
# =============================================================================

[CmdletBinding()]
param(
    [string]$Phase7Dir   = "$env:USERPROFILE\Desktop\thesis-phase7",
    [string]$ConfigDir   = "$env:USERPROFILE\Desktop\thesis-phase7\config",
    [string]$ScriptsDir  = "$env:USERPROFILE\Desktop\thesis-phase7\scripts",
    [string]$DataDir     = "$env:USERPROFILE\Desktop\thesis-phase7\data",
    [string]$LogsDir     = "$env:USERPROFILE\Desktop\thesis-phase7\logs",

    # Filter: only run specific platform(s) (comma-separated)
    # e.g., -PlatformFilter "03_django_gunicorn,06_flyio"
    [string]$PlatformFilter = "",

    # Filter: only run specific scenario(s) (comma-separated)
    # e.g., -ScenarioFilter "A_browse,D_burst"
    [string]$ScenarioFilter = "",

    # Number of replications per (platform, scenario) cell
    [int]$Replications = 8,

    # Override scenario duration (e.g., "5m" for pilot)
    [string]$DurationOverride = "",

    # Override target RPS (per scenario specific; set to skip)
    [string]$RpsOverride = "",

    # Cooldown seconds between runs (settle scale-down, recover sockets)
    [int]$CooldownSec = 60,

    # Pre-wake duration (warm cold-start serverless platforms)
    [int]$PreWakeSec = 180,

    # SSH user@host for Linux VM (for docker stats)
    [string]$LinuxVM = "azureuser@20.218.108.186",

    # Path to k6 binary
    [string]$K6 = "C:\Program Files\k6\k6.exe",

    # Path to Python
    [string]$Python = "python",

    # Resume mode: skip runs already in master_runs.csv
    [switch]$Resume,

    # Dry-run: print plan, do not execute
    [switch]$DryRun
)

# =============================================================================
# SETUP
# =============================================================================

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Ensure directories exist
foreach ($d in @($Phase7Dir, $DataDir, "$DataDir\raw", "$DataDir\docker_stats", $LogsDir)) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
}

$MasterCsv = Join-Path $DataDir "master_runs.csv"

# Load config
$Platforms = (Get-Content (Join-Path $ConfigDir "platforms.json") -Raw | ConvertFrom-Json).platforms
$Scenarios = (Get-Content (Join-Path $ConfigDir "scenarios.json") -Raw | ConvertFrom-Json).scenarios

# Apply filters
if ($PlatformFilter) {
    $allowed = $PlatformFilter -split ','
    $Platforms = $Platforms | Where-Object { $allowed -contains $_.id }
}
if ($ScenarioFilter) {
    $allowed = $ScenarioFilter -split ','
    $Scenarios = $Scenarios | Where-Object { $allowed -contains $_.id }
}

$ParserPy = Join-Path $ScriptsDir "parse_k6_output.py"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

function Write-Banner($msg, $color = "Magenta") {
    Write-Host ""
    Write-Host ("=" * 78) -ForegroundColor $color
    Write-Host "  $msg" -ForegroundColor $color
    Write-Host ("=" * 78) -ForegroundColor $color
}

function Get-Timestamp { (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffK") }

function Get-RunId($platformId, $scenarioId, $rep) {
    return "{0}__{1}__rep{2:D2}" -f $platformId, $scenarioId, $rep
}

function Test-RunComplete($runId) {
    # Check if this run_id is already in master_runs.csv
    if (-not (Test-Path $MasterCsv)) { return $false }
    $found = Import-Csv $MasterCsv | Where-Object { $_.run_id -eq $runId }
    return ($null -ne $found)
}

function Invoke-PreWake($platform) {
    # 3-minute pre-wake: hit /health/ every 10 seconds
    $url = "$($platform.url)/health/"
    $rounds = [math]::Ceiling($PreWakeSec / 10)
    Write-Host "  Pre-wake $url ($rounds rounds, $PreWakeSec sec)..." -NoNewline
    for ($i = 1; $i -le $rounds; $i++) {
        & curl.exe -sS -o NUL --max-time 30 $url 2>$null
        if ($i -lt $rounds) { Start-Sleep -Seconds 10 }
    }
    Write-Host " done" -ForegroundColor Green
}

function Start-DockerStats($outputName) {
    # Async-Job SSH with hard timeout (works around Windows OpenSSH "session held open by stderr" bug)
    # Strategy: start SSH in PowerShell background job, wait up to 20s for PID return, then force-kill the job.
    $vm = $script:LinuxVM
    if (-not $vm) { $vm = $LinuxVM }

    $job = Start-Job -ArgumentList $vm, $outputName -ScriptBlock {
        param($linuxVM, $name)
        # The remote command MUST close all file descriptors so SSH can disconnect
        $cmd = "cd ~/thesis-monitoring && (nohup bash docker_stats_collector.sh /tmp/$name 0 </dev/null >/tmp/$name.log 2>&1 &) ; sleep 0.5 ; pgrep -f 'docker_stats_collector.sh /tmp/$name' | head -1"
        & ssh -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 -o ServerAliveInterval=5 -o ServerAliveCountMax=2 $linuxVM $cmd 2>$null
    }

    # Wait at most 20 seconds for SSH to return
    $completed = Wait-Job -Job $job -Timeout 20
    if ($completed) {
        $output = Receive-Job -Job $job 2>$null
        Remove-Job -Job $job -Force 2>$null
        if ($output) { return ($output | Select-Object -Last 1).ToString().Trim() }
        return ""
    } else {
        # Timeout: kill the job
        Write-Host "    [WARN] SSH Start-DockerStats timeout (>20s), forcing job stop" -ForegroundColor Yellow
        Stop-Job -Job $job -Force 2>$null
        Remove-Job -Job $job -Force 2>$null
        return ""
    }
}

function Stop-DockerStats($remotePid, $outputName, $localPath) {
    $vm = $script:LinuxVM
    if (-not $vm) { $vm = $LinuxVM }

    # Async-Job SSH kill with timeout
    $killJob = Start-Job -ArgumentList $vm, $remotePid -ScriptBlock {
        param($linuxVM, $rpid)
        $cmd = "kill $rpid 2>/dev/null; sleep 1; pkill -f 'docker_stats_collector.sh /tmp/' 2>/dev/null; echo done"
        & ssh -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 $linuxVM $cmd 2>$null
    }
    Wait-Job -Job $killJob -Timeout 15 | Out-Null
    Receive-Job -Job $killJob 2>$null | Out-Null
    Remove-Job -Job $killJob -Force 2>$null

    # Async-Job scp fetch with timeout
    $scpJob = Start-Job -ArgumentList $vm, $outputName, $localPath -ScriptBlock {
        param($linuxVM, $name, $local)
        & scp -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 "${linuxVM}:/tmp/$name" $local 2>$null
    }
    Wait-Job -Job $scpJob -Timeout 30 | Out-Null
    Remove-Job -Job $scpJob -Force 2>$null

    # Async-Job cleanup with timeout
    $cleanJob = Start-Job -ArgumentList $vm, $outputName -ScriptBlock {
        param($linuxVM, $name)
        & ssh -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 $linuxVM "rm -f /tmp/$name /tmp/$name.log" 2>$null
    }
    Wait-Job -Job $cleanJob -Timeout 10 | Out-Null
    Remove-Job -Job $cleanJob -Force 2>$null
}

function Get-ScenarioScript($scenarioId) {
    switch -Regex ($scenarioId) {
        '^A_'    { return Join-Path $ScriptsDir "k6\scenario_A_browse.js" }
        '^B_'    { return Join-Path $ScriptsDir "k6\scenario_B_mixed.js" }
        '^C_'    { return Join-Path $ScriptsDir "k6\scenario_C_checkout.js" }
        '^D_'    { return Join-Path $ScriptsDir "k6\scenario_D_burst.js" }
        default  { throw "Unknown scenario: $scenarioId" }
    }
}

function Get-ScenarioDuration($scenario) {
    if ($DurationOverride) { return $DurationOverride }
    return "$($scenario.duration_min)m"
}

function Get-ScenarioRps($scenario) {
    if ($RpsOverride) { return $RpsOverride }
    if ($scenario.rps) { return $scenario.rps }
    return "10"  # Burst uses stages; rps not applicable
}

# =============================================================================
# MAIN LOOP
# =============================================================================

Write-Banner "PHASE 7 ORCHESTRATOR - START"
Write-Host "Platforms:        $($Platforms.Count)"
Write-Host "Scenarios:        $($Scenarios.Count)"
Write-Host "Replications:     $Replications"
Write-Host "Total runs:       $($Platforms.Count * $Scenarios.Count * $Replications)"
Write-Host "Phase 7 dir:      $Phase7Dir"
Write-Host "Master CSV:       $MasterCsv"
Write-Host "Pre-wake:         $PreWakeSec sec"
Write-Host "Cooldown:         $CooldownSec sec"
Write-Host "Linux VM (stats): $LinuxVM"
Write-Host "k6 binary:        $K6"
if ($DurationOverride) { Write-Host "Duration override: $DurationOverride" -ForegroundColor Yellow }
if ($RpsOverride)      { Write-Host "RPS override:      $RpsOverride" -ForegroundColor Yellow }
if ($Resume)           { Write-Host "Resume mode:       ON (skip completed)" -ForegroundColor Yellow }
if ($DryRun)           { Write-Host "DRY RUN:           ON (no execution)" -ForegroundColor Yellow }

# Build run plan
$plan = @()
foreach ($platform in $Platforms) {
    foreach ($scenario in $Scenarios) {
        for ($rep = 1; $rep -le $Replications; $rep++) {
            $runId = Get-RunId $platform.id $scenario.id $rep
            $plan += [PSCustomObject]@{
                run_id = $runId
                platform = $platform
                scenario = $scenario
                rep = $rep
            }
        }
    }
}

Write-Host ""
Write-Host "Total planned runs: $($plan.Count)"
if ($Resume) {
    $completed = $plan | Where-Object { Test-RunComplete $_.run_id }
    Write-Host "Already completed:  $($completed.Count)"
    $plan = $plan | Where-Object { -not (Test-RunComplete $_.run_id) }
    Write-Host "Remaining:          $($plan.Count)"
}

if ($DryRun) {
    Write-Banner "DRY RUN - Plan preview (first 10)" "Yellow"
    $plan | Select-Object -First 10 | Format-Table run_id -AutoSize
    Write-Host "...total $($plan.Count) runs would execute"
    return
}

# Execute plan
$runNumber = 0
$startedAt = Get-Date
foreach ($job in $plan) {
    $runNumber++
    $platform = $job.platform
    $scenario = $job.scenario
    $rep      = $job.rep
    $runId    = $job.run_id

    Write-Banner "RUN $runNumber/$($plan.Count): $runId" "Cyan"

    # Paths for this run
    $csvOut      = Join-Path $DataDir "raw\${runId}.csv"
    $jsonOut     = Join-Path $DataDir "raw\${runId}.json"
    $statsOut    = Join-Path $DataDir "docker_stats\${runId}__docker_stats.csv"
    $logFile     = Join-Path $LogsDir "${runId}.log"
    $statsRemote = "thesis_${runId}.csv"

    $scenarioScript = Get-ScenarioScript $scenario.id
    $duration       = Get-ScenarioDuration $scenario
    $rps            = Get-ScenarioRps $scenario

    # === Pre-wake ===
    Invoke-PreWake $platform

    # === Start docker stats (Linux VM only) ===
    $statsRemotePid = $null
    if ($platform.docker_container) {
        Write-Host "  Starting docker stats collector on $LinuxVM..."
        $statsRemotePid = Start-DockerStats $statsRemote
        Write-Host "    Remote PID: $statsRemotePid"
        Start-Sleep -Seconds 2  # Let collector warm up
    } else {
        Write-Host "  (No docker stats: platform is not on Linux VM)" -ForegroundColor DarkGray
    }

    # === Run k6 ===
    $startTs = Get-Timestamp
    Write-Host "  k6 START at $startTs"
    Write-Host "    Script:   $(Split-Path -Leaf $scenarioScript)"
    Write-Host "    Target:   $($platform.url)"
    Write-Host "    Duration: $duration"
    Write-Host "    RPS:      $rps"

    # k6 environment variables
    # Parse duration to minutes for D_burst stage scaling (e.g., "5m" -> 5, "30m" -> 30)
    $durationMin = 30
    if ($duration -match '^(\d+)m$') { $durationMin = [int]$matches[1] }
    elseif ($duration -match '^(\d+)s$') { $durationMin = [math]::Max(1, [math]::Round([int]$matches[1] / 60)) }

    $envArgs = @(
        "BASE_URL=$($platform.url)",
        "TARGET_RPS=$rps",
        "DURATION=$duration",
        "DURATION_MIN=$durationMin",
        "PLATFORM_ID=$($platform.id)",
        "REP=$rep"
    )

    $k6Args = @(
        "run",
        "--out", "csv=$csvOut",
        "--out", "json=$jsonOut",
        "--quiet",
        "--log-output", "file=$logFile",
        "--log-format", "raw"
    )
    foreach ($e in $envArgs) {
        $k6Args += "--env"
        $k6Args += $e
    }
    $k6Args += $scenarioScript

    # Launch k6 (foreground; orchestrator waits)
    # k6 logs go to log file via --log-output; capture summary only
    & $K6 $k6Args 2>&1 | Out-Null

    $k6Exit = $LASTEXITCODE
    $endTs = Get-Timestamp
    Write-Host "  k6 END   at $endTs  (exit=$k6Exit)"

    # === Stop docker stats and fetch CSV ===
    if ($statsRemotePid) {
        Write-Host "  Stopping docker stats, fetching CSV..."
        Stop-DockerStats $statsRemotePid $statsRemote $statsOut
        if (Test-Path $statsOut) {
            $rows = (Get-Content $statsOut | Measure-Object -Line).Lines
            Write-Host "    [OK] docker stats: $rows rows -> $statsOut" -ForegroundColor Green
        } else {
            Write-Host "    [WARN] docker stats CSV not retrieved" -ForegroundColor Yellow
        }
    }

    # === Parse k6 output -> master row ===
    Write-Host "  Parsing k6 output..."
    $parseArgs = @(
        $ParserPy,
        "--csv",       $csvOut,
        "--json",      $jsonOut,
        "--master",    $MasterCsv,
        "--platform",  $platform.id,
        "--scenario",  $scenario.id,
        "--rep",       $rep,
        "--start",     $startTs,
        "--end",       $endTs,
        "--target_rps", $rps
    )
    & $Python $parseArgs *>&1 | Tee-Object -FilePath $logFile -Append

    # === Cooldown ===
    if ($runNumber -lt $plan.Count) {
        Write-Host "  Cooldown ${CooldownSec}s..." -NoNewline
        Start-Sleep -Seconds $CooldownSec
        Write-Host " done"
    }

    # === Progress ETA ===
    $elapsed = (Get-Date) - $startedAt
    $perRun  = $elapsed.TotalSeconds / $runNumber
    $remain  = ($plan.Count - $runNumber) * $perRun
    $eta     = (Get-Date).AddSeconds($remain)
    Write-Host "  Progress: $runNumber/$($plan.Count) ($([math]::Round($runNumber/$plan.Count*100,1))%)  ETA: $($eta.ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor DarkCyan
}

Write-Banner "PHASE 7 ORCHESTRATOR - COMPLETE" "Green"
Write-Host "Total runs:       $($plan.Count)"
Write-Host "Master CSV:       $MasterCsv"
Write-Host "Raw data dir:     $DataDir\raw"
Write-Host "Docker stats dir: $DataDir\docker_stats"
Write-Host "Logs dir:         $LogsDir"
Write-Host "Total time:       $((Get-Date) - $startedAt)"
