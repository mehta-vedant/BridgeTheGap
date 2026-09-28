<#
.SYNOPSIS
    Initialize the hackathon project repository at official kickoff.

.DESCRIPTION
    This folder is the hackathon project folder. It is deliberately NOT a git
    repository before the official start of the event, so that the submission
    history begins at kickoff and contains no prior work.

    This script performs the kickoff. It initializes the repository and sets
    the default branch, but it does NOT create a commit unless you explicitly
    pass -Commit. That default is deliberate: a commit made before the
    official start would contaminate the submission history.

    Run this once, after the official problem statement is in hand.

.PARAMETER Commit
    Actually create the first commit. Without this switch the script only
    initializes the repository and reports what would be committed.

.PARAMETER Message
    Commit message to use with -Commit. Ignored otherwise.

.PARAMETER OnlyProduct
    Stage only product paths, leaving the pre-seeded toolkit files
    (AGENTS.md, .agents/, docs/, scripts/, .gitignore, .gitattributes)
    untracked, so the submission history shows product work only.

.EXAMPLE
    .\scripts\kickoff.ps1
    # initialize only, commit nothing

.EXAMPLE
    .\scripts\kickoff.ps1 -Commit -Message "chore: initialize project workspace"

.EXAMPLE
    .\scripts\kickoff.ps1 -Commit -OnlyProduct -Message "feat: initial project structure"
#>

[CmdletBinding()]
param(
    [switch]$Commit,
    [string]$Message = 'chore: initialize project workspace',
    [switch]$OnlyProduct
)

# NOTE ON ERROR HANDLING
# $ErrorActionPreference is deliberately 'Continue', not 'Stop'.
# This script shells out to git, and git writes ordinary warnings to stderr
# (for example the "CRLF will be replaced by LF" notice produced by
# .gitattributes on Windows). With 'Stop', PowerShell escalates a native
# command's stderr into a terminating error, so a harmless warning would
# abort the kickoff. Failure detection here is explicit instead: every git
# call is followed by an $LASTEXITCODE check and a Write-Error with an
# explicit exit code.
$ErrorActionPreference = 'Continue'

$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot

try {
    # --- Refuse to clobber an existing repository -------------------------
    if (Test-Path '.git') {
        Write-Error "A .git directory already exists in $projectRoot."
        Write-Host "This script is for kickoff only. Use normal git commands." -ForegroundColor Yellow
        exit 1
    }

    Write-Host "Project root: $projectRoot" -ForegroundColor DarkGray
    Write-Host ""

    # --- Initialize the repository ----------------------------------------
    & git init -q
    if ($LASTEXITCODE -ne 0) { Write-Error "git init failed."; exit 1 }
    & git branch -M main
    if ($LASTEXITCODE -ne 0) { Write-Error "could not set branch to main."; exit 1 }
    Write-Host "Initialized git repository on branch 'main'." -ForegroundColor Green

    # --- Report what is present -------------------------------------------
    $all = @(& git ls-files --others --exclude-standard)
    $toolkit = @('.agents', 'AGENTS.md', 'HANDOFF.md', 'docs', 'scripts',
                 '.gitignore', '.gitattributes', '.env.example')

    $product = @($all | Where-Object {
            $top = ($_ -split '/')[0]
            $toolkit -notcontains $top
        })

    Write-Host ""
    Write-Host "Files detected: $($all.Count) total" -ForegroundColor Cyan
    Write-Host "  product paths : $($product.Count)"
    Write-Host "  toolkit paths : $($all.Count - $product.Count)"

    if ($OnlyProduct) {
        if ($product.Count -eq 0) {
            Write-Error "-OnlyProduct was requested but no product paths were found."
            exit 1
        }
        # Capture stderr rather than letting it print inline. A warning such
        # as the .gitattributes CRLF notice is expected and harmless; it is
        # only shown if the command actually fails.
        $gitErr = & git add -- $product 2>&1
        if ($LASTEXITCODE -ne 0) { Write-Error "git add failed: $gitErr"; exit 1 }
        Write-Host ""
        Write-Host "Staged product paths only:" -ForegroundColor Cyan
        $product | ForEach-Object { "  $_" }
    }
    else {
        $gitErr = & git add -A 2>&1
        if ($LASTEXITCODE -ne 0) { Write-Error "git add failed: $gitErr"; exit 1 }
        Write-Host ""
        Write-Host "Staged everything (-OnlyProduct not used)." -ForegroundColor Cyan
    }

    # --- Commit only when explicitly asked ---------------------------------
    if (-not $Commit) {
        Write-Host ""
        Write-Host "NO COMMIT CREATED." -ForegroundColor Yellow
        Write-Host "That is the safe default. Review the staged list, then run:"
        Write-Host "  .\scripts\kickoff.ps1 -Commit -Message `"$Message`""
        Write-Host ""
        Write-Host "Only commit once the official hackathon has started." -ForegroundColor Yellow
        exit 0
    }

    $count = [int]((& git rev-list --all --count) -replace '\D', '')
    if ($count -ne 0) {
        Write-Error "Expected an empty history, found $count commits. Aborting."
        exit 1
    }

    $gitErr = & git commit -q -m $Message 2>&1
    if ($LASTEXITCODE -ne 0) { Write-Error "git commit failed: $gitErr"; exit 1 }
    $sha = (& git rev-parse --short HEAD)
    Write-Host ""
    Write-Host "Created first commit: $sha  $Message" -ForegroundColor Green
    Write-Host ""
    Write-Host "History now begins at the official start of the event." -ForegroundColor Cyan
}
finally {
    Pop-Location
}
