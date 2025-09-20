import requests
import sys

# Test URLs
# 이 URL들을 실제 테스트 환경에 맞게 수정하세요.
# 예: GitHub Actions 환경에서는 localhost를 사용합니다.
# url_mp4_exists = 'http://localhost/images/video.gif'
url_mp4_exists = 'http://example.com/images/video.gif'

def test_nginx_gif_redirect():
    """
    NGINX가 .gif 파일을 .mp4로 올바르게 리디렉션하는지 테스트합니다.
    """
    print(f"Testing URL: {url_mp4_exists}")
    try:
        # allow_redirects=False: 리디렉션 응답을 직접 확인하기 위해 필수
        response = requests.get(url_mp4_exists, allow_redirects=False, timeout=5)

        # 예상하는 리디렉션 상태 코드 확인 (301 또는 302)
        if response.status_code == 301 or response.status_code == 302:
            print("✅ Redirect status code is correct.")

            # Location 헤더가 올바른지 확인
            location_header = response.headers.get('Location')
            # NGINX 설정에 따라 Location 헤더의 포맷을 맞춰야 합니다.
            # 이 예제는 외부 리다이렉션을 가정합니다.
            expected_location = url_mp4_exists.replace('.gif', '.mp4')
            if location_header and location_header == expected_location:
                print(f"✅ Location header is correct: {location_header}")

                # 리디렉션된 최종 URL에 대한 성공적인 응답을 확인
                final_response = requests.get(location_header, timeout=5)
                if final_response.status_code == 200:
                    print("✅ Final file was successfully served.")
                else:
                    print(f"❌ Final file response failed with status code: {final_response.status_code}")
                    sys.exit(1) # 최종 요청 실패 시 스크립트 종료
            else:
                print(f"❌ Location header is incorrect. Expected: {expected_location}, Got: {location_header}")
                sys.exit(1) # Location 헤더 불일치 시 스크립트 종료
        else:
            print(f"❌ Unexpected status code: {response.status_code}. Expected 301 or 302.")
            sys.exit(1) # 예상치 못한 상태 코드 시 스크립트 종료

    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1) # 요청 실패 시 스크립트 종료

if __name__ == "__main__":
    test_nginx_gif_redirect()