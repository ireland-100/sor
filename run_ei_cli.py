import pandas as pd
from pathlib import Path
from pyei.two_by_two import TwoByTwoEI
from pyei.r_by_c import RowByColumnEI
from matplotlib import pyplot as plt
import click
import json

##Things that Chloe added in January
from pyei.goodmans_er import GoodmansER
from pyei.goodmans_er import GoodmansERBayes

####

EI_MODELS = {
    "2x2": TwoByTwoEI,
    "2x4": RowByColumnEI,
}

EI_PARAMETERS = {
    "2x2": {
        "model_name": "king99_pareto_modification",
        "pareto_scale": 15,
        "pareto_shape": 2,
    },
    "2x4": {"model_name": "multinomial-dirichlet"},
}


def run_ei(
    csv_flie_name: str,
    ei_type: str,
    candidate_names: list[str],
    demographic_group_names: list[str],
    precinct_column_name: str,
    group_fraction_column_names: list[str],
    votes_fraction_column_names: list[str],
    pop_column_name: str,
    show_progressbar: bool,
):
    e_df = pd.read_csv(csv_flie_name)
    e_df.fillna(0, inplace=True)

    group_fraction_matrix = e_df[group_fraction_column_names].to_numpy().squeeze()
    votes_fraction_matrix = e_df[votes_fraction_column_names].to_numpy().squeeze()

    if ei_type == "2x4":
        group_fraction_matrix = group_fraction_matrix.T
        votes_fraction_matrix = votes_fraction_matrix.T

    population_vector = e_df[pop_column_name].to_numpy().squeeze().astype(int)
    precinct_df = e_df[precinct_column_name]

    ei_model = EI_MODELS[ei_type](**EI_PARAMETERS[ei_type])

    if ei_type == "2x2":
        ei_model.fit(
            group_fraction_matrix,
            votes_fraction_matrix,
            population_vector,
            demographic_group_name=demographic_group_names[0],
            candidate_name=candidate_names[0],
            precinct_names=precinct_df,
            chains=4,
            progressbar=show_progressbar,
        )

    else:
        ei_model.fit(
            group_fraction_matrix,
            votes_fraction_matrix,
            population_vector,
            demographic_group_names=demographic_group_names,
            candidate_names=candidate_names,
            precinct_names=precinct_df,
            chains=4,
            progressbar=show_progressbar,
        )

    return ei_model


@click.command()
@click.option("--settings-file", type=str)
def main(settings_file: str):
    with open(settings_file, "r") as file:
        settings = json.load(file)

    model = run_ei(
        **settings,
        show_progressbar=False,
    )

    dem_group_names = (
        model.demographic_group_name
        if hasattr(model, "demographic_group_name")
        else "-".join(model.demographic_group_names)
    )
    cand_names = (
        model.candidate_name
        if hasattr(model, "candidate_name")
        else "-".join(model.candidate_names)
    )

    summary_dict = {
        f"summary": model.summary(),
        f"posterior_mean_{dem_group_names}_{cand_names}": model.posterior_mean_voting_prefs[
            0
        ]
        .astype(float)
        .tolist(),
        f"credible_interval_{dem_group_names}_{cand_names}": model.credible_interval_95_mean_voting_prefs[
            0
        ].tolist(),
        f"posterior_mean_NON_{dem_group_names}_{cand_names}": model.posterior_mean_voting_prefs[
            1 #### this is probably where the error is, so I changed it
        ]
        .astype(float)
        .tolist(),
        f"credible_interval_NON_{dem_group_names}_{cand_names}": model.credible_interval_95_mean_voting_prefs[
            1 ### same as above
        ].tolist(),
    }

    output_summary_file = Path("./summary_files").resolve() / Path(
        Path(settings_file).stem + "--SUMMARY.json"
    )
    with open(output_summary_file, "w") as f:
        json.dump(summary_dict, f, indent=4)

    output_plot_file = Path("./plots").resolve() / Path(
        Path(settings_file).stem + "--PLOT.png"
    )

    output_goodmans_file = Path("./plots").resolve() / Path(
        Path(settings_file).stem + "--GOODMANSPLOT.png"
    )

    # The 2x4 plots KDES, so we need to separate it
    if isinstance(model, TwoByTwoEI):
        plt.clf()
        goodmans_er = GoodmansER(is_weighted_regression="True")
        goodmans_er.fit(group_fraction_matrix,
                        votes_fraction_matrix,
                        population_vector,
                        demographic_group_name=demographic_group_names,
                        candidate_name=candidate_names)

        fig, _ = goodmans_er.plot()

        fig.savefig(output_goodmans_file, bbox_inches="tight", dpi=300)

        ###########

        #ax[0].set_xlim(-0.1, 1.01)
        #ax[1].set_xlim(-0.1, 1.01)
        #plt.savefig(output_plot_file, bbox_inches="tight", dpi=300)
    else:
        plt.clf()
        _, ax = plt.subplots()
        model.plot_kdes(plot_by="candidate", axes=ax)
        plt.savefig(output_plot_file, bbox_inches="tight", dpi=300)

    print("Done!")


if __name__ == "__main__":
    main()
