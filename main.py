import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).with_name("songs.csv")

def load_catalogue():
    """Load the music catalogue from CSV."""
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print("Error: songs.csv was not found.")
        return pd.DataFrame()

def show_songs(data):
    if data.empty:
        print("\nNo songs found.")
        return
    view = data[["track_name", "artist", "genre", "album_name", "release_year"]]
    print("\n" + view.to_string(index=False))

def show_genres(data):
    print("\n========== MUSIC GENRES ==========")
    for genre, count in data["genre"].value_counts().items():
        print(f"{genre:<20} {count} songs")

def browse_genre(data):
    genres = sorted(data["genre"].dropna().unique())
    print("\nAvailable genres:")
    for number, genre in enumerate(genres, start=1):
        print(f"{number}. {genre}")

    choice = input("\nEnter genre name (or number): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(genres):
        selected = genres[int(choice) - 1]
    else:
        matches = [g for g in genres if g.lower() == choice.lower()]
        if not matches:
            print("Genre not found.")
            return
        selected = matches[0]

    print(f"\n========== {selected.upper()} ==========")
    show_songs(data[data["genre"] == selected])

def search_songs(data):
    query = input("\nSearch by song, artist or album: ").strip().lower()
    if not query:
        print("Please enter a search term.")
        return
    mask = (
        data["track_name"].astype(str).str.lower().str.contains(query, na=False)
        | data["artist"].astype(str).str.lower().str.contains(query, na=False)
        | data["album_name"].astype(str).str.lower().str.contains(query, na=False)
    )
    print(f"\nSearch results for '{query}':")
    show_songs(data[mask])

def top_songs(data):
    count = data.sort_values("number_of_streams", ascending=False).head(10)
    print("\n========== TOP 10 BY STREAMS ==========")
    print(count[["track_name", "artist", "genre", "number_of_streams"]].to_string(index=False))

def artist_songs(data):
    artist = input("\nEnter artist name: ").strip().lower()
    result = data[data["artist"].astype(str).str.lower().str.contains(artist, na=False)]
    if result.empty:
        print("Artist not found.")
    else:
        print(f"\nSongs by {artist.title()}:")
        show_songs(result)

def add_song(data):
    print("\n========== ADD A NEW SONG ==========")
    new_song = {
        "genre": input("Genre: ").strip(),
        "artist": input("Artist: ").strip(),
        "track_name": input("Song name: ").strip(),
        "album_name": input("Album name: ").strip(),
        "release_year": input("Release year: ").strip(),
        "album_type": input("Album type (Single/Album/EP/Live): ").strip(),
        "bpm": input("BPM: ").strip(),
        "number_of_streams": input("Number of streams: ").strip() or "0",
        "song_length_min": input("Song length (e.g. 3:45): ").strip(),
        "avg_percent_song_played": input("Average played percentage (0-100): ").strip() or "0"
    }

    if not new_song["genre"] or not new_song["artist"] or not new_song["track_name"]:
        print("Genre, artist and song name are required. Song not added.")
        return data

    try:
        new_song["release_year"] = int(new_song["release_year"])
        new_song["bpm"] = float(new_song["bpm"] or 0)
        new_song["number_of_streams"] = int(new_song["number_of_streams"])
        new_song["avg_percent_song_played"] = float(new_song["avg_percent_song_played"])
    except ValueError:
        print("Year, BPM, streams and percentage must be numbers. Song not added.")
        return data

    updated = pd.concat([data, pd.DataFrame([new_song])], ignore_index=True)
    updated.to_csv(DATA_FILE, index=False)
    print("Song added successfully!")
    return updated

def main():
    catalogue = load_catalogue()
    if catalogue.empty:
        print("Catalogue is empty. Add songs to songs.csv first.")
        return

    while True:
        print("""
========================================
          SPOTIFY MUSIC CATALOGUE
========================================
1. View all songs
2. Browse music genres
3. Search a song / album
4. View songs by an artist
5. Top 10 songs by streams
6. Show genre summary
7. Add a new song
0. Exit
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_songs(catalogue)
        elif choice == "2":
            browse_genre(catalogue)
        elif choice == "3":
            search_songs(catalogue)
        elif choice == "4":
            artist_songs(catalogue)
        elif choice == "5":
            top_songs(catalogue)
        elif choice == "6":
            show_genres(catalogue)
        elif choice == "7":
            catalogue = add_song(catalogue)
        elif choice == "0":
            print("\nThanks for using Spotify Music Catalogue!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
