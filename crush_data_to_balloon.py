import pandas as pd

def main():

    IN_FPATH = "./test/sbart_balloon_features.csv"
    FTRIAL_FPATH = "./test/FirstTrial.csv"
    OUT_FPATH = "./test/sbart_balloon_features_reduced.csv"

    df = pd.read_csv(IN_FPATH)
    ftrial_df = pd.read_csv(FTRIAL_FPATH)
    ftrial_df["id"] = ftrial_df["Participant"]

    df = pd.merge(df, ftrial_df, on="id")

    df_no_beginning_pump = df[df["onset_from_balloon_start"] != 0]
    df_just_beginning_pump = df.groupby(["id", "balloon_number"]).head(1)

    x = df_no_beginning_pump.groupby(["id", "balloon_number"])["pump_event_duration"].mean().tolist()
    y = df_no_beginning_pump.groupby(["id", "balloon_number"])["pump_event_pumps"].mean().tolist()

    # print(x.shape)
    # print(y.shape)
    # print(df_just_beginning_pump.shape)

    df_just_beginning_pump["avg_pump_event_duration"] = x
    df_just_beginning_pump["avg_pumps_per_pump_event"] = y

    df_just_beginning_pump["time_until_first_pump"] = df["pump_event_duration"]
    df_just_beginning_pump.drop(["pump_event_number", "pump_event_duration"], axis=1, inplace=True)

    df_just_beginning_pump.to_csv(OUT_FPATH)










if __name__ == "__main__":
    main()
