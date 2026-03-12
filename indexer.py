import os
import database
import pypdf
import docx

readables = {'.txt', '.pdf', '.docx', '.md', '.py', '.js', '.html', '.css', '.csv', '.json'}

skip = {'$Recyle.bin','AppData','node_modules','__pycache__','.git','venv','env'}

def read_content(filepath, filetype):
    if filetype not in readables:
        return ''
    try:
        if filetype == '.pdf':
            text=''
            reader=pypdf.PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() or ''
            return text [:5000]
        elif filetype == ".docx":
            doc = docx.Document(filepath)
            text = ' '.join([para.text for para in doc.paragraphs])
            return text[:5000]
        else:
            with open(filepath, 'r', encoding='utf-8', errors= 'ignore') as f:
                return f.read(5000)
    except Exception:
        return ''

def index_folder(folder_path,c):
    print(f'Indexing: {folder_path}')
    count = 0
    
    for root, dirs, files in os.walk(folder_path):
        filtered = []
        for d in dirs:
            if d not in skip:
                filtered.append(d)
        dirs[:] = filtered
    
        for filename in files:
            filepath = os.path.join(root,filename)
            filetype = os.path.splitext(filename)[1].lower()
            content = read_content(filepath, filetype)

            database.insert(c,filename, filepath, filetype, content)
            count+=1

            if count % 500 == 0:
                c.commit()
                print(f' Indexed  {count} files so far...')
    print(f'Done! Indexed {count} files from {folder_path}')
    return count

def run():
    database.create()
    c = database.connection()
    folders_to_index = [
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

    total = 0
    for folder in folders_to_index:
        if os.path.exists(folder):
            total += index_folder(folder, c)
        else:
            print(f'Skipping {folder} - folder not found')
    c.commit()
    c.close()
    print(f'Done Indexing! Total files indexed: {total}')
    print(f'Database has {database.get_total()} files total.')
if __name__== '__main__':
    run()