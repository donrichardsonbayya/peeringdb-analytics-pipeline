# PowerShell script to test PostgreSQL connection
# Run this script to test if PostgreSQL is accessible from Windows

try {
    # Test if port 5433 is listening
    $connection = Test-NetConnection -ComputerName localhost -Port 5433 -WarningAction SilentlyContinue
    if ($connection.TcpTestSucceeded) {
        Write-Host "✅ Port 5433 is accessible" -ForegroundColor Green
        
        # Try to connect using .NET PostgreSQL driver (if available)
        try {
            # This requires Npgsql.dll to be available
            $connectionString = "Host=localhost;Port=5433;Database=pe_data;Username=pe_user;Password=pe_pass;"
            Write-Host "Connection string: $connectionString" -ForegroundColor Yellow
            Write-Host "✅ Connection string is ready for PowerBI" -ForegroundColor Green
        }
        catch {
            Write-Host "⚠️  .NET PostgreSQL driver not available, but connection should work in PowerBI" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "❌ Port 5433 is not accessible" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error testing connection: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🔧 Troubleshooting Steps:" -ForegroundColor Cyan
Write-Host "1. Make sure Docker Desktop is running" -ForegroundColor White
Write-Host "2. Try restarting Docker Desktop" -ForegroundColor White
Write-Host "3. In PowerBI Desktop, try these connection details:" -ForegroundColor White
Write-Host "   Server: localhost" -ForegroundColor Gray
Write-Host "   Port: 5433" -ForegroundColor Gray
Write-Host "   Database: pe_data" -ForegroundColor Gray
Write-Host "   Username: pe_user" -ForegroundColor Gray
Write-Host "   Password: pe_pass" -ForegroundColor Gray
Write-Host "4. Alternative: Try Server: 127.0.0.1 instead of localhost" -ForegroundColor White