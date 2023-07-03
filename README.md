
<img width="745" alt="Interactive CLI tool" src="https://github.com/aminh02/Rad-Show/assets/90900584/d49f3a8e-ce15-4048-9854-aa4be55c9b0f">


# Rad-Show: macOS System DNS Setter

This is a TUI written in python with ncurses. It supports a number of popular DNS providers, including Google, OpenDNS, and Cloudflare. It also enables Iranian users to choose DNS providers that circumvent bans on Iranian IP addresses.

## Usage

The script requires Python 3. To use it, open a terminal and navigate to the directory containing the script. Then, run the script:

```shell
git clone https://github.com/aminh02/Rad-Show.git
cd Rad-Show
python3 rad-show.py
```

Alternatively you can add it as an alias to your shell configuration file (~/.zshrc if you use ZSH):

```shell
echo 'alias dns="python3 rad-show.py"' >> ~/.zshrc
```

Now you can simply use the command `dns` to run the script.

In the interactive TUI, you can navigate between different options using the arrow keys or by typing the first letter of the option you want to select. After selecting an option, hit return/enter and confirm your choice.

The following DNS providers are supported:

- Google
- OpenDNS
- Cloudflare
- Quad9
- Shecan
- Begzar
- 403
- Radar
- Electro

To set the DNS servers to the default provided by the network, choose `Network Default`.
To flush the DNS cache, choose `Flush DNS Cache`.

## Example

To set the DNS servers to Shecan, navigate to Shecan using the arrow keys or by typing 's' an hit return/enter.

<img width="722" alt="image" src="https://github.com/aminh02/Rad-Show/assets/90900584/7909dfc0-490f-4c99-b056-0c71603a5d52">

## License

This script is released under the MIT License. See `LICENSE` for more information.
