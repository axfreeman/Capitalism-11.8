foreach ($file in Get-ChildItem *.json) {
    Write-Output $file.name
    Get-Content $file | Set-Content -Encoding utf8 ("$file.name" +".sql")
 }