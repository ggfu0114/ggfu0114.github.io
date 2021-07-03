#!/usr/bin/python

import markdown
import sys

TEMPLATE = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css" integrity="sha512-Oy18vBnbSJkXTndr2n6lDMO5NN31UljR8e/ICzVPrGpSud4Gkckb8yUpqhKuUNoE+o9gAb4O/rAxxw1ojyUVzg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.7.0/styles/github-gist.min.css" integrity="sha256-tAflq+ymku3Khs+I/WcAneIlafYgDiOQ9stIHH985Wo=" crossorigin="anonymous" />
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
def main():
    src = sys.argv[1]
    dst = sys.argv[2]
    md_file = open(src, 'r').read()
    extensions = ['tables','nl2br','fenced_code','footnotes', 'toc','wikilinks','sane_lists','codehilite','def_list','attr_list','extra']
    html = markdown.markdown(md_file.decode('utf-8'), extensions=extensions)
    with open(dst, 'w') as f:
        whole_html = TEMPLATE % html.encode('utf-8')
        f.write(whole_html)

if __name__ == '__main__':
    main()