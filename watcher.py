import os
import time
import database
from indexer import read_content, skip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return
        c = database.connection()
        path = event.src_path
        filename = os.path.basename(path)
        filetype = os.path.splitext(filename)[1].lower()
        content = read_content(path, filetype)
        database.insert(c, filename, path, filetype,content)
        c.commit()
        print(f'[+] Indexed new file: {filename}')
        c.close()
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        database.delete(event.src_path)
        print(f'[-] Removed from index: {os.path.basename(event.src_path)}')
    
    def on_modified(self, event):
        if event.is_directory:
            return
        path = event.src_path
        filename = os.path.basename(path)
        filetype = os.path.splitext(filename)[1].lower()
        content = read_content(path, filetype)
        database.update(path, content)
        print(f'[~] Updated in index: {filename}')

    def on_moved(self, event):
        if event.is_directory:
            return
        c = database.connection()
        database.delete(event.src_path)
        newpath = event.dest_path
        filename = os.path.basename(newpath)
        filetype = os.path.splitext(filename)[1].lower()
        content = read_content(newpath, filetype)
        database.insert(c,filename,newpath,filetype,content)
        c.commit()
        print(f'[>] Moved in index: {filename}')
        c.close()

def run():
    folders_to_watch = [
        os.path.expanduser('~/OneDrive'),
        os.path.expanduser('~/Desktop'),
        os.path.expanduser('~/Documents'),
        os.path.expanduser('~/Pictures'),
        os.path.expanduser('~/Downloads'),
        os.path.expanduser('~/javafiles'),
        os.path.expanduser('~/Videos'),
        os.path.expanduser('~/Music'),
        'C:/Program Files/Games',
        'C:/ytdl'
    ]

    handler = FileChangeHandler()
    observer = Observer()

    for folder in folders_to_watch:
        if os.path.exists(folder):
            observer.schedule(handler, folder, recursive = True)
            print(f"Watching: {folder}")

    observer.start()
    print('File watcher running..... Press Ctrl+C to stop.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__=='__main__':
    run()