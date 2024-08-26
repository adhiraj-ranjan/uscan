# UScan

**UScan** is an efficient and asynchronous subdomain enumeration tool written in Python. It supports extracting URLs from discovered subdomains and allows filtering to include or exclude domain URLs. This tool is designed for cybersecurity enthusiasts, penetration testers, and anyone interested in discovering subdomains associated with a given domain.

## Features

- **Asynchronous Subdomain Enumeration:** Utilizes Python's `asyncio` and `aiohttp` for high-speed, non-blocking subdomain enumeration.
- **URL Extraction:** Option to extract URLs from the HTML of discovered subdomains.
- **Domain Filtering:** Ability to filter extracted URLs to include or exclude domain-specific URLs.
- **Custom Wordlists:** Supports the use of custom wordlists for subdomain discovery.
- **Results Saving:** Save discovered subdomains and URLs to files for later analysis.

## Installation

Before using **UScan**, ensure you have Python 3.7+ installed. You can install the required dependencies using `pip`:

```bash
pip install aiohttp aiofiles beautifulsoup4 pytz
```

## Usage

To use **UScan**, run it from the command line with the following options:

```bash
python uscan.py -d <target_domain> -w <wordlist_path> [-f [output_file]] [-u] [-du]
```

### Command-Line Options

- `-d, --domain`: **[Required]** Specify the target domain (e.g., `example.com`).
- `-w, --wordlist`: **[Required]** Path to the wordlist to use for subdomain enumeration.
- `-f, --file`: Save results to a file. If no file name is provided, the domain name will be used as the default file name.
- `-u, --extract-urls`: Extract URLs from the discovered subdomains (excluding domain-specific URLs by default).
- `-du, --domain-urls`: Include domain-specific URLs when extracting URLs with the `-u` option.

### Example

Enumerate subdomains for `example.com` using a wordlist:

```bash
python uscan.py -d example.com -w wordlist.txt
```

Save the results to a file named `example.com_subdomains.txt`:

```bash
python uscan.py -d example.com -w wordlist.txt -f
```

Extract URLs from the discovered subdomains and save them:

```bash
python uscan.py -d example.com -w wordlist.txt -u -f
```

Include domain-specific URLs in the extracted URLs:

```bash
python uscan.py -d example.com -w wordlist.txt -u -du -f
```

## Output

**UScan** provides the following output:

- **Subdomains:** Discovered subdomains are printed in green and can be saved to a file.
- **URLs:** Extracted URLs from the discovered subdomains are displayed under the corresponding subdomain and can be saved to a separate file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Version

**UScan** v1.0 by [@adhiraj-ranjan](https://github.com/adhiraj-ranjan)

## Contributing

Feel free to fork this repository, submit issues, or create pull requests to contribute to the project.

## Acknowledgments

Thanks to the developers of `aiohttp`, `aiofiles`, `BeautifulSoup`, and `pytz` for their excellent libraries.

---

Happy Scanning!
