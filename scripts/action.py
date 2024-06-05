# Dummy function returning fixed response times based on the provided URL. 
# It serves as a basic example to help us understand how the agent can utilize external functions.

def get_response_time(url):
    if url == "learnwithhasan.com":
        return 0.5
    if url == "google.com":
        return 0.3
    if url == "openai.com":
        return 0.4