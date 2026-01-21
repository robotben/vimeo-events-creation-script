VIMEO LIVE EVENTS CREATION SCRIPT
==================================

Creates Vimeo live events from CSV data and returns streaming details.


SETUP
-----
1. Install dependencies:
   pip install -r requirements.txt

2. Create .env file with your Vimeo API token:
   VIMEO_ACCESS_TOKEN=your_token_here

   Get your token at: https://developer.vimeo.com/apps
   Required scopes: create, edit, public


USAGE
-----
python create_vimeo_events.py                  # Uses events_sample.csv
python create_vimeo_events.py your_file.csv   # Uses custom CSV


CSV FORMAT
----------
Required columns:
- title: Event name

Optional columns:
- description: Event description

Example:
  title,description
  My Live Event,This is a test stream
  Another Event,Second event description


OUTPUT
------
For each event created, the script displays:
- Event ID
- Stream URL (RTMPS endpoint)
- Stream Key
- Player URL
- Event Link
- Embed Code (iframe HTML)

Results are also saved to: output/event_results.json


FILES
-----
create_vimeo_events.py  - Main script
events_sample.csv       - Example CSV template
.env                    - Your API token (keep private)
.env.example            - Template for .env file
requirements.txt        - Python dependencies
.gitignore              - Prevents .env from being committed


API DETAILS
-----------
Endpoint:
  POST https://api.vimeo.com/me/live_events

Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json
  Accept: application/vnd.vimeo.*+json;version=3.4

Request Payload:
  {
    "title": "Event title",
    "stream_title": "Event title",
    "type": "recurring",
    "privacy": {
      "view": "anybody",
      "embed": "public"
    },
    "embed": {
      "playbar": true,
      "volume": true,
      "fullscreen_button": true,
      "color": "#00adef"
    },
    "description": "Optional description"
  }

Key Response Fields:
  uri              - Event URI (e.g., /live_events/1234567)
  rtmps_link       - Secure RTMP streaming endpoint
  rtmp_link        - Standard RTMP streaming endpoint
  stream_key       - Unique key for this event's stream
  embed.html       - Ready-to-use iframe embed code

Type Options:
  "recurring"      - Reusable event; stream key persists across sessions
                     If encoder disconnects, viewers wait for reconnection

Privacy Options:
  view: "anybody"  - Public viewing
  view: "nobody"   - Private
  view: "password" - Password protected
  embed: "public"  - Embeddable anywhere
  embed: "private" - Embed only on whitelisted domains


NOTES
-----
- Events are created as "recurring" type (reusable stream key)
- Privacy is set to public view and embed by default
- Stream URL is the same for all events; stream key is unique per event
