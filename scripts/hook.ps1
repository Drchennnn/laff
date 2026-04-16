# laff hook — inject into $PROFILE with:
#   . "e:\laff\scripts\hook.ps1"

$LaffPort = 9876  # must match config.yaml port

function Send-LaffEvent {
    param(
        [string]$EventType,
        [string]$Command,
        [int]$ExitCode
    )
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $connected = $client.ConnectAsync('127.0.0.1', $LaffPort).Wait(200)
        if ($connected -and $client.Connected) {
            # Build JSON manually to avoid ConvertTo-Json overhead/BOM
            $cmd = $Command -replace '\\', '\\' -replace '"', '\"'
            $payload = "{`"event`":`"$EventType`",`"command`":`"$cmd`",`"exit_code`":$ExitCode}`n"
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
            $stream = $client.GetStream()
            $stream.Write($bytes, 0, $bytes.Length)
            $stream.Flush()
        }
        $client.Close()
    } catch {
        # Never break the terminal — silently ignore all errors
    }
}

# Preserve any existing prompt function
$script:LaffOriginalPrompt = if (Test-Path Function:\prompt) { $function:prompt } else { $null }

function global:prompt {
    # Capture exit state FIRST — any other code will overwrite $? and $LASTEXITCODE
    $lastSuccess = $?
    $lastExit    = $LASTEXITCODE

    # Determine event type
    $eventType = if ($null -ne $lastExit -and $lastExit -ne 0) {
        'failure'
    } elseif (-not $lastSuccess) {
        'failure'
    } else {
        'success'
    }

    # Only send if there was an actual command (not just an empty Enter)
    $lastCmd = (Get-History -Count 1).CommandLine
    if ($lastCmd) {
        $exitCode = if ($null -ne $lastExit) { $lastExit } else { 0 }
        Send-LaffEvent -EventType $eventType -Command $lastCmd -ExitCode $exitCode
    }

    # Delegate to original prompt or use default
    if ($script:LaffOriginalPrompt) {
        & $script:LaffOriginalPrompt
    } else {
        "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) "
    }
}
