import pandas as pd
import numpy as np
from scipy.optimize import minimize_scalar

from sklearn.cluster import KMeans
from blackjack.computer_vision.utils import timeit


@timeit
def cluster_one_player(card_predictions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clusters cards of dealer and player for simple case with only one player.
    Note(!): requires dealers cards to be on top of image!
    """

    # prepare data
    X = card_predictions_df[["x", "y"]]

    # run kmeans clustering with 2 clusters (Dealer & Player)
    km = KMeans(n_clusters=2)
    km.fit(X)
    card_predictions_df["cluster"] = km.labels_  # save predicted cluster to original df
    # decide which cluster is the dealer cluster and which the players
    # by looking which clister has lowest mean y coord, i.e. is at top in image
    mean_vertical_position_by_cluster = (
        card_predictions_df.groupby("cluster")[["y"]]
        .mean()
        .sort_values("y")
        .reset_index()
    )

    dealer_cluster = mean_vertical_position_by_cluster.iloc[0, 0]  # lowest mean y
    player_cluster = mean_vertical_position_by_cluster.iloc[1, 0]  # highest mean y

    # clean df and rename clusters
    # clean_pred_df = card_predictions_df.drop_duplicates(subset="class")[["class", "cluster"]]
    # clean_pred_df["cluster"] = clean_pred_df["cluster"].replace({dealer_cluster: "dealer", player_cluster: "player"})
    # clean_pred_df["class"] = clean_pred_df["class"].apply(lambda x: x[:-1])
    card_predictions_df["cluster"] = card_predictions_df["cluster"].replace(
        {dealer_cluster: "dealer", player_cluster: "player"}
    )

    # create a results dict, containing all cards
    card_predictions_dict = card_predictions_df.to_dict("records")

    print("✅ clustered predictions for one player")

    return card_predictions_dict


@timeit
def cluster_one_player_advanced(card_predictions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clusters cards of dealer and player for simple case with only one player.
    Note(!): requires dealers cards to be on top of image!
    """

    # if no card was recognized return none
    if card_predictions_df is None:
        return None

    # get y coordinates of each pred, scale, create loss function for optimal horizontal line
    y_scal = card_predictions_df["y"] / 1000
    loss_function = lambda x: np.sum([np.abs(x - y) ** 3 for y in y_scal])

    # minimise loss function undo scaling, save y threshold
    result = minimize_scalar(
        loss_function, bounds=(np.min(y_scal), np.max(y_scal)), method="bounded"
    )
    y_threshold = round(result.x * 1000)

    # save clustering for each card based on y_thres
    card_predictions_df["cluster"] = card_predictions_df["y"].apply(
        lambda y: "dealer" if y < y_threshold else "player"
    )

    # clean cols, clean duplicate rows
    card_predictions_df.drop(columns=["image_path", "prediction_type"], inplace=True)
    by_corners_dict = card_predictions_df.to_dict("records")

    # calculate person based dicts
    by_person_dict = (
        card_predictions_df.groupby("cluster")["class"]
        .apply(lambda x: list(set(x)))
        .to_dict()
    )

    print("✅ clustered predictions for one player")

    return {"by_corner": by_corners_dict, "by_person": by_person_dict}
