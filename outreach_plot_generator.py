"""This script is used for Go Outdoors to take a csv file, parse it, and then create plots showing the children's progress"""
import argparse
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import regex as re


def get_topic_df_from_csv(csv_file):
    """Create the dictionary of dataframes from a csv file.

    Args:
        csv_file (str): String pointing to either relative or absolute path of excel file

    Returns:
        Any: Dictionary of dataframes which correspond to sheets in an excel file
    """
    topics = []
    df_dict = {}
    topic_regex = re.compile(r"(?<=How much did you know about )(.*)(?= BEFORE)")
    after_regex = re.compile(r"(?<=How much did you know about )(.*)(?= AFTER)")
    interest_regex = re.compile(r"(?<=How much did you LIKE )(.*)")
    df = pd.read_csv(csv_file)
    for column in df.columns:
        match = topic_regex.search(column)
        if match:
            topics.append(match.group(1))
    for topic in topics:
        filtered_columns = df.filter(regex=topic).columns
        # Select the columns you want to keep
        df_dict[topic] = df[filtered_columns]
    # Verify that the needed columns are in the dataframe
    for topic, topic_df in df_dict.items():
        columns = "-".join(topic_df.columns)
        after_match = after_regex.search(columns)
        interest_match = interest_regex.search(columns)
        if not after_match:
            print(f"The topic {topic} is missing the AFTER question. Exiting.")
            sys.exit(1)
        if not interest_match:
            print(f"The topic {topic} is missing the INTEREST question. Exiting.")
            sys.exit(1)
    return df_dict


def create_plottable_df(df, topic):
    """Takes an initial dataframe and returns a knowledge dataframe and an
    interest dataframe which are ready to be plotted

    Args:
        df (pandas dataframe): Dataframe which is ready to be plotted

    Returns:
        pandas_dataframe: Dataframe which corresponds to the student's interest in a particular subject
        pandas_dataframe: Dataframe which corresponds to the student's before and after knowledge of a subject
    """
    # Need to pull out the correct scale
    learn_scale_match = re.search(r"(?<=lesson\?\n)((.|\n)*)", df.columns[0])
    if learn_scale_match:
        learn_scale = {}
        scale_group = learn_scale_match.group(1)
        scale_group = scale_group.split("\n")
        for line in scale_group:
            line = line.split(" = ")
            learn_scale[int(line[0])] = line[1]
    else:
        print(
            "Couldn't extract scale from csv. Assuming 1-4 for learning, 1-3 for interest"
        )
    learn_scale = {1: "Nothing", 2: "A little", 3: "Some", 4: "A lot"}
    interest_scale = {1: "Dislike", 2: "Like", 3: "Love"}
    # Need to now rename columns so they aren't so damn long
    # df.columns = scale.values()
    # # Setting column names
    column_rename_map = {}
    for column in df.columns:
        if "BEFORE" in column:
            column_rename_map[column] = "before"
        elif "AFTER" in column:
            column_rename_map[column] = "after"
        elif "LIKE" in column:
            column_rename_map[column] = "like"
        else:
            print(f"Column not known. {column}")
    df = df.rename(columns=column_rename_map)
    # Pulling out student votes for knowledge level from xlsx
    knowledge_before = df["before"].value_counts()
    knowledge_after = df["after"].value_counts()
    interest = df["like"].value_counts()
    # Have to concatenate both series into a dataframe, reset the indexes, and then transpose

    df_knowledge = pd.concat(
        [knowledge_before, knowledge_after], axis=1, keys=["Before", "After"]
    )
    df_knowledge = df_knowledge.sort_index(ascending=True)
    df_knowledge = df_knowledge.T
    knowledge_columns = list(
        df_knowledge.columns
    )  # Grab final column names (don't hardcode in case they change)
    df_knowledge[knowledge_columns] = df_knowledge[knowledge_columns].apply(
        lambda x: (x / x.sum()) * 100, axis=1
    )  # Convert everything to percentage
    df_knowledge = df_knowledge.rename(columns=learn_scale)
    df_knowledge.columns.name = topic
    df_int = pd.DataFrame(interest)
    interest_column = ["Interest"]
    df_int.columns = interest_column
    df_int[interest_column] = df_int[interest_column].apply(
        lambda x: (x / x.sum()) * 100, axis=0
    )  # Convert everything to percentage
    df_int.index.name = None  # Have to remove this or else it will display on the plots
    df_int = df_int.sort_index(ascending=True)
    df_int = df_int.rename(index=interest_scale)
    return df_knowledge, df_int


def main():
    """Main function"""
    csv_file = args.csv_file
    df_dict = get_topic_df_from_csv(csv_file)
    plot_dfs = []
    plot_interest = []
    for topic, df in df_dict.items():
        print(f"Generating plots for topic {topic}")
        plot_df, interest = create_plottable_df(df, topic)
        plot_dfs.append(plot_df)
        plot_interest.append(interest)

    for i, plot_df in enumerate(plot_dfs):
        fig = plt.figure()
        topic = plot_df.columns.name
        subplot_title_x_loc = (
            0.5  # Change this to change the location of the title (i.e. The topics)
        )
        subplot_title_y_loc = 1.05
        fig.suptitle(topic, x=subplot_title_x_loc, y=subplot_title_y_loc, fontsize=14)
        axes = fig.subplots(nrows=1, ncols=2)

        ax1 = plot_df.plot(
            kind="bar",
            stacked=True,
            ax=axes[1],
            # color=["#2A788EFF", "#7AD151FF", "#FDE725FF", "#440154FF"],  # ,
            color=["#fd9c5a", "#ffceaa", "#a0cbeb", "#4099d7"],
            title="Knowledge Gains",
        )
        ax1.legend(loc="lower left", bbox_to_anchor=(1, 0), title="Knowledge Level")
        # Reversing the legend
        handles, labels = ax1.get_legend_handles_labels()
        # Reverse the order of handles and labels
        handles = handles[::-1]
        labels = labels[::-1]
        # Create a new legend with the reversed order
        ax1.legend(
            handles,
            labels,
            loc="lower left",
            bbox_to_anchor=(1, 0),
            title="Knowledge Level",
        )
        ax1.yaxis.set_major_formatter(mtick.PercentFormatter())

        ax2 = plot_interest[i].plot(
            kind="bar",
            ylabel="Votes",
            legend=False,
            ax=axes[0],
            title="Interest",
            color="#989898",
        )
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        fig.tight_layout()
        title = f"plots/{topic}.pdf"
        # fig.savefig(title, dpi=600, bbox_inches="tight")
        fig.savefig(title, format="pdf", dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates plots from excel file for Go Outdoors"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        dest="csv_file",
        help="csv file to create plots from",
        required=True,
    )
    args = parser.parse_args()
    main()
