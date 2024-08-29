import argparse
import sys

from bs4 import BeautifulSoup
import requests


def main(input_url: str, depth: int=0, output_file: str = None, verbose: bool= False) -> None:
    base_url: str = input_url
    visited_urls: set = set(scrape(input_url, []))

    def parseUrl(input_url):
        return (
            base_url + input_url 
            if str(input_url).startswith("/") or str(input_url).startswith("#") 
            else input_url
        )

    for _ in range(depth):
        next_set = []

        if not visited_urls:
            continue
        
        for input_url in visited_urls:
            try:
                next_set.extend(set(scrape(parseUrl(input_url), next_set)))
            except TypeError:
                continue
        
        
        visited_urls.union(set(next_set))
        visited_urls = set(visited_urls)
        
    visited_urls = set(visited_urls)

    if verbose:
        for url in visited_urls:
            print(url)

    if output_file:
        with open(output_file, mode="a") as file:
            file.writelines([f"{url}\n" for url in visited_urls])


def scrape(input_url: str, url_set: list[str]) -> list[str]:
    try:
        response = requests.get(input_url)
    except Exception:
        return url_set

    if response.status_code == 404:
        return url_set

    soup = BeautifulSoup(response.content, "html.parser")
    atags = soup.find_all('a')
    
    def filterUrl(url:str):
        return url and not (url.startswith("javascript") or url.startswith("mailto"))

    url_found: list[str] = [ tag.get("href") for tag in atags if filterUrl(tag.get("href")) ]

    url_set.extend(url_found)
    
    return url_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="URL Crawler", description='Scrape site urls')
    parser.add_argument("-l", '--link', metavar='str', type=str, help='Base URL site as string',  default=sys.stdin, required=True)
    parser.add_argument("-d", '--depth', metavar='int', type=int, help='Lookup depth as integer', default=0, required=False)
    parser.add_argument("-o", '--output', metavar='str', type=str, help='Output file path as string', default=None, required=False)
    parser.add_argument("-v",'--verbosity', help='Output file path as string', action="store_true")
    args = parser.parse_args()

    try:
        main(
            input_url=args.link, 
            depth=args.depth, 
            output_file=args.output, 
            verbose=args.verbosity
        )
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)