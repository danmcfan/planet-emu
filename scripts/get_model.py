import pandas as pd
import numpy as np
import click
import os

from planet_emu import util, predict


@click.command()
@click.option(
    "-ls",
    "--loss",
    show_default=True,
    default="mean_absolute_percentage_error",
    help="Loss function for model",
)
@click.option(
    "-lr",
    "--learning_rate",
    show_default=True,
    default=0.001,
    help="Learning rate of the model",
)
@click.option(
    "-e",
    "--epochs",
    show_default=True,
    default=100,
    help="Number of epochs to train",
)
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    show_default=True,
    default=False,
    help="Overwrite existing model",
)
def main(
    loss: str,
    learning_rate: float,
    epochs: int,
    overwrite: bool,
) -> None:
    dataset = pd.read_csv("data/csv/features.csv")
    dataset = dataset.drop(columns=["fips_code"])

    train_dataset, test_dataset = predict.split_dataset(dataset)
    train_features, train_labels = predict.split_features(train_dataset, "ndvi")
    test_features, test_labels = predict.split_features(test_dataset, "ndvi")

    if os.path.exists("data/model/linear/assets") and not overwrite:
        linear_model = predict.load_model("data/model/linear")
    else:
        linear_model, hist = predict.get_model(
            train_features,
            train_labels,
            loss=loss,
            learning_rate=learning_rate,
            epochs=epochs,
            linear=True,
        )
        util.to_csv(hist, "linear_model_history")
        linear_model.save("data/model/linear")

    linear_features = test_features.copy()
    linear_features["ndvi_prediction"] = linear_model.predict(linear_features).flatten()
    linear_features["ndvi_real"] = test_labels
    linear_features = linear_features.loc[:, ["ndvi_prediction", "ndvi_real"]]
    util.to_csv(linear_features, "linear_model_predictions")

    evaluation = predict.get_evaluation(linear_model, test_features, test_labels)
    print("Linear Model - Mean Absolute Percent Error:", evaluation)

    feature_names = train_features.columns
    feature_weights = np.array(linear_model.layers[1].kernel)

    weights_df = pd.DataFrame(
        {name: weight for name, weight in zip(feature_names, feature_weights)}
    ).T.reset_index()
    weights_df.columns = ["feature", "weight"]
    weights_df["weight_abs"] = abs(weights_df["weight"])
    weights_df["effect"] = weights_df["weight"].apply(
        lambda x: "pos" if x > 0 else "neg"
    )
    weights_df = weights_df.sort_values("weight_abs", ascending=False)
    util.to_csv(weights_df, "linear_model_weights")

    if os.path.exists("data/model/dnn/assets") and not overwrite:
        dnn_model = predict.load_model("data/model/dnn")
    else:
        dnn_model, hist = predict.get_model(
            train_features,
            train_labels,
            loss=loss,
            learning_rate=learning_rate,
            epochs=epochs,
            linear=False,
        )
        util.to_csv(hist, "dnn_model_history")
        dnn_model.save("data/model/dnn")

    dnn_features = test_features.copy()
    dnn_features["ndvi_prediction"] = dnn_model.predict(dnn_features).flatten()
    dnn_features["ndvi_real"] = test_labels
    dnn_features = dnn_features.loc[:, ["ndvi_prediction", "ndvi_real"]]
    util.to_csv(dnn_features, "dnn_model_predictions")

    evaluation = predict.get_evaluation(dnn_model, test_features, test_labels)
    print("Deep Nueral Network Model - Mean Absolute Percent Error:", evaluation)


if __name__ == "__main__":
    main()
