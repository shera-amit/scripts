from ase.db import connect
from ase.io import read, write
import os
from pathlib import Path
import argparse

def sync_db(old_db_path, new_db_path, sync_to_old=True):
    if sync_to_old:
        db = connect(old_db_path)
    else:
        db = connect(new_db_path)

    dirs = [d for d in os.listdir() if d[0].isdigit()]

    for row in db.select():
        row_id = row.id
        try:
            atoms = read(f'./{row_id}/OUTCAR')
            db.write(atoms, id=row_id)
        except FileNotFoundError:
            print(f'Failed to read {row_id}')
            continue

    print(f'Database synced successfully to {"old" if sync_to_old else "new"} database.')

def main():
    parser = argparse.ArgumentParser(description='Sync calculations to a database.')
    parser.add_argument('old_db_path', help='Path to the old database file')
    parser.add_argument('new_db_path', help='Path to the new database file')
    parser.add_argument('--sync-to-new', action='store_true', help='Sync to the new database')

    args = parser.parse_args()

    sync_to_old = not args.sync_to_new

    sync_db(args.old_db_path, args.new_db_path, sync_to_old)

if __name__ == '__main__':
    main()
