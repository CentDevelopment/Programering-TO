# Rename Computer
$UserName = "Bruker"
$ComputerName = "CLI10-DF"
Rename-Computer -NewName $ComputerName -Force

# Configure IP (No Gateway, Set DNS to 10.13.37.45)
$IP = "10.13.37.49"
$Subnet = "255.255.255.0"
$DNS = "10.13.37.45"

New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress $IP -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses $DNS

# Join domain
$Domain = "nodo.local"
$AdminUser = "$Domain\administrator"
$Password = ConvertTo-SecureString "Admin:123" -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($AdminUser, $Password)

Add-Computer -DomainName $Domain -Credential $Credential -Restart
