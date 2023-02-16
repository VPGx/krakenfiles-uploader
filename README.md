# krakenfiles-uploader
Usage: krakenfiles.py (file to be uploaded)

The purpose of this is to create an uploader for usage with the newly documented KrakenFiles API.

The script starts by making the inital request to KrakenFiles in order to find the most available / less used upload server, aswell as the unique serverAccessToken for each upload.

After it recieves the Upload URL and the serverAccessToken, it uses that information to upload the file given when the script was initally run.
