# template.py
# Waf module to insert tokens in template files with given values.

from waflib.TaskGen import extension
from waflib.Task import Task
from string import Template
from pickle import dumps
from operator import itemgetter

class template(Task):
  def run(self):
    self.outputs[0].write(Template(self.inputs[0].read()).safe_substitute(self.generator.mapping))

  def sig_vars(self):
    super().sig_vars()
    for _, v in sorted(self.generator.mapping.items(), key=itemgetter(0)):
      self.m.update(dumps(v))

@extension('.in')
def process_template(gen, source):
  out_dir = getattr(gen, 'out_dir', None)
  if out_dir:
    out_dir = gen.bld.bldnode.find_or_declare(out_dir)
    out_dir.mkdir()
  else:
    out_dir = gen.bld.bldnode
  target = out_dir.make_node(source.change_ext('', ext_in='.in').name)
  gen.create_task('template', source, target)
  inst_to = getattr(gen, 'install_path', None)
  if inst_to:
    gen.bld.install_files(inst_to, [target])
