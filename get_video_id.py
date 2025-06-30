from urllib.parse import urlparse, parse_qs


def get_youtube_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract query parameters
    query_params = parse_qs(parsed_url.query)
    # Return the 'v' parameter (video id)
    return query_params.get('v', [None])[0]

# Example usage
# url = "https://www.youtube.com/watch?v=8oLi5b4w4PQ&list=RD8oLi5b4w4PQ&index=1"
# video_id = get_youtube_video_id(url)
# print("Video ID:", video_id)
