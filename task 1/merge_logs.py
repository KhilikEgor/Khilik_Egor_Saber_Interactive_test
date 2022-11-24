import json
import argparse
import time
import shutil
from pathlib import Path


class Merger:
    @staticmethod
    def merge_logs(path_to_logs_1, path_to_logs_2, path_to_output):
        line_a = line_b = None
        # Open logs files and output file
        with open(path_to_logs_1, mode='r') as log_a_file, \
                open(path_to_logs_2, mode='r') as log_b_file, \
                open(path_to_output, mode='w') as output_file:
            while True:
                # Read line from each file
                if line_a is None:
                    line_a = log_a_file.readline()
                if line_b is None:
                    line_b = log_b_file.readline()

                # Find time in each line
                if line_a and line_b:
                    time_a = json.loads(line_a).get('timestamp')
                    time_b = json.loads(line_b).get('timestamp')

                    # time comparing and record to output file
                    if time_a <= time_b:
                        output_file.write(line_a)
                        line_a = None
                    else:
                        output_file.write(line_b)
                        line_b = None

                # Checking for empty files
                elif line_a and not line_b:
                    output_file.write(line_a)
                    line_a = log_a_file.readline()
                elif not line_a and line_b:
                    output_file.write(line_b)
                    line_b = log_b_file.readline()
                elif not line_a and not line_b:
                    break

    @staticmethod  # create directory like in log_generator.py
    def create_dir(dir_path: Path, force_write: bool = False) -> None:
        if dir_path.exists():
            if not force_write:
                raise FileExistsError(
                    f'Dir "{dir_path}" already exists. Remove it first or choose another one.')
            if force_write:
                shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True)

    @staticmethod  # parser arguments like in log_generator.py, updated for this program
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Tool to merge logs')

        parser.add_argument(
            'file_a',
            type=Path,
            help='path to the first log file',
        )

        parser.add_argument(
            'file_b',
            type=Path,
            help='the path to the second log file',
        )

        parser.add_argument(
            '-o', '--output',
            help="Path to the output log file",
            default="Output.jsonl",
            required=False)

        parser.add_argument(
            '-w', '--overwrite',
            action='store_const',
            const=True,
            default=False,
            help='overwrite merged log file if exists',
            dest='overwrite',
        )
        return parser.parse_args()


def main() -> None:
    args = Merger.parse_args()
    input_file_1 = Path(args.file_a)
    input_file_2 = Path(args.file_b)
    output_file = Path(args.output)

    # Create output directory
    Merger.create_dir(output_file, force_write=args.overwrite)

    # Merging logs files
    print("Merging is started...")
    t0 = time.time()
    output_file_path = output_file.joinpath('merged_log.jsonl')
    Merger.merge_logs(input_file_1, input_file_2, output_file_path)
    print(f'Merging files took {time.time() - t0:0f} sec.')


if __name__ == '__main__':
    main()
