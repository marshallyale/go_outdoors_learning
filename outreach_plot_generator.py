"""This script is used for Go Outdoors to take an excel file, parse it, and then create plots showing the children's progress"""
from typing import Any
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def create_df_dict_from_excel(excel_file: str) -> Any:
    """Create the dictionary of dataframes from an excel file. Ignores any sheets that are blank.

    Args:
        excel_file (str): String pointing to either relative or absolute path of excel file

    Returns:
        Any: Dictionary of dataframes which correspond to sheets in an excel file
    """
    df_dict = pd.read_excel(excel_file, sheet_name=None)
    keys_to_delete = (
        []
    )  # Can't delete empty dfs in loop or else we get a dictionary changed size error
    for key, value in df_dict.items():
        if value.empty:
            keys_to_delete.append(key)
        else:
            df_dict[key] = df_dict[key].fillna(0)

    for key in keys_to_delete:
        del df_dict[key]
    return df_dict


def create_plottable_df(df):
    """Takes an initial dataframe and returns a knowledge dataframe and an
    interest dataframe which are ready to be plotted

    Args:
        df (pandas dataframe): Dataframe which is ready to be plotted

    Returns:
        pandas_dataframe: Dataframe which corresponds to the student's interest in a particular subject
        pandas_dataframe: Dataframe which corresponds to the student's before and after knowledge of a subject
    """
    topic = df.columns[0]  # Grabbing topic
    df.columns = df.iloc[1]  # Setting column names

    # Pulling out student votes for knowledge level from xlsx
    knowledge_before = df.iloc[2:, 1:4].sum(axis=0)
    knowledge_after = df.iloc[2:, 4:7].sum(axis=0)
    interest = (df.iloc[2:, 7:10]).sum(axis=0)
    # Have to concatenate both series into a dataframe, reset the indexes, and then transpose
    df_knowledge = pd.concat(
        [knowledge_before, knowledge_after], axis=1, keys=["Before", "After"]
    )
    df_knowledge = df_knowledge.T  # Transpose to get things in correct order
    knowledge_columns = list(
        df_knowledge.columns
    )  # Grab final column names (don't hardcode in case they change)
    df_knowledge[knowledge_columns] = df_knowledge[knowledge_columns].apply(
        lambda x: (x / x.sum()) * 100, axis=1
    )  # Convert everything to percentage
    df_knowledge.columns.name = topic

    df_int = pd.DataFrame(interest)
    df_int = df_int.iloc[::-1]
    interest_column = ["Interest"]
    df_int.columns = interest_column
    df_int[interest_column] = df_int[interest_column].apply(
        lambda x: (x / x.sum()) * 100, axis=0
    )  # Convert everything to percentage
    df_int.index.name = (
        None  # Have to remove this or else it will display on the plots
    )
    return df_knowledge, df_int


def main():
    """Main function"""
    excel_file = args.excel_file
    df_dict = create_df_dict_from_excel(excel_file)
    plot_dfs = []
    plot_interest = []
    for df in df_dict.values():
        plot_df, interest = create_plottable_df(df)
        plot_dfs.append(plot_df)
        plot_interest.append(interest)

    for i, plot_df in enumerate(plot_dfs):
        fig = plt.figure()
        topic = plot_df.columns.name
        subplot_title_x_loc = 0.5  # Change this to change the location of the title (i.e. The topics)
        subplot_title_y_loc = 1.05
        fig.suptitle(
            topic, x=subplot_title_x_loc, y=subplot_title_y_loc, fontsize=14
        )
        axes = fig.subplots(nrows=1, ncols=2)

        ax1 = plot_df.plot(
            kind="bar",
            stacked=True,
            ax=axes[1],
            color=["#2A788EFF", "#7AD151FF", "#FDE725FF"],  # "#440154FF",
            title="Knowledge Gains",
        )
        ax1.legend(
            loc="lower left", bbox_to_anchor=(1, 0), title="Knowledge Level"
        )
        ax1.yaxis.set_major_formatter(mtick.PercentFormatter())

        ax2 = plot_interest[i].plot(
            kind="bar",
            ylabel="Votes",
            legend=False,
            ax=axes[0],
            title="Interest",
        )
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        fig.tight_layout()
        title = f"plots/{topic}.png"
        fig.savefig(title, dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates plots from excel file for Go Outdoors"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        dest="excel_file",
        help="Excel file to create plots from",
        required=True,
    )
    args = parser.parse_args()
    main()
