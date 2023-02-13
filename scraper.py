from pinscrape import pinscrape
from joblib import Parallel, delayed
import os
import shutil
import argparse
import json

# Optional Settings
threads = 1
max_imgs = 100
proxy_list = {}


def rename_files(folder):
    i = 0
    for file in os.listdir(folder):
        i += 1
        old_file = os.path.join(folder, file)
        new_file = os.path.join(folder, f"{i}.jpg")
        os.rename(old_file, new_file)


def main(keyword):
    output_folder = f"./Downloads/{keyword}"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        os.mkdir(output_folder)

    print("\n Downloading....")

    details = pinscrape.scraper.scrape(
        keyword, output_folder, proxy_list, threads, max_imgs)

    rename_files(output_folder)

    if details["isDownloaded"]:
        print("\nDownloading completed !!")
        print(f"\nTotal images downloaded: {len(details['url_list'])}")
    else:
        print("\nNothing to download !!")


if __name__ == '__main__':
    if not os.path.exists("./Downloads"):
        os.mkdir("./Downloads")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q", "--query", help="Pinterest Search Query (String)")
    parser.add_argument("-j", "--json", help="list of queries (JSON)")
    parser.add_argument("-clear", "--clear",
                        help="delete all images downloaded (Boolean)")
    args = parser.parse_args()

    if args.json != None:
        with open("./query.json", "r") as f:
            query = json.load(f)
        Parallel(n_jobs=threads)(delayed(main)(arg)for arg in query)
    elif args.query != None:
        print(args.query, type(args.query))
        if isinstance(args.query, str):
            main(args.query)
        elif isinstance(args.query, list):
            Parallel(n_jobs=threads)(delayed(main)(arg)for arg in args.query)
        else:
            raise ValueError("type not supported, use String or String list")
    elif args.clear != None:
        if os.path.exists("./Downloads"):
            shutil.rmtree("./Downloads")
        else:
            raise Exception("Downloads have already been deleted")
    else:
        raise ValueError("Option not exists, use the --help flag")
