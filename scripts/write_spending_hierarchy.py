from phlspending.data import *
from pathlib import Path
import json

cwd = Path(".")

COLUMNS = [
    "major_class_description",
    "dept_name_short",
    "class_superset",
    "class_description",
    "index_code_description",
]
FY = 2019


def create_entries(df):
    entries = []
    # Stopping case
    if df.shape[1] == 2:  # only 2 columns left
        X = df.groupby(df.columns[0])[df.columns[-1]].sum().reset_index()
        for i in range(X.shape[0]):  # iterating on rows
            entries.append({"name": X.iloc[i, 0], "value": X.iloc[i, 1]})
    # Iterating case
    else:
        values = set(df.iloc[:, 0])  # Getting the set of unique values
        for v in values:
            entries.append(
                {
                    "name": v,
                    # reiterating the process but without the first column
                    # and only the rows with the current value
                    "children": create_entries(df.loc[df.iloc[:, 0] == v].iloc[:, 1:]),
                }
            )
    return entries


if __name__ == "__main__":

    # Load the data
    checkbook = load_disbursements()

    # Do the nested grouping
    data = checkbook.query(f"fiscal_year == {FY}")

    # Nested calculation
    out = {"name": FY, "children": create_entries(data[COLUMNS + ["amount"]])}

    # Save
    filename = cwd / ".." / "src" / "data" / f"spending_hierarchy_{FY}.json"
    json.dump(out, open(filename, "w"))

