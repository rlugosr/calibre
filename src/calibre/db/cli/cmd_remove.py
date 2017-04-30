#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

from calibre.db.delete_service import delete_service
from calibre.srv.changes import books_deleted

readonly = False


def implementation(db, notify_changes, ids, permanent):
    db.remove_books(ids, permanent=permanent)
    if not permanent:
        delete_service().wait()
    if notify_changes is not None:
        notify_changes(books_deleted(ids))


def option_parser(get_parser):
    p = get_parser(
        _(
            '''\
%prog remove ids

Remove the books identified by ids from the database. ids should be a comma separated \
list of id numbers (you can get id numbers by using the search command). For example, \
23,34,57-85 (when specifying a range, the last number in the range is not included).
'''
        )
    )
    p.add_option(
        '--permanent',
        default=False,
        action='store_true',
        help=_('Do not use the recycle bin')
    )
    return p


def main(opts, args, dbctx):
    if len(args) < 1:
        raise SystemExit(_('You must specify at least one book to remove'))

    ids = set()
    for arg in args:
        for x in arg.split(','):
            y = tuple(map(int, x.split('-')))
            if len(y) > 1:
                ids |= set(range(y[0], y[1]))
            else:
                ids.add(y[0])

    dbctx.run('remove', ids, opts.permanent)

    return 0
