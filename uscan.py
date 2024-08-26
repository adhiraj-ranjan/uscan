import argparse
import asyncio
import aiohttp
import aiofiles
from datetime import datetime
import pytz
import time
from bs4 import BeautifulSoup
import re

print('[ VERSION INFO ] UScan v1.0 by @github.com/adhiraj-ranjan\n')

ist_timezone = pytz.timezone('Asia/Kolkata')

BATCH_SIZE = 1000

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

DOMAIN_REGEX_PATTERN = r'(?:https?:\/\/)?(?:www\.)?(?:[^\.]+\.)?([^\.]+\.[^\/:]+)'


def current_datetime_ist():
    return datetime.now(ist_timezone).strftime('%H:%M:%S %Z%z')

class SubdomainEnumerator:
    def __init__(self, domain, wordlist, output_file=None):
        self.domain = domain
        self.wordlist = wordlist
        self.output_file = output_file
        self.found_subdomains = set()  # Use a set to avoid duplicates
        self.found_urls = set()

    async def load_wordlist(self):
        async with aiofiles.open(self.wordlist, mode='r') as file:
            lines = await file.readlines()
        return [line.strip() for line in lines if line.strip()]

    async def check_subdomain(self, session, subdomain):
        url = f"http://{subdomain}.{self.domain}"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    print(f"\033[0;32m[ DNS ] {url}\033[0m")
                    self.found_subdomains.add(url)

                    # Extract URLs from the response HTML
                    if args.extract_urls:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        for link in soup.find_all('a', href=True):
                            found_url = link['href'].split()[0]
                            
                            if args.domain_urls:
                                match = re.search(DOMAIN_REGEX_PATTERN, found_url)
                                if not match or match.group(1) == self.domain: # unable to retrieve domain name
                                    continue
                            
                            if found_url not in self.found_urls:
                                print(f"\t{found_url}")
                                self.found_urls.add(found_url)

        except aiohttp.ClientError:
            pass  # Ignore the subdomains that don't resolve
        except UnicodeError:
            pass # Ignore invalid subdomains

    async def run(self):
        print("[ info ] Loading wordlist at", current_datetime_ist())
        subdomains = await self.load_wordlist()
        print(f"[ info ] {len(subdomains)} lines Loaded!")

        print("[ info ] Started Subdomain Enumeration at", current_datetime_ist(), "\n")
        start_timestamp = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                for i in range(0, len(subdomains), BATCH_SIZE):
                    
                    tasks = [self.check_subdomain(session, subdomain) for subdomain in subdomains[i:i + BATCH_SIZE]]
                    # print("awaiting", BATCH_SIZE, "tasks")
                    await asyncio.gather(*tasks)
                    # print("Progress:", i + BATCH_SIZE)

        finally:   
            print(f"\n[ info ] Scan took {round(time.time() - start_timestamp, 2)}s, Found {len(self.found_subdomains)} Sub Domains")
            if self.output_file:
                await self.save_subdomain_results()
                if args.extract_urls:
                    await self.save_url_results() 
            # else:
            #     print("[ info ] No output file specified; results not saved.")
        
        print("[ info ] Enumeration completed at", current_datetime_ist())

    async def save_url_results(self):
        fname = self.output_file + "_urls.txt"
        async with aiofiles.open(fname, mode='w') as file:
            for url in self.found_urls:
                await file.write(f"{url}\n")
        print(f"[ info ] Urls saved to {fname}")

    async def save_subdomain_results(self):
        fname = self.output_file + "_subdomains.txt"
        async with aiofiles.open(fname, mode='w') as file:
            for subdomain in self.found_subdomains:
                await file.write(f"{subdomain}\n")
        print(f"[ info ] Subdomains saved to {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Enumeration Tool")
    parser.add_argument("-d", "--domain", help="Target domain (e.g., example.com)", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist", required=True)
    parser.add_argument("-f", "--file", nargs='?', const=True, help="Save results to a file (default: domain name)")
    parser.add_argument("-u", "--extract-urls", action='store_true', help="Extract URls from Subdomains ( only with other domains )")
    parser.add_argument("-du", "--domain-urls", action='store_true', help="include Domain urls in --extarct-urls or -u")
    args = parser.parse_args()

    if args.file is True:
        output_file = args.domain  # Default filename
    else:
        output_file = args.file


    enumerator = SubdomainEnumerator(args.domain, args.wordlist, output_file if output_file != True else None)

    try:
        asyncio.run(enumerator.run())

    except KeyboardInterrupt:
        print("[ info ] Keyboard interrupted received")
