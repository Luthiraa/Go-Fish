from collections import Counter

def match_keywords_to_services(keywords, additional_keywords):
    services = {
        'github': [
            'repository', 'commit', 'pull request', 'issue', 'code', 'branch', 'merge', 'fork', 'clone', 'release', 
            'tag', 'gist', 'contributor', 'collaborator', 'webhook', 'actions', 'workflow', 'milestone', 'label'
        ],
        'slack': [
            'channel', 'message', 'workspace', 'bot', 'integration', 'thread', 'mention', 'reaction', 'emoji', 
            'direct message', 'group', 'call', 'video', 'file', 'upload', 'notification', 'status', 'away', 'online'
        ],
        'stack overflow': [
            'question', 'answer', 'tag', 'vote', 'reputation', 'comment', 'badge', 'profile', 'edit', 'flag', 
            'close', 'duplicate', 'accepted', 'bounty', 'view', 'upvote', 'downvote', 'favorite', 'bookmark'
        ],
        'reddit': [
            'subreddit', 'post', 'comment', 'upvote', 'downvote', 'karma', 'award', 'flair', 'thread', 'mod', 
            'moderator', 'spoiler', 'crosspost', 'link', 'image', 'video', 'poll', 'discussion'
        ]
    }
    
    keyword_counter = Counter(keywords)
    service_scores = {service: 0 for service in services}

    for service, service_keywords in services.items():
        for keyword in service_keywords:
            if keyword in keyword_counter:
                service_scores[service] += keyword_counter[keyword]
        for keyword in additional_keywords.get(service, []):
            if keyword in keyword_counter:
                service_scores[service] += keyword_counter[keyword]

    sorted_services = sorted(service_scores.items(), key=lambda item: item[1], reverse=True)
    matched_services = [service for service, score in sorted_services if score > 0]

    return matched_services

if __name__ == "__main__":
    keywords = ["repository", "commit", "question", "thread", "karma"]
    additional_keywords = {
        'github': ['repo', 'push', 'pull'],
        'slack': ['chat', 'team'],
        'stack overflow': ['query', 'response'],
        'reddit': ['discussion', 'vote']
    }
    matched_services = match_keywords_to_services(keywords, additional_keywords)
    print("Matched Services:", matched_services)