from shift_paths import base_path, processes, skim, histograms_path
from Logger import info

import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trees", action="store_true")
    return parser.parse_args()


def main():
    args = get_args()

    merge_histograms = not args.trees

    for process in processes:
        info(f"\n\n Merging {process} histograms...")
        
        hist_path = histograms_path if merge_histograms else ""
        input_path = f"{base_path}/{process}/{skim}/{hist_path}/*.root"

        info(f"\tInput path: {input_path}")

        hist_path = "_"+histograms_path if merge_histograms else ""
        output_path = f"{base_path}/{process}/merged_{skim}{hist_path}.root"
        
        info(f"\tOutput path: {output_path}")

        os.system(f"rm {output_path}")
        os.system(f"hadd -f -j -k {output_path} {input_path}")


if __name__ == "__main__":
    main()
