import itertools
import json
import os

import praw

USERNAME = '_9MOTHER9HORSE9EYES9'

# Follow API guidelines: https://github.com/reddit/reddit/wiki/API#rules
USER_AGENT = '9m9h9e9 e-book script:v0.2 (by /u/cryzed-)'
SPINE_PATH = os.path.join('parts', 'spine.json')


def main():
    client = praw.Reddit(user_agent=USER_AGENT)
    redditor = client.get_redditor(USERNAME)
    parts = {}

    print('- Scraping parts...')
    for thing in itertools.chain(redditor.get_comments(limit=None), redditor.get_submitted(limit=None)):
        html = getattr(thing, 'body_html', getattr(thing, 'selftext_html', None))
        if not html:
            print('- Skipping %s: no content' % thing.permalink)
            continue

        text = getattr(thing, 'body', getattr(thing, 'selftext', None))
        if text == '[removed]':
            print('- Skipping %s: removed' % thing.permalink)
            continue

        print('- Adding: %s...' % thing.id)
        parts[thing.id] = (thing.created, html, text)

    if os.path.exists(SPINE_PATH):
        with open(SPINE_PATH) as file:
            spine = json.load(file)
    else:
        spine = {}

    print('- Saving parts...')
    for id_, (created, html, text) in parts.items():
        with open(os.path.join('parts', id_ + '.html'), 'w', encoding='UTF-8') as file:
            file.write(html)
        with open(os.path.join('parts', id_ + '.txt'), 'w', encoding='UTF-8') as file:
            file.write(text)

        spine[id_] = created

    print('- Saving spine...')
    with open(SPINE_PATH, 'w') as file:
        json.dump(spine, file)

    print('Finished!')


if __name__ == '__main__':
    main()
