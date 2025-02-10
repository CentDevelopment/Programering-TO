# Rename Computer
Rename-Computer -NewName "SRV22-AD" -Force

# Install ADDS and DHCP roles
Install-WindowsFeature -Name AD-Domain-Services, DHCP -IncludeManagementTools

# Configure ADDS and Promote to Domain Controller
$DomainName = "nodo.local"
$SafeModePassword = ConvertTo-SecureString "Admin:123" -AsPlainText -Force
Install-ADDSForest -DomainName $DomainName -SafeModeAdministratorPassword $SafeModePassword -Force

# Restart after AD setup
Restart-Computer -Force

# Configure DHCP
$DHCPRange = "192.168.1.100 192.168.1.200"
$DNS = "192.168.1.1"
$Gateway = "192.168.1.1"

Add-DhcpServerV4Scope -Name "Nodo Scope" -StartRange 192.168.1.100 -EndRange 192.168.1.200 -SubnetMask 255.255.255.0
Set-DhcpServerV4OptionValue -OptionId 6 -Value $DNS
Set-DhcpServerV4OptionValue -OptionId 3 -Value $Gateway

# Enable Remote Desktop
Set-ItemProperty "HKLM:\System\CurrentControlSet\Control\Terminal Server\" -Name "fDenyTSConnections" -Value 0
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
