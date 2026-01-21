#!/usr/bin/env python3
"""
Vimeo Live Events Creator
Reads event data from a CSV file and creates live events via the Vimeo API.
Returns stream URL, embed code, and stream key for each event.
"""

import csv
import json
import os
import sys

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

VIMEO_API_BASE = "https://api.vimeo.com"


def get_access_token():
    """Get Vimeo access token from environment variable."""
    token = os.getenv("VIMEO_ACCESS_TOKEN")
    if not token:
        print("Error: VIMEO_ACCESS_TOKEN not found in environment variables.")
        print("Please create a .env file with your Vimeo access token.")
        print("See .env.example for the required format.")
        sys.exit(1)
    return token


def create_live_event(token, title, description=""):
    """
    Create a live event on Vimeo.

    Args:
        token: Vimeo API access token
        title: Event title
        description: Event description (optional)

    Returns:
        dict with event details including stream URL, embed code, and stream key
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.vimeo.*+json;version=3.4"
    }

    # Build the request payload
    payload = {
        "title": title,
        "stream_title": title,
        "type": "recurring",
        "privacy": {
            "view": "anybody",
            "embed": "public"
        },
        "embed": {
            "playbar": True,
            "volume": True,
            "fullscreen_button": True,
            "color": "#00adef"
        }
    }

    if description:
        payload["description"] = description

    # Create the live event
    response = requests.post(
        f"{VIMEO_API_BASE}/me/live_events",
        headers=headers,
        json=payload
    )

    if response.status_code not in [200, 201]:
        print(f"Error creating event '{title}': {response.status_code}")
        print(f"Response: {response.text}")
        return None

    event_data = response.json()

    # Extract relevant information
    event_uri = event_data.get("uri", "")
    event_id = event_uri.split("/")[-1] if event_uri else ""

    # Get streaming configuration (API uses rtmp_link/rtmps_link)
    stream_url = event_data.get("rtmps_link") or event_data.get("rtmp_link", "")
    stream_key = event_data.get("stream_key", "")

    # Get embed code
    embed_html = ""
    if "embed" in event_data and "html" in event_data["embed"]:
        embed_html = event_data["embed"]["html"]
    elif "player_embed_url" in event_data:
        player_url = event_data["player_embed_url"]
        embed_html = f'<iframe src="{player_url}" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>'

    # Construct player URL if not available
    player_url = event_data.get("player_embed_url", "")
    if not player_url and event_id:
        player_url = f"https://player.vimeo.com/video/{event_id}"

    return {
        "event_id": event_id,
        "title": title,
        "stream_url": stream_url,
        "stream_key": stream_key,
        "embed_code": embed_html,
        "player_url": player_url,
        "link": event_data.get("link", "")
    }


def read_csv_events(csv_path):
    """
    Read events from a CSV file.

    Expected columns: title, description
    """
    events = []

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Validate required columns
        if "title" not in reader.fieldnames:
            print("Error: CSV must have a 'title' column")
            sys.exit(1)

        for row in reader:
            event = {
                "title": row.get("title", "").strip(),
                "description": row.get("description", "").strip()
            }

            if event["title"]:
                events.append(event)

    return events


def save_results(results, output_path="output/event_results.json"):
    """Save the results to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")


def print_event_details(event_result):
    """Print formatted event details."""
    print("\n" + "=" * 60)
    print(f"Event: {event_result['title']}")
    print("=" * 60)
    print(f"Event ID:    {event_result['event_id']}")
    print(f"Stream URL:  {event_result['stream_url']}")
    print(f"Stream Key:  {event_result['stream_key']}")
    print(f"Player URL:  {event_result['player_url']}")
    print(f"Event Link:  {event_result['link']}")
    print(f"\nEmbed Code:")
    print(event_result['embed_code'])
    print("=" * 60)


def main():
    """Main function to create Vimeo live events from CSV."""
    # Check command line arguments
    if len(sys.argv) < 2:
        csv_path = "events_sample.csv"
        print(f"No CSV file specified. Using default: {csv_path}")
    else:
        csv_path = sys.argv[1]

    print(f"Reading events from: {csv_path}")

    # Get access token
    token = get_access_token()

    # Read events from CSV
    events = read_csv_events(csv_path)
    print(f"Found {len(events)} event(s) to create")

    if not events:
        print("No events to create. Exiting.")
        return

    # Create events and collect results
    results = []
    successful = 0
    failed = 0

    for event in events:
        print(f"\nCreating event: {event['title']}...")

        result = create_live_event(
            token=token,
            title=event["title"],
            description=event["description"]
        )

        if result:
            results.append(result)
            print_event_details(result)
            successful += 1
        else:
            failed += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total events processed: {len(events)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    # Save results to JSON
    if results:
        save_results(results)

    return results


if __name__ == "__main__":
    main()
