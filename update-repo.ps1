#!/usr/bin/env pwsh

# Add all changes
git add .

# Get commit message from user
$commitMessage = Read-Host -Prompt 'Enter your commit message'

# Commit changes
git commit -m $commitMessage

# Push to main branch
git push origin main

Write-Host "Updates pushed successfully!" -ForegroundColor Green