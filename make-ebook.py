import html
import json
import operator
import os
import textwrap

from ebooklib import epub

SPINE_PATH = os.path.join('parts', 'spine.json')
AUTHOR = '_9MOTHER9HORSE9EYES9'
TITLE = 'The Interface Series'
LANGUAGE = 'en'

# There's no real rhyme or reason to this, I just tried to find a value which looks good on my e-book reader
MAX_TITLE_LENGTH = 56


def main():
    print('- Loading spine...')
    with open(SPINE_PATH) as file:
        spine = json.load(file)

    book = epub.EpubBook()
    book.set_title(TITLE)
    book.add_author(AUTHOR)
    book.set_language(LANGUAGE)

    print('- Loading parts...')
    chapters = []
    for id_, created in sorted(spine.items(), key=operator.itemgetter(1)):
        with open(os.path.join('parts', id_ + '.html')) as file:
            html_content = file.read()
        with open(os.path.join('parts', id_ + '.txt')) as file:
            text = file.read()

        file_name = id_ + '.xhtml'
        chapter = epub.EpubHtml(file_name=file_name)
        chapter.content = html_content
        book.add_item(chapter)
        chapters.append(chapter)

        # Have to unescape HTML entities in the text content
        title = textwrap.shorten(html.unescape(text), MAX_TITLE_LENGTH, placeholder='...')
        book.toc.append(epub.Link(file_name, title, id_))

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', *chapters]

    file_name = '%s #%d.epub' % (book.title, len(chapters))
    print('- Saving: %s...' % file_name)
    epub.write_epub(file_name, book)
    print('Finished!')


if __name__ == '__main__':
    main()
