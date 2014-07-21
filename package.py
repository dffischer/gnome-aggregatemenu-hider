from waflib.Context import g_module, APPNAME, VERSION

def dist(ctx):
  appname = getattr(g_module, APPNAME)
  major, _, minor = getattr(g_module, VERSION).rpartition('.')
  package = 'gnome-shell-extension-aggregatemenu-hider-{}-{}.src.tar.gz'.format(major, minor)
  ctx(source='PKGBUILD.in',
      mapping={
        'appname': appname,
        'major': major,
        'minor': minor})

setattr(g_module, 'build', dist)
