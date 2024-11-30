import os
import pandas as pd

INPUT_FOLDER = "./input"
OUTPUT_FOLDER = "./output"
USELESS_COLUMNS = [
    "platform",
    "conn_country",
    "ip_addr",
    "episode_name",
    "episode_show_name",
    "spotify_episode_uri",
    "reason_start",
    "reason_end",
    "shuffle",
    "offline",
    "offline_timestamp",
    "incognito_mode"
]
RENAMED_COLUMNS = {
    "ts": "timestamp",
    "ms_played": "duration",
    "master_metadata_track_name": "track_name",
    "master_metadata_album_artist_name": "artist_name",
    "master_metadata_album_album_name": "album_name",
}

def main():
    # Read all json files in the input folder and combine them into a single dataframe
    raw_jsons_dfs = []
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(".json"):
            file_path = os.path.join(INPUT_FOLDER, file_name)
            file_df = pd.read_json(file_path)
            file_df.drop(columns=USELESS_COLUMNS, inplace=True, errors="ignore")
            raw_jsons_dfs.append(file_df)
    combined_df = pd.concat(raw_jsons_dfs, ignore_index=True)

    # Filter out rows with less than 30 seconds of playtime
    mask = (combined_df["ms_played"] > 30000)
    combined_df = combined_df[mask]

    # Rename columns
    combined_df.rename(columns=RENAMED_COLUMNS, inplace=True)

    # Sort by timestamp
    combined_df.sort_values(by="timestamp", inplace=True)

    # Remove duplicates
    combined_df.drop_duplicates(inplace=True)

    # Reset index
    combined_df.reset_index(drop=True, inplace=True)

    # Ensure the output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Save the final dataframe as a json file in the output folder
    combined_df.to_json(os.path.join(OUTPUT_FOLDER, "spotify_data.json"), orient="records", index=False, indent=2)

if __name__ == "__main__":
    main()