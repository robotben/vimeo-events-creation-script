VIMEO LIVE EVENTS CREATION SCRIPT
==================================

Creates Vimeo live events from CSV data and returns streaming details.


PREREQUISITES
-------------
- Python 3.7 or higher
- A Vimeo account with Live streaming access
- A Vimeo API access token


STEP-BY-STEP SETUP
------------------

1. INSTALL PYTHON (if not already installed)
   - Download Python from: https://www.python.org/downloads/
   - During installation, CHECK the box "Add Python to PATH"
   - To verify installation, open Command Prompt and type:
       python --version
     You should see something like "Python 3.11.0"

2. DOWNLOAD THIS SCRIPT
   - Download or clone this repository to your computer
   - Note the folder location (e.g., C:\Users\YourName\vimeo-script)

3. OPEN COMMAND PROMPT
   - Press Windows+R, type "cmd", press Enter
   - Navigate to the script folder:
       cd C:\Users\YourName\vimeo-script
     (Replace with your actual folder path)

4. INSTALL REQUIRED PACKAGES
   - In Command Prompt, run:
       pip install -r requirements.txt
   - This installs the necessary Python libraries

5. GET YOUR VIMEO API TOKEN
   - Go to: https://developer.vimeo.com/apps
   - Click "Create App" (or select existing app)
   - Go to the "Authentication" tab
   - Generate a new Access Token with these scopes:
       - create
       - edit
       - public
   - Copy the token (you'll only see it once!)

6. CREATE YOUR .env FILE
   - In the script folder, create a new file named exactly:  .env
   - Open it with Notepad and add this line:
       VIMEO_ACCESS_TOKEN=paste_your_token_here
   - Save and close the file
   - IMPORTANT: Never share this file or commit it to GitHub

7. CREATE YOUR CSV FILE
   - Open events_sample.csv in Excel or a text editor
   - Replace the sample data with your event details
   - Save the file (keep it as CSV format)


RUNNING THE SCRIPT
------------------
1. Open Command Prompt
2. Navigate to the script folder:
     cd C:\Users\YourName\vimeo-script
3. Run the script:
     python create_vimeo_events.py

   Or specify a custom CSV file:
     python create_vimeo_events.py my_events.csv

4. The script will display results for each event created
5. Results are also saved to: output/event_results.json


TROUBLESHOOTING
---------------
"python is not recognized..."
  - Python wasn't added to PATH during installation
  - Reinstall Python and check "Add Python to PATH"

"No module named requests..."
  - Run: pip install -r requirements.txt

"VIMEO_ACCESS_TOKEN not found..."
  - Make sure .env file exists in the script folder
  - Make sure the file is named exactly ".env" (not ".env.txt")

"403 Forbidden" or "create scope" error
  - Your API token doesn't have the right permissions
  - Generate a new token with create, edit, public scopes


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
