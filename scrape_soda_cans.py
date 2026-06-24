import argparse
import os

from icrawler.builtin import BingImageCrawler

COLOR_QUERIES = {
    "red": ["red soda can", "red aluminum can drink", "red pop can", "red cola can"],
    "green": ["green soda can", "green aluminum can drink", "green pop can", "green cola can"],
    "blue": ["blue soda can", "blue aluminum can drink", "blue pop can", "blue cola can"],
}


def scrape_color(color, queries, output_dir, max_num):
    target_dir = os.path.join(output_dir, color)
    for query in queries:
        count = len(os.listdir(target_dir)) if os.path.isdir(target_dir) else 0
        if count >= max_num:
            break
        crawler = BingImageCrawler(storage={"root_dir": target_dir})
        crawler.crawl(keyword=query, max_num=max_num - count, filters={"type": "photo"})
    return target_dir


def main():
    parser = argparse.ArgumentParser(
        description="Download sample soda can images by color using icrawler."
    )
    parser.add_argument("--max-num", type=int, default=50, help="images per color")
    parser.add_argument("--output-dir", default="data", help="root output directory")
    args = parser.parse_args()

    for color, queries in COLOR_QUERIES.items():
        target_dir = scrape_color(color, queries, args.output_dir, args.max_num)
        count = len(os.listdir(target_dir)) if os.path.isdir(target_dir) else 0
        print(f"{color}: {count} images in {target_dir}")


if __name__ == "__main__":
    main()
