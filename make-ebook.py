import html
import json
import operator
import os
import textwrap

from ebooklib import epub

SPINE_PATH = os.path.join('parts', 'spine.json')
AUTHOR = '_9MOTHER9HORSE9EYES9'
MAX_TITLE_LENGTH = 64


def main():
    print('- Loading spine...')
    with open(SPINE_PATH) as file:
        spine = json.load(file)

    book = epub.EpubBook()
    book.set_title('The Interface Series')
    book.add_author(AUTHOR)
    book.set_language('en')
    book.toc = []

    print('- Loading parts...')
    sorted_spine = sorted(spine.items(), key=operator.itemgetter(1))
    for index, (id_, created) in enumerate(sorted_spine, start=1):
        file_name = id_ + '.xhtml'
        chapter = epub.EpubHtml(file_name=file_name)

        with open(os.path.join('parts', id_ + '.html')) as file:
            html_content = file.read()

        with open(os.path.join('parts', id_ + '.txt')) as file:
            text = file.read()

        chapter.content = html_content
        book.add_item(chapter)

        # Have to unescape HTML entities in the text content
        title = textwrap.shorten(html.unescape(text), MAX_TITLE_LENGTH, placeholder='...')
        book.toc.append(epub.Link(file_name, title, id_))

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', *book.items]

    file_name = '%s - %d.epub' % (book.title, len(spine))
    print('- Saving: %s...' % file_name)
    epub.write_epub(file_name, book)


if __name__ == '__main__':
    main()
