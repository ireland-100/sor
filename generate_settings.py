from glob import glob
from pathlib import Path
from itertools import product
import json


all_csv_files = glob("./csv_files/*.csv")

#hello!!!!!
# Add county to this when the file is ready
# NOTE: Adding "county" may require modification of the for loop below
precinct_column_names = [
    "GEOID",
    # "county"
]
# fmt: off
#   ei_type,  pop_col,     candidate_names,                demographic_grp_names,         group_frac_col_names,                                                        votes_frac_col_names 
setting_tuples = [ 
    ( "2x2", "totpop_PL",  ["sor_PL_pct"],                 ["hispanic_PL_pct"],           ["hispanic_PL_pct"],                                                         ["white_PL_pct"],),
    ( "2x2", "totpop_PL",  ["sor_ACS_pct"],                ["brazilian_ACS_pct"],         ["brazilian_ACS_pct"],                                                       ["white_PL_pct"],),
    ( "2x2", "totpop_PL",  ["sor_ACS_pct"],                ["guyanese_ACS_pct"],          ["guyanese_ACS_pct"],                                                        ["white_PL_pct"],),
    ( "2x2", "totpop_ACS", ["sor_ACS_pct"],                ["cabo_verdean_ACS_pct"],      ["cabo_verdean_ACS_pct"],                                                    ["sor_ACS_pct"],),
    ( "2x2", "totpop_ACS", ["sor_ACS_pct"],                ["belizean_ACS_pct"],          ["belizean_ACS_pct"],                                                        ["sor_ACS_pct"],),
    ( "2x2", "totpop_ACS", ["hispanic_PL_pct"],            ["brazilian_ACS_pct"],         ["brazilian_ACS_pct"],                                                       ["sor_ACS_pct"],),
    ( "2x2", "totpop_PL",  ["hispanic_PL_pct"],            ["guyanese_ACS_pct"],          ["guyanese_ACS_pct"],                                                        ["hispanic_PL_pct"],),
    ( "2x2", "totpop_PL",  ["black_PL_pct"],               ["cabo_verdean_ACS_pct"],      ["cabo_verdean_ACS_pct"],                                                    ["black_PL_pct"],),
    ( "2x2", "totpop_PL",  ["hispanic_PL_pct"],            ["belizean_ACS_pct"],          ["belizean_ACS_pct"],                                                        ["hispanic_PL_pct"],),
    ( "2x2", "totpop_PL",  ["sor_ACS_pct"],                ["mena_world_bank_ACS_pct"],   ["mena_world_bank_ACS_pct"],                                                 ["hispanic_PL_pct"],),
    ( "2x2", "totpop_ACS", ["sor_ACS_pct"],                ["mena_unhcr_ACS_pct"],        ["mena_unhcr_ACS_pct"],                                                      ["sor_ACS_pct"],),
    ( "2x2", "totpop_ACS", ["sor_ACS_pct"],                ["mena_unsd_ACS_pct"],         ["mena_unsd_ACS_pct"],                                                       ["sor_ACS_pct"],),
    ( "2x2", "totpop_ACS", ["white_PL_pct"],               ["mena_world_bank_ACS_pct"],   ["mena_world_bank_ACS_pct"],                                                 ["sor_ACS_pct"],),
    ( "2x2", "totpop_ACS", ["white_PL_pct"],               ["mena_unhcr_ACS_pct"],        ["mena_unhcr_ACS_pct"],                                                      ["sor_ACS_pct"],),
    ( "2x2", "totpop_PL",  ["white_PL_pct"],               ["mena_unsd_ACS_pct"],         ["mena_unsd_ACS_pct"],                                                       ["sor_PL_pct"],),
    ( "2x4", "totpop_ACS", ["Brazilian", "Non-Brazilian"], ["SOR0", "W0", "B0", "Other"], ["white_ACS_pct", "black_ACS_pct", "sor_ACS_pct", "not_sor0_w0_b0_ACS_pct"], ["brazilian_ACS_pct", "non_brazilian_ACS_pct"]),
]
# fmt: on


if __name__ == "__main__":
    for (
        file,
        precinct_col,
        (
            ei_type,
            pop_col,
            cand_names,
            demo_group_names,
            group_frac_names,
            votes_frac_names,
        ),
    ) in product(
        all_csv_files,
        precinct_column_names,
        setting_tuples,
    ):

        settings = dict(
            csv_flie_name=str(Path(file).resolve()),
            ei_type=ei_type,
            candidate_names=cand_names,
            demographic_group_names=demo_group_names,
            precinct_column_name=precinct_col,
            group_fraction_column_names=group_frac_names,
            votes_fraction_column_names=votes_frac_names,
            pop_column_name=pop_col,
        )

        output_folder = Path("./settings_files").resolve()
        output_folder.mkdir(exist_ok=True, parents=True)
        output_name = f"{output_folder}/{Path(file).stem}--EITYPE--{ei_type}--RACE--{'-'.join(cand_names)}--DEMOGROUPS--{'-'.join(demo_group_names)}.json"

        with open(output_name, "w") as f:
            f.write(json.dumps(settings, indent=4))
