
<img width="762" height="643" alt="Interactive CLI tool" src="https://github.com/aminh02/Rad-Show/assets/90900584/df71ea1b-4727-4de8-b0c9-7a37c954effb">


# Rad-Show: macOS System DNS Setter

This is a Python script that can be used to change the DNS servers used by the macOS system. It supports a number of popular DNS providers, including Google, OpenDNS, and Cloudflare. It also enables Iranian users to choose DNS providers that circumvent bans on Iranian IP addresses.

## Usage

The script requires Python 3 and the `argparse` module. To use it, open a terminal and navigate to the directory containing the script. Then, run the script with the following command:

```shell
python3 rad-show.py [PROVIDER]
```

Replace `[PROVIDER]` with the name of the DNS provider you want to use (you only need to type the first character). The following DNS providers are supported:

- Google
- OpenDNS
- Cloudflare
- Quad9
- Shecan
- Begzar
- 403
- Radar
- Electro

To set the DNS servers to the default value, use the following command:

```shell
python3 rad_show.py D
```

You can also use the -s option and then enter a URL, and the script will check if that website is working with the current network settings.

```shell
python3 rad_show.py chat.openai.com/chat
```

```shell
chat.openai.com/chat is available.
```

## Example

To set the DNS servers to Shecan, use the following command:

```shell
python3 rad_show.py s
```

## License

This script is released under the MIT License. See `LICENSE` for more information.
