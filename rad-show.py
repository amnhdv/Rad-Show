#!/usr/bin/env python3

import argparse
import subprocess

# A dictionary of DNS providers and their corresponding IP addresses
DNS_PROVIDERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'OpenDNS': ['208.67.222.222', '208.67.220.220'],
    'Cloudflare': ['1.1.1.1', '1.0.0.1'],
    'Quad9': ['9.9.9.9', '149.112.112.112'],
    'Shecan': ['178.22.122.100', '185.51.200.2'],
    'Begzar': ['185.55.225.25', '185.55.226.26'],
    '403': ['10.202.10.202', '10.202.10.102'],
    'Radar': ['10.202.10.10', '10.202.10.11'],
    'Electro': ['78.157.42.100', '78.157.42.101']
}

def set_dns(provider):
    # If the provider is "default", unset the DNS
    if provider == 'D':
        subprocess.run(["networksetup", "-setdnsservers", "Wi-Fi", "empty"])
        print(f"DNS set to default.")
        return
    # Otherwise, set the DNS to the chosen provider's IP addresses
    provider_options = [name for name in DNS_PROVIDERS.keys() if name.lower().startswith(provider.lower())]
    if len(provider_options) == 0:
        print(f"No provider starting with '{provider}' found.")
        return
    elif len(provider_options) > 1:
        print(f"Multiple provider options: {provider_options}. Please specify a more specific provider name.")
        return
    else:
        provider = provider_options[0]
        dns_addresses = DNS_PROVIDERS[provider]
        # Construct and execute the command to set the DNS
        dns_command = f"networksetup -setdnsservers Wi-Fi {' '.join(dns_addresses)}"
        subprocess.call(dns_command, shell=True)
        print(f"DNS set to {provider}: {', '.join(dns_addresses)}")

if __name__ == '__main__':
    # Create a list of available provider choices for the command line argument
    provider_choices = [name for name in DNS_PROVIDERS.keys()] + [name[0].lower() for name in DNS_PROVIDERS.keys()] + ["default", "d"]
    # Set up the command line argument parser
    parser = argparse.ArgumentParser(description='Set macOS system DNS')
    parser.add_argument('provider', choices=provider_choices, help=f'DNS provider to use:\n S: Shecan, B: Begzar, 4: 403, R: Radar, E: Electro\nD: default: the system default')
    args = parser.parse_args()
    # Call the set_dns function with the chosen provider
    set_dns(args.provider[0].upper())
