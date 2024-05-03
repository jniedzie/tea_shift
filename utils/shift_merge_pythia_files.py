from shift_paths import base_path, processes, skim, variant
from Logger import info

import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trees", action="store_true")
    return parser.parse_args()


def main():
    args = get_args()

    for process in processes:
        info(f"\n\n Merging {process} histograms...")
        
        input_path = f"{base_path}/{process}/{variant}/histograms/*.root"
        output_path = f"{base_path}/{process}/merged_{variant}_histograms.root"

        if args.trees:
            input_path = input_path.replace("histograms", "trees")
            output_path = output_path.replace("histograms", "trees")

        info(f"\tInput path: {input_path}")
        info(f"\tOutput path: {output_path}")

        os.system(f"rm {output_path}")
        os.system(f"hadd -f -j -k {output_path} {input_path}")


if __name__ == "__main__":
    main()
