#!/usr/bin/python

import glob
import os
import pathlib
import sys
from datetime import datetime
from pathlib import Path

import markdown
from lxml import etree

TEMPLATE = """
<head>
<title>%s</title>
<meta charset="utf-8" />
<meta name="description" content="%s" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="GGFU" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css" integrity="sha512-Oy18vBnbSJkXTndr2n6lDMO5NN31UljR8e/ICzVPrGpSud4Gkckb8yUpqhKuUNoE+o9gAb4O/rAxxw1ojyUVzg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.7.0/styles/github-gist.min.css" integrity="sha256-tAflq+ymku3Khs+I/WcAneIlafYgDiOQ9stIHH985Wo=" crossorigin="anonymous" />
<link rel="stylesheet" href="https://ggfu0114.github.io/css/code_block.css"/>
<script>
    $(function () {
      $("#includedNavigation").load("../../navigation_header.html");
    });
  </script>
</head>
<style>
	.markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
	}

	@media (max-width: 767px) {
		.markdown-body {
			padding: 15px;
		}
	}
</style>
<body>
<!-- Navigation-->
<div id="includedNavigation"></div>
<article class="markdown-body">
	%s
</article>
</body>
"""


"""Example hackmd meta

Title: AWS IoT介紹
Description: 裝置可以透過 certificates 去做驗證,
      連接上AWS IoT service做系統整合應用
Authors: GGFU
Date: 31/12/2020
Tags: AWS, IoT, policy
base_url: https://ggfu0114.github.io/

"""


FILE_FD_PATH = pathlib.Path(__file__).parent.resolve()
PROJECT_ROOT_FD = os.path.join(FILE_FD_PATH, '..')
POST_HTML_FD = os.path.join(PROJECT_ROOT_FD, 'post')
RAW_MD_FD = os.path.join(PROJECT_ROOT_FD, 'raw_md')
HOST_POST_URL = 'https://ggfu0114.github.io/post'
SITEMAP_FILE_NAME = 'sitemap.xml'


def _walk_files_by_extension(fd: str, extension: str = 'html'):
    sub_paths = set()
    for root, dirs, files in os.walk(fd):
        for file in files:
            if file.endswith(extension):
                full_file_path = os.path.join(root, file)
                sub_path = full_file_path.replace(fd, '')
                sub_paths.add(sub_path)
    return list(sub_paths)


def _generate_sitemap_xml(sub_paths: list) -> None:
    """Create XML sitemap for google search."""

    urlset = etree.Element('urlset')
    urlset.attrib['xmlns'] = 'http://www.sitemaps.org/schemas/sitemap/0.9'

    for sub_path in sub_paths:
        # another child with text
        child_url = etree.Element('url')
        loc = etree.Element('loc')
        loc.text = f'{HOST_POST_URL}{sub_path}'
        child_url.append(loc)
        lastmod = etree.Element('lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
        child_url.append(lastmod)
        changefreq = etree.Element('changefreq')
        changefreq.text = 'weekly'
        child_url.append(changefreq)
        priority = etree.Element('priority')
        priority.text = '0.8'
        child_url.append(priority)

        urlset.append(child_url)

    # pretty string
    xml_string = etree.tostring(urlset, pretty_print=True).decode('utf-8')
    sitemap_file = os.path.join(PROJECT_ROOT_FD, SITEMAP_FILE_NAME)
    with open(sitemap_file, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write(xml_string)


def _md_to_html(src: str) -> str:
    """Convert markdown format to html content."""

    md_text = open(src, 'r').read()
    file_name = os.path.basename(src)
    file_name, extension = os.path.splitext(file_name)
    extensions = ['tables', 'nl2br', 'fenced_code', 'meta',
                  'footnotes', 'toc', 'wikilinks', 'sane_lists',
                  'codehilite', 'def_list', 'attr_list',
                  'extra']
    md = markdown.Markdown(extensions=extensions)
    html = md.convert(md_text)
    markdown_md = md.Meta
    print(f'markdown_md:{markdown_md}')
    file_fd_path = pathlib.Path(__file__).parent.resolve()

    md_year = str(datetime.strptime(
        markdown_md.get('date')[0], '%d/%m/%Y').year)

    file_fd = os.path.join(file_fd_path, '..', 'post', md_year)
    html_file_name = markdown_md.get('id', [file_name])[0]
    file_path = os.path.join(file_fd, f'{html_file_name}.html')

    if not os.path.exists(file_fd):
        os.makedirs(file_fd)

    with open(file_path, 'w') as f:
        html_title = ''.join(markdown_md.get('title'))
        html_description = ''.join(markdown_md.get('description'))
        whole_html = TEMPLATE % (html_title, html_description, html)
        f.write(whole_html)
    return file_path


def main():
    if len(sys.argv) > 1:
        print(f'Covert specific markdown file from markdown to html.')
        src = sys.argv[1]
        _md_to_html(src)
    else:
        print(f'Covert project folders from markdown to html.')
        python_flask_fd = RAW_MD_FD
        print(f' %%{python_flask_fd}')
        paths = _walk_files_by_extension(python_flask_fd, 'md')
        for p in paths:
            full_path = python_flask_fd+p
            print(f' %%{full_path}')
            _md_to_html(full_path)

    paths = _walk_files_by_extension(POST_HTML_FD)
    _ = _generate_sitemap_xml(paths)


if __name__ == '__main__':
    main()
