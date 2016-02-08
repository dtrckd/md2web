#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, random
import pypandoc


'''
 md2web
--- Ultra light, simple and easy website generator based on mardown syntax.

1. get things {tags, pages etc} from markdonws files,
2. generatate HTML:
    * list of tags menu (square tags be inspired by ge-lidt top leadborder...)
    * all tags pages list [sqare by title]
    * unique html from mardowns

# CSS/style Customization.
# Markown enhencement for special HTML and Javascstipt features...

@author: dtrckd (ddtracked@gmail.com)
@license: GPL
'''

_ext = '.md'
_rev = 1
_main = 'index.php'

def get_md(path='.'):
    # Return a the list of markdown files under the @path.

    ext = _ext
    files = []
    for f in os.listdir(path):
        if f.endswith(ext):
            files.append(f[:-len(ext)])
    return files


def get_tags_files_dict(files):
    # Return dict of:
    #   * keys are @tag find in top mardown file and stargin with @.
    #   * Values are the files associated to tags

    tags_files = {}
    for f in files:
        with open(f+_ext, 'r') as _f:
            for l in _f.readlines():
                l = l.strip()
                if l.startswith(('\n', '#', '%')):
                    continue
                elif l.startswith('@'):
                    tag = l[1:]
                    tag_set = tags_files.get(tag, set())
                    tag_set.add(f)
                    tags_files[tag] = tag_set
                else:
                    break

    for t in tags_files:
        tags_files[t] = list(tags_files[t])
    return tags_files


def gen_tagmenu_md(tags):
    # Return an MD formated list of @tag from the input list
    menu = {}
    main = _main
    rev = _rev
    l = ''
    for t in tags:
        l += '* [%s](%s?rev=%s&q=tag_%s)\n' % (t.title(), main, rev, t)
    menu['tags_list'] = l

    return menu


def gen_taggroup_md(tags_files_dict):
    # Return dict of MD content grouping by @tag.
    #   * keys are the file, also ref in the @tagmenu pages
    #   * values are list of MD pages associated to tags
    taggroup = {}
    rev = _rev
    main = _main
    for t, lf in tags_files_dict.items():
        md_code = '# %s \n\n' % t
        for f in lf:
            md_code += '* [%s](%s?rev=%s&q=%s)\n' % (f.title().replace('_', ' '), main, rev, f)
        md_code += '\n'
        tag_ref = 'tag_' + t
        taggroup[tag_ref] = md_code

    return taggroup


def dump_html(input):
    # Dump the html file of the dictionnary input,
    # if dict: keys are the files name, and values the HTML content.
    # else list: list of MD files

    if type(input) in (list, set):
        for f in input:
            fin = f + _ext
            fout = f + '.html'
            print 'creating %s' % (fout)
            pypandoc.convert(fin, 'html', outputfile=fout)
    elif type(input) is dict:
        for f , content in input.items():
            fout = f + '.html'
            print 'creating %s' % (fout)
            pypandoc.convert(content, 'html', format='md', outputfile=fout)
    else:
        raise NotImplementedError()


if __name__ == '__main__':

    path = ('.')
    tags_files = get_tags_files_dict(get_md(path))
    files = set(sum(tags_files.values(), []))
    menu = gen_tagmenu_md(tags_files.keys())
    taggroup = gen_taggroup_md(tags_files)

    tagall = {'tags_all': '\n'.join(set(taggroup.values())) }

    renderer = [menu, tagall, taggroup, files]
    for d in renderer:
        dump_html(d)



