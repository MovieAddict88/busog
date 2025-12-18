import requests
import json

BASE_URL = "http://localhost:8000/backend/api/rooms"
SONGS_URL = "http://localhost:8000/backend/api/songs.php"

def create_room(room_name, creator_name):
    url = f"{BASE_URL}/create.php"
    payload = {
        "room_name": room_name,
        "creator_name": creator_name,
        "device": "desktop",
        "is_public": 1,
        "max_users": 10
    }
    response = requests.post(url, json=payload)
    return response.json()

def join_room(room_code, user_name):
    url = f"{BASE_URL}/join.php"
    payload = {
        "room_code": room_code,
        "user_name": user_name,
        "device": "desktop"
    }
    response = requests.post(url, json=payload)
    return response.json()

def add_song(room_code, user_name, song_id):
    url = f"{BASE_URL}/update.php"
    payload = {
        "room_code": room_code,
        "user_name": user_name,
        "action": "add_song",
        "song_id": song_id
    }
    response = requests.post(url, json=payload)
    return response.json()

def next_song(room_code, user_name):
    url = f"{BASE_URL}/update.php"
    payload = {
        "room_code": room_code,
        "user_name": user_name,
        "action": "next_song"
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_first_song_id():
    response = requests.get(SONGS_URL)
    data = response.json()
    if data['songs']:
        return data['songs'][0]['id']
    return None

if __name__ == "__main__":
    # 1. Create a room
    room_creator = "Creator"
    room_data = create_room("Test Room", room_creator)
    room_code = room_data.get("room_code")
    if not room_code:
        print("Failed to create room")
        exit()

    # 2. Join the room with another user
    other_user = "Joiner"
    join_room(room_code, other_user)

    # 3. Add a song to the queue by the creator
    song_id = get_first_song_id()
    if not song_id:
        print("No songs found")
        exit()

    add_song(room_code, room_creator, song_id)

    # 4. Attempt to skip the song by the non-owner
    print(f"\\nAttempting to skip song as '{other_user}' (should fail)...")
    skip_by_non_owner = next_song(room_code, other_user)
    print(f"Response: {skip_by_non_owner}")

    # 5. Attempt to skip the song by the owner
    print(f"\\nAttempting to skip song as '{room_creator}' (should succeed)...")
    skip_by_owner = next_song(room_code, room_creator)
    print(f"Response: {skip_by_owner}")
