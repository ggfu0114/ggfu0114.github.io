#!/usr/bin/python

import markdown
import sys
import os
import pathlib
from datetime import datetime
from pathlib import Path

TEMPLATE = """
<head>
<title>%s</title>
<meta charset="utf-8" />
<meta name="description" content="%s" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="GGFU" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css" integrity="sha512-Oy18vBnbSJkXTndr2n6lDMO5NN31UljR8e/ICzVPrGpSud4Gkckb8yUpqhKuUNoE+o9gAb4O/rAxxw1ojyUVzg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.7.0/styles/github-gist.min.css" integrity="sha256-tAflq+ymku3Khs+I/WcAneIlafYgDiOQ9stIHH985Wo=" crossorigin="anonymous" />
<link rel="stylesheet" href="https://ggfu0114.github.io/css/code_block.css"/>
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
<article class="markdown-body">
	%s
</article>
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
import glob

FILE_FD_PATH = pathlib.Path(__file__).parent.resolve()
PROJECT_ROOT_FD = os.path.join(FILE_FD_PATH, '..')
POST_HTML_FD = os.path.join(PROJECT_ROOT_FD, 'post')
HOST_POST_URL = 'https://ggfu0114.github.io/post'
def _walk_all_html(fd: str):
    # for root, dirs, files in os.walk(fd):

    #     for file in files:
    #         if file.endswith(".html"):
    #             print(dirs)
    #             print(os.path.join(file))
    sub_paths = []
    for file_path in glob.glob(f'{fd}/*/*.html'):

        sub_path = file_path.replace(POST_HTML_FD, '')
        sub_paths.append(sub_path)
        print(sub_path)
    return sub_paths

paths = _walk_all_html(POST_HTML_FD)

from lxml import etree
def _generate_sitemap_xml(sub_paths: list)->str:
    # create XML 
    urlset = etree.Element('urlset')
    urlset.attrib['xmlns']= 'http://www.sitemaps.org/schemas/sitemap/0.9'
    
    for sub_path in sub_paths:
        # another child with text
        child_url = etree.Element('url')
        loc = etree.Element('loc')
        loc.text = f'{HOST_POST_URL}{sub_path}'
        child_url.append(loc)
        lastmod = etree.Element('lastmod')
        lastmod.text = '2021-07-03'
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
    return xml_string
res = _generate_sitemap_xml(paths)
print(res)






def main():
    src = sys.argv[1]
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
    print(file_fd_path)
    md_year = str(datetime.strptime(
        markdown_md.get('date')[0], '%d/%m/%Y').year)
    print(f'file_fd_path＝{file_fd_path}')
    file_fd = os.path.join(file_fd_path, '..', 'post', md_year)
    file_path = os.path.join(file_fd, f'{file_name}.html')

    if not os.path.exists(file_fd):
        os.makedirs(file_fd)

    with open(file_path, 'w') as f:
        html_title = ''.join(markdown_md.get('title'))
        html_description = ''.join(markdown_md.get('description'))

        whole_html = TEMPLATE % (html_title, html_description, html)
        f.write(whole_html)


if __name__ == '__main__':
    main()
