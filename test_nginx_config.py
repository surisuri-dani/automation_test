import requests
import sys
import os

TEST_HOST = os.environ.get('TEST_HOST', 'http://localhost')

def test_redirect_to_mp4_if_exists():
    """Tests if a .gif request correctly redirects to a .mp4 if it exists."""
    url = f"{TEST_HOST}/images/video.gif"
    expected_location = f"{TEST_HOST}/images/video.mp4"

    print(f"Testing redirect for existing MP4: {url}")
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)

        if response.status_code == 302:
            print("✅ Status code is 302 Found, as expected.")
            if response.headers.get('Location') == expected_location:
                print("✅ Location header is correct.")
            else:
                print(f"❌ Location header is incorrect. Expected: {expected_location}, Got: {response.headers.get('Location')}")
                sys.exit(1)
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

def test_no_redirect_if_mp4_does_not_exist():
    """Tests that a .gif request does NOT redirect if the .mp4 doesn't exist."""
    url = f"{TEST_HOST}/images/no_mp4.gif"

    print(f"\nTesting no redirect for non-existent MP4: {url}")
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)

        if response.status_code == 200:
            print("✅ Status code is 200 OK, as expected.")
            # Verify the content is the original GIF (optional, but good practice)
            if "This is a GIF that stays" in response.text:
                print("✅ Original GIF content was served.")
            else:
                print("❌ Original GIF content was not served.")
                sys.exit(1)
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_redirect_to_mp4_if_exists()
    test_no_redirect_if_mp4_does_not_exist()
    print("\nAll tests passed successfully.")