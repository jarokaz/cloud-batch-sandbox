from absl import flags
from absl import app
from absl import logging


flags.DEFINE_integer('random_seed', None, 'The random seed for the data '
                     'pipeline. By default, this is randomly generated. Note '
                     'that even if this is set, Alphafold may still not be '
                     'deterministic, because processes like GPU inference are '
                     'nondeterministic.')

FLAGS = flags.FLAGS

def _main(argv):
    print(FLAGS.random_seed)


if __name__ == "__main__":
    app.run(_main)
