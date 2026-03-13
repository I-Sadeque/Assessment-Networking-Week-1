"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--mode", "-m", required=True,
                        choices=["validate", "complete"])
    parser.add_argument("postcode", type=str)

    args = parser.parse_args()
    postcode = args.postcode.strip().upper()

    if args.mode == "validate":
        if validate_postcode(postcode):
            print(f"{postcode} is a valid postcode.")
        else:
            print(f"{postcode} is not a valid postcode.")

    elif args.mode == "complete":
        completed = get_postcode_completions(postcode)

        if not completed:
            print(f"No matches for {postcode}.")

        for complete in completed[:5]:
            print(complete)
