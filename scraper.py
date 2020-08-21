import argparse

from src.pquery import ProteinQuery


def write_csv(records, out):
    with open(out, "w") as h:
        h.write("HMDB_id,UniProt_id,name\n")
        for record in records:
            h.write(",".join(record))
            h.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Using a keyword to search in HMDB and save results to a table")
    parser.add_argument("-k", type=str, required=True,
                        help="keywords to search in HMDB")
    parser.add_argument("-o", type=str, required=True,
                        help="output path of comma-delimited result table")
    args = parser.parse_args()

    query = ProteinQuery(args.k)
    query.parse()
    write_csv(query.res, args.o)