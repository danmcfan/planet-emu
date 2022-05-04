import pandas as pd
import os

from planet_emu import util, predict


def main(
    loss: str = "mean_absolute_percentage_error",
    learning_rate: int = 0.001,
    epochs: int = 100,
) -> None:
    dataset = pd.read_csv("data/csv/features.csv")
    dataset = dataset.drop(columns=["fips_code"])

    train_dataset, test_dataset = predict.split_dataset(dataset)
    train_features, train_labels = predict.split_features(train_dataset, "ndvi")
    test_features, test_labels = predict.split_features(test_dataset, "ndvi")

    if os.path.exists("data/model/assets"):
        model = predict.load_model("data/model")
    else:
        model, hist = predict.get_model(
            train_features,
            train_labels,
            loss=loss,
            learning_rate=learning_rate,
            epochs=epochs,
        )
        util.to_csv(hist, "model_history")
        model.save("data/model")

    evaluation = predict.get_evaluation(model, test_features, test_labels)
    test_features["ndvi_prediction"] = model.predict(test_features).flatten()
    test_features["ndvi"] = test_labels

    util.to_csv(test_features, "model_predictions")
    print(evaluation)


if __name__ == "__main__":
    main()
