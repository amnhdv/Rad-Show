#!/usr/bin/env python3

import argparse
import subprocess
import requests

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
        return f"          \033[1;32m<DNS set to default.>\033[0m        "
    # Otherwise, set the DNS to the chosen provider's IP addresses
    provider_options = [name for name in DNS_PROVIDERS.keys() if name.lower().startswith(provider.lower())]
    if len(provider_options) == 0:
        return f"\033[1;31m<No provider starting with '{provider}' found>\033[0m"
    elif len(provider_options) > 1:
        return f"\033[1;33m<Several provider options: {provider_options}. Retry>\033[0m"
    else:
        provider = provider_options[0]
        dns_addresses = DNS_PROVIDERS[provider]
        # Construct and execute the command to set the DNS
        dns_command = f"networksetup -setdnsservers Wi-Fi {' '.join(dns_addresses)}"
        subprocess.call(dns_command, shell=True)
        print(f"\033[1;32mDNS set to {provider}: {', '.join(dns_addresses)}\033[0m")
        return "         \033[1;32m<DNS Addresses Set.>\033[0m        "

def check_availability(url):
    try:
        r = requests.head(url)
        return f"{url} is available."
    except requests.ConnectionError:
        return f"{url} is unavailable. Please check address/your connection or change the DNS provider."
    except requests.exceptions.MissingSchema:
        try:
            r = requests.head("http://" + url)
            return f"{url} is available."
        except requests.ConnectionError:
            return f"{url} is unavailable. Please check address/your connection or change the DNS provider."

def flush_dns_cache():
    subprocess.run(["dscacheutil", "-flushcache"])
    return "         \033[1;32m<DNS cache flushed.>\033[0m        "

# Create a list of available provider choices for the command line argument
provider_choices = [name for name in DNS_PROVIDERS.keys()] + [name[0].lower() for name in DNS_PROVIDERS.keys()] + ["default", "d"]
# Set up the command line argument parser

def generate_prompt(user_choice, output):
    default_color = "\033[1;33m"
    highlight_color = "\033[1;32m"

    google_color = highlight_color if user_choice.lower()[0] == 'g' else default_color
    opendns_color = highlight_color if user_choice.lower()[0] == 'o' else default_color
    cloudflare_color = highlight_color if user_choice.lower()[0] == 'c' else default_color
    quad9_color = highlight_color if user_choice.lower()[0] == 'q' else default_color
    shecan_color = highlight_color if user_choice.lower()[0] == 's' else default_color
    begzar_color = highlight_color if user_choice.lower()[0] == 'b' else default_color
    _403_color = highlight_color if user_choice.lower()[0] == '4' else default_color
    radar_color = highlight_color if user_choice.lower()[0] == 'r' else default_color
    electro_color = highlight_color if user_choice.lower()[0] == 'e' else default_color
    default_color = highlight_color if user_choice.lower()[0] == 'd' else default_color
    
    output_text = output
    prompt = f"""
    ___  __  __     __ _  _  __  _   _  
    | _ \/  \| _\  /' _| || |/__\| | | | 
    | v | /\ | v | `._`| >< | \/ | 'V' | 
    |_|_|_||_|__/  |___|_||_|\__/!_/ \_! 
                                                               
###########################################
#                                         #
#        \033[1;36mChoose your DNS provider:\033[0m        #
#                                         #
#       {google_color}G: Google\033[0m        {opendns_color}O: OpenDNS\033[0m       #
#       {cloudflare_color}C: Cloudflare\033[0m    {quad9_color}Q: Quad9\033[0m         #
#       {shecan_color}S: Shecan\033[0m        {begzar_color}B: Begzar\033[0m        #
#       {_403_color}4: 403\033[0m           {radar_color}R: Radar\033[0m         #
#       {electro_color}E: Electro\033[0m       {default_color}D: default\033[0m       #
#                                         #
#       \033[1;32mEnter f to flush DNS cache.\033[0m       #
#       \033[1;31mEnter p, followed by URL to\033[0m       #
#       \033[1;31m    check availability.\033[0m           #
#              \033[1;32mHit x to exit.\033[0m             #
#                \033[1;34mCommand: \033[1;34m{str(user_choice)[0]}\033[0m               #
#                                         #
#  {output_text}  #
#                                         #
###########################################
"""
    return prompt

global user_choice
user_choice = "f"
output = "                                     "
while True:
    subprocess.call("clear", shell=True)
    prompt = generate_prompt(user_choice, output)
    user_choice = input(prompt + "\033[1;36mEnter your choice or 'x' to exit: \033[0m")
    # @TODO Sanitize the input
    k = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    result = "".join(list(filter(lambda x: x in k, user_choice)))
    if user_choice == "":
        exit()
    elif user_choice.lower().startswith('x'):
        break
    elif user_choice.lower().startswith('p'):
        output = check_availability(user_choice.split(" ")[1])
    elif user_choice.lower().startswith('f'):
        output = flush_dns_cache()
    else:
        output = set_dns(user_choice.upper())

# Call the set_dns function with the chosen provider