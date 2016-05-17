from csv import DictReader
from waflib.Task import Task
from waflib.TaskGen import feature, before_method
from waflib.Context import g_module, APPNAME, VERSION
from re import compile

class patch_aurinfo(Task):
  package = compile('pkgname = gnome-shell-extension-hide-(.*)-git\n')
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
  ctx(source='PKGBUILD.in',
      mapping={
        'appname': appname,
        'major': major,
        'minor': minor},
      target='PKGBUILD')
  ctx(rule='makepkg --printsrcinfo -p ${SRC} > ${TGT}',
      source='PKGBUILD',
      target='SRCINFO.in',
      name='mksrcinfo')
  ctx(features='aurinfo',
      source='SRCINFO.in extensions.csv',
      target='.SRCINFO')
  ctx(rule='tar cf ${TGT} -C ${bld.bldnode.abspath()} '
          '--transform="s|^|' + appname + '/|" ${SRC}',
      source='PKGBUILD .SRCINFO ',
      target='gnome-shell-extension-aggregatemenu-hider-{}-{}.src.tar.gz'
        .format(major, minor),
      install_path='${DESTDIR}')

setattr(g_module, 'build', dist)
