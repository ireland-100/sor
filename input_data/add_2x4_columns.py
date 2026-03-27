import pandas as pd
from glob import glob


if __name__ == "__main__":
    for file in glob("./*.csv"):
        df = pd.read_csv(file)
        df["not_sor0_w0_b0_ACS_pct"] = (
            1 - df["sor_ACS_pct"] - df["white_ACS_pct"] - df["black_ACS_pct"]
        )
        df["non_brazilian_ACS_pct"] = 1 - df["brazilian_ACS_pct"]
        df.to_csv(file, index=False)
