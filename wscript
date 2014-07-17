#! /usr/bin/env python

from csv import DictReader

def options(ctx):
  ctx.load('template', tooldir='.')
  ctx.load('gnu_dirs')

def configure(ctx):
  ctx.load('template', tooldir='.')
  ctx.load('gnu_dirs')

def build(ctx):
  with open('extensions.csv') as f:
    for extension in DictReader(f):
      name = extension['name'].partition(' ')[0]
      uuid = 'hide-' + name + '@' + extension['author']
      ctx(source='extension.js.in metadata.json.in',
          mapping={
            'name': name,
            'uuid': uuid,
            'item': extension['item'],
            'description': extension['description']},
          name=name,
          out_dir=uuid,
          install_path='${DATAROOTDIR}/gnome-shell/extensions/' + uuid)
