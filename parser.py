import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def parse_cor(filepath):

    metadata = {}
    rows = []

    with open(filepath, "r") as file:
        lines = file.readlines()

    data_start = None

    for i, line in enumerate(lines):

        line = line.strip()

        if line.startswith("Temperature"):
            metadata["Temperature"] = line.split(":")[-1].strip()

        elif "Surface Area:" in line:
            metadata["Surface Area"] = line.split()[-1]

        elif "Density:" in line:
            metadata["Density"] = line.split()[-1]

        elif "Weight:" in line:
            metadata["Weight"] = line.split()[-1]

        elif "Reference Potential:" in line:
            metadata["Reference Potential"] = line.split()[-1]

        elif line.startswith("E(V)"):
            data_start = i + 2
            break

    if data_start is None:
        raise Exception("Experimental data not found.")

    for line in lines[data_start:]:

        values = line.split()

        if len(values) != 3:
            continue

        try:

            voltage = float(values[0])
            current = float(values[1])
            time = float(values[2])

            rows.append([voltage, current, time])

        except:
            pass

    df = pd.DataFrame(
        rows,
        columns=["Voltage (V)", "Current Density (A/cm²)", "Time (s)"]
    )

    return metadata, df


def analyze(df):

    area = np.trapezoid(
        df["Current Density (A/cm²)"],
        df["Time (s)"]
    )

    print("\nExperiment Summary")
    print("-" * 30)
    print(f"Samples            : {len(df)}")
    print(f"Duration           : {df['Time (s)'].max():.2f} s")
    print(f"Average Current    : {df['Current Density (A/cm²)'].mean():.5e}")
    print(f"Peak Current       : {df['Current Density (A/cm²)'].max():.5e}")
    print(f"Integrated Current : {area:.5e}")


def plot(df):

    plt.figure(figsize=(8,5))

    plt.plot(
        df["Time (s)"],
        df["Current Density (A/cm²)"]
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Current Density (A/cm²)")
    plt.title("Current Density vs Time")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("current_vs_time.png", dpi=300)
    plt.show()


def main():

    if len(sys.argv) != 2:
        print("Usage: python parser.py sample.cor")
        return

    filepath = sys.argv[1]

    metadata, df = parse_cor(filepath)

    print("\nMetadata")
    print("-" * 30)

    for key, value in metadata.items():
        print(f"{key}: {value}")

    df.to_csv("output.csv", index=False)

    analyze(df)

    plot(df)

    print("\nCSV exported -> output.csv")
    print("Plot saved   -> current_vs_time.png")


if __name__ == "__main__":
    main()
