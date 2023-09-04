Basic Instructions:

# If you want to scrape band setlists first:
Go to setlist.fm and visit the main page for each band you want to get the setlists from
Paste each band's page URL onto its own line in band_pages.txt
Run Scraper/scraper_main.py (It will take a while, close to 10 minutes per band -- This is so we don't flood Setlist.fm with requests)
If successful, the script will write the output to output.json.

The output json will have the bands in the order they are listed in band_pages.txt with the inner dictionaries being each song sorted by the number of times it was found in a concert setlist.

# If you already have band data or after you have scraped Setlist.fm
Load the band data into band_data.json -- The data must be in the follow format:

{
BandOne: {
    Song1: 1,
    Song2: 5,
    Song3: 6
    },
BandTwo: {
    Song1: 3,
    Song2: 5,
    Song3: 1
    }
}

In the config.json, enter your playlist's title, your spotify client secret, spotify client ID, and spotify redirect URI.
You can find those by creating a new "App" in the spotify developer portal and copying the values it gives you:
https://developer.spotify.com/dashboard/create

Note that when creating your app, spotify will ask you for a redirect URI. This can be anything, but whatever you enter as the redirect URI must match what you set in the config.json.

Once all of this is set up, run playlist_main.py and a web browser page should open to the redirect URI along with a bunch of other information. Paste the whole URL into your terminal window and the script will be authorized to read and write to your playlists. 

From there simply wait for the playlists to be created.

If you would like a separate playlist to be created for each band in addition to the single playlist with all bands, run the script with the --singleband argument.


If you do not load band data in band_data.json, the script will prompt you to give it a band name followed by a comma separated list of songs, then will create a playlist with those songs.