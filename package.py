from csv import DictReader
from waflib.Task import Task
from waflib.TaskGen import feature, before_method
from waflib.Context import g_module, APPNAME, VERSION
from re import compile

class patch_aurinfo(Task):
  package = compile('pkgname = gnome-shell-extension-hide-(.*)\n')
  def run(self):
    with open(self.inputs[1].abspath(), 'r') as csv:
      descriptions = {
        extension['name'].partition(' ')[0].lower():
        extension['description']
        for extension in DictReader(csv)}
    with open(self.inputs[0].abspath(), 'r') as original,\
         open(self.outputs[0].abspath(), 'w') as out:
      for line in original:
        out.write(line)
        match = self.package.fullmatch(line)
        if match:
          out.write('\tpkgdesc = ' + descriptions[match.group(1)] + '\n')

@feature('aurinfo')
@before_method('process_source')
def aurinfo(gen):
  sources = gen.to_nodes(gen.source)
  gen.source = []
  gen.create_task('patch_aurinfo', sources, gen.path.find_or_declare(gen.target))

def dist(ctx):
  appname = getattr(g_module, APPNAME)
  major, _, minor = getattr(g_module, VERSION).rpartition('.')
  package = 'gnome-shell-extension-aggregatemenu-hider-{}-{}.src.tar.gz'.format(major, minor)
  ctx(source='PKGBUILD.in',
      mapping={
        'appname': appname,
        'major': major,
        'minor': minor})
  ctx(rule='mkaurball -fp ${SRC}',
      source='PKGBUILD',
      target=package,
      name='mkaurball')
  ctx(rule='tar xf ${SRC[0]} -C extract',
      source=package,
      target='extract/' + appname + '/.AURINFO'
            ' extract/' + appname + '/PKGBUILD')
  ctx(features='aurinfo',
      source='extract/' + appname + '/.AURINFO'
            ' extensions.csv',
      target='patched/' + appname + '/.AURINFO')
  ctx(rule='cp ${SRC} ${TGT}',
      source='extract/' + appname + '/PKGBUILD',
      target='patched/' + appname + '/PKGBUILD')
  ctx(rule='tar cf ${TGT} -C ${TGT[0].parent.abspath()} ${SRC[0].parent.name}',
      source='patched/' + appname + '/.AURINFO'
            ' patched/' + appname + '/PKGBUILD',
      target='patched/' + package)

setattr(g_module, 'build', dist)
