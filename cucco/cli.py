# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click
import sys

from cucco.config import Config
from cucco.cucco import Cucco

@click.command()
@click.argument('path')
@click.pass_context
def batch(ctx, path):
    """
    Normalize files in path.

    Apply normalizations over all files found in a given path.
    The normalizations applied will be those defined in the config
    file. If no config is specified, the default normalizations will
    be used.
    """

    pass

@click.command()
@click.argument('text', required=False)
@click.pass_context
def normalize(ctx, text):
    """
    Normalize text or piped input.

    Normalize text passed as an argument to this command using
    the specified config (default values if --config option is
    not used).

    Pipes can be used along this command to process the output
    of another cli. This is the default behaviour when no text
    is defined.
    """

    if text:
        print(text)
    else:
        for line in sys.stdin:
            print(line)

@click.group()
@click.option('--config', '-c',
              help='Path to config file.')
@click.option('--language', '-c', default='en',
              help='Language to use for the normalization.')
@click.option('--verbose', is_flag=True,
              help='Increase output verbosity.')
@click.version_option()
@click.pass_context
def cli(ctx, config, language, verbose):
    """
    Cucco allows to apply normalizations to a given text or file.
    This normalizations include, among others, removal of accent
    marks, stop words an extra whitespaces, replacement of
    punctuation symbols, emails, emojis, etc.

    For more info on how to use and configure Cucco, check the
    project website at https://cucco.io.
    """

    ctx.obj = {}
    ctx.obj['config'] = Config(config, language, verbose)

cli.add_command(batch)
cli.add_command(normalize)
