import requests

# Test URLs
url_gif_exists = 'http://example.com/images/existing_image.gif'
url_mp4_exists = 'http://example.com/images/video.gif'
url_s3_fallback = 'http://example.com/images/not_found.gif'

def test_nginx_gif_redirect():
    """
    Tests if NGINX correctly redirects a .gif file to a .mp4.
    """
    print(f"Testing URL: {url_mp4_exists}")
    try:
        response = requests.get(url_mp4_exists, allow_redirects=False, timeout=5)

        # Check for 301/302 redirect
        if response.status_code == 301 or response.status_code == 302:
            print("✅ Redirect status code is correct.")

            # Check for the correct Location header
            location_header = response.headers.get('Location')
            expected_location = url_mp4_exists.replace('.gif', '.mp4')
            if location_header == expected_location:
                print(f"✅ Location header is correct: {location_header}")

                # Follow the redirect to verify the final file exists
                final_response = requests.get(location_header, timeout=5)
                if final_response.status_code == 200:
                    print("✅ Final file was successfully served.")
                else:
                    print(f"❌ Final file response failed with status code: {final_response.status_code}")

            else:
                print(f"❌ Location header is incorrect. Expected: {expected_location}, Got: {location_header}")
        elif response.status_code == 200:
            print("❌ Redirect did not happen. Expected 301/302, got 200.")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    test_nginx_gif_redirect()