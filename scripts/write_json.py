import pandas as pd
from phlspending.data import *
from phlspending.core import *
from pathlib import Path
import json

from phila_style import *
from phila_style.matplotlib import get_theme

palette = get_default_palette()
standards = get_digital_standards()

cwd = Path(".")


def overtime():

    data = load_employee_OT_data().query("dept_number != '22'")
    X = data.copy()
    X["class_100"] *= X["cpi_factor"]
    X["class_100_OT"] *= X["cpi_factor"]
    X = X.groupby("fiscal_year")[["class_100", "class_100_OT", "total_employees"]].sum()
    Y = X["class_100_OT"] / X["total_employees"]

    X = (Y / 1e3).reset_index(name="ot_per_employee")

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(cwd / ".." / "src" / "data" / "overtime_per_employee.json", "w") as ff:
        json.dump(out, ff)


def get_color(row):
    if row["diff"] < -200:
        return standards["love-park-red"]
    if row["diff"] > 20:
        return standards["love-park-red"]
    return palette["medium-gray"]


def employees_by_dept():
    FY20_Q2 = load_FY20_employees(quarter=2)
    data = load_employee_OT_data()
    employees = pd.concat(
        [data[["dept_name", "dept_number", "fiscal_year", "total_employees"]], FY20_Q2]
    )
    employees_no_DHS = employees.query("dept_number != 22")

    # Get the differences
    start_year = 2017
    end_year = 2020

    e = calculate_difference(
        employees_no_DHS.groupby(["fiscal_year", "dept_name"])["total_employees"].sum(),
        year2=start_year,
        year1=end_year,
    ).assign(percent_diff=lambda df: df["diff"] / df[start_year])

    e["color"] = e.apply(get_color, axis=1)

    data = []
    for i in range(len(e)):
        X = e.iloc[i]
        data.append({"name": X["dept_name"], "data": [[X["diff"], X[2020]]]})

    out = {"data": data, "colors": e["color"].tolist()}
    with open(cwd / ".." / "src" / "data" / "employees_by_dept.json", "w") as ff:
        json.dump(out, ff)


def employees():

    data = load_employee_OT_data()
    citywide_quarterly = load_quarterly_employee_count(kind="citywide")

    # Plot number of employees
    N_all = data.groupby("fiscal_year")["total_employees"].sum()

    # Subtract DHS
    dhs_counts = load_quarterly_employee_count(kind="DHS")
    dhs_q4 = dhs_counts.query("quarter == 4").set_index("fiscal_year")
    N = N_all - dhs_q4["general_fund"]

    # FY20 Q2
    fy20_q2 = (
        citywide_quarterly.query("fiscal_year == 2020 and quarter == 2")[
            "actual_positions"
        ].squeeze()
        - dhs_counts.query("fiscal_year == 2020 and quarter == 2")[
            "general_fund"
        ].squeeze()
    )

    X = N.append(pd.Series([fy20_q2], index=[2020]))
    X = X.rename_axis("fiscal_year").reset_index(name="total_employees")

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(cwd / ".." / "src" / "data" / "historical_employees.json", "w") as ff:
        json.dump(out, ff)


def payroll():

    data = load_employee_OT_data()
    X = data.groupby("fiscal_year")[
        ["class_100", "class_100_OT", "total_employees"]
    ].sum()
    X = (X["class_100"] / 1e9).reset_index()

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(cwd / ".." / "src" / "data" / "historical_payroll.json", "w") as ff:
        json.dump(out, ff)


def increases_by_major_class():

    df = load_disbursements()
    X = (
        calculate_difference(
            df.groupby(["fiscal_year", "major_class_description"])["amount"].sum(),
            year1=2019,
            year2=2017,
        ).set_index("major_class_description")["diff"]
        / 1e6
    ).reset_index()

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(cwd / ".." / "src" / "data" / "increases_by_major_class.json", "w") as ff:
        json.dump(out, ff)


def by_major_class_normalized():

    # Load data
    actual = load_spending_by_major_class().query("kind == 'Actual'")

    # Classes
    class_labels = CLASS_LABELS
    classes = list(class_labels)

    # remove DHS
    actual_no_DHS = actual.query("dept != '22'")

    X = actual_no_DHS.groupby("fiscal_year")[classes].sum().rename(columns=class_labels)
    X = X / 1e6

    X = X.div(X.sum(axis=1), axis=0)
    X = X.reset_index()

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(
        cwd / ".." / "src" / "data" / "by_major_class_normalized.json", "w"
    ) as ff:
        json.dump(out, ff)


def by_major_class():

    # Load data
    actual = load_spending_by_major_class().query("kind == 'Actual'")

    # Classes
    class_labels = CLASS_LABELS
    classes = list(class_labels)

    # remove DHS
    actual_no_DHS = actual.query("dept != '22'")

    X = actual_no_DHS.groupby("fiscal_year")[classes].sum().rename(columns=class_labels)
    X = (X / 1e6).reset_index()

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(cwd / ".." / "src" / "data" / "by_major_class.json", "w") as ff:
        json.dump(out, ff)


def historical_spending():

    df = load_historical_data()
    X = df.set_index("fiscal_year")
    X = (X["spending"] / 1e6).reset_index()

    out = {}
    for col in X:
        out[col] = X[col].tolist()
    with open(cwd / ".." / "src" / "data" / "historical_spending.json", "w") as ff:
        json.dump(out, ff)


if __name__ == "__main__":

    historical_spending()
    by_major_class()
    by_major_class_normalized()
    increases_by_major_class()
    payroll()
    employees()
    employees_by_dept()
    overtime()
