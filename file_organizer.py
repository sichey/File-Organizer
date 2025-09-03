import os
import shutil
from pathlib import Path
import datetime

FILE_CATEGORIES = {
    'Images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx', '.csv', '.odt', '.rtf'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', '.opus'],
    'Scripts': ['.py', '.js', '.sh', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.swift', '.ts', '.json', '.xml', 'sql'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Editing Files': ['.psd', '.prproj', '.aep', '.blend', '.ai', '.indd', '.eps', '.svg'],
}

SORT_LOG_FILENAME = ".sort_log"
USER_FOLDERS_KEY = "USER_FOLDERS"  

def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return 'Others'

def write_to_log(root_path: Path, moved_files):
    log_path = root_path / SORT_LOG_FILENAME
    with log_path.open("w", encoding="utf-8") as f:
        for original_path, new_path in moved_files:
            f.write(f"{original_path}||{new_path}\n")

def read_log(root_path: Path):
    log_path = root_path / SORT_LOG_FILENAME
    if not log_path.exists():
        return []

    moved_files = []
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("||")
            if len(parts) == 2:
                moved_files.append((parts[0], parts[1]))
    return moved_files

def delete_log(root_path: Path):
    log_file = root_path / SORT_LOG_FILENAME
    if log_file.exists():
        log_file.unlink()

def get_date_folder_name(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%B %Y")  

def sort_by_type(path):
    root_path = Path(path)
    moved_files = []

    
    for item in root_path.iterdir():
        if item.parent != root_path:
            continue
        if item.is_file() and item.name != SORT_LOG_FILENAME:
            ext = item.suffix.lower()
            category = get_category(ext)
            target_dir = root_path / category
            target_dir.mkdir(exist_ok=True)

            target_path = target_dir / item.name
            shutil.move(str(item), str(target_path))
            moved_files.append((str(item), str(target_path)))
    
    
    for item in root_path.iterdir():
        if item.is_dir() and item.name not in [f for f in FILE_CATEGORIES.keys()] + ["Others"]:
            
            others_dir = root_path / "Others"
            others_dir.mkdir(exist_ok=True)
            
            target_path = others_dir / item.name
            shutil.move(str(item), str(target_path))
            moved_files.append((f"{USER_FOLDERS_KEY}:{str(item)}", str(target_path)))

    write_to_log(root_path, moved_files)

def sort_by_date(path):
    root_path = Path(path)
    moved_files = []

    
    for item in root_path.iterdir():
        if item.parent != root_path:
            continue
        if item.is_file() and item.name != SORT_LOG_FILENAME:
            modified_time = item.stat().st_mtime
            folder_name = get_date_folder_name(modified_time)
            target_dir = root_path / folder_name
            target_dir.mkdir(exist_ok=True)

            target_path = target_dir / item.name
            shutil.move(str(item), str(target_path))
            moved_files.append((str(item), str(target_path)))
    
    
    for item in root_path.iterdir():
        if item.is_dir() and not any(item.name.startswith(month) for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
            
            modified_time = item.stat().st_mtime
            folder_name = get_date_folder_name(modified_time)
            target_dir = root_path / folder_name
            target_dir.mkdir(exist_ok=True)
            
            target_path = target_dir / item.name
            shutil.move(str(item), str(target_path))
            moved_files.append((f"{USER_FOLDERS_KEY}:{str(item)}", str(target_path)))

    write_to_log(root_path, moved_files)

def sort_all(path):
    root_path = Path(path)
    moved_files = []

    
    
    
    for item in root_path.iterdir():
        if item.parent != root_path:
            continue
        if item.is_file() and item.name != SORT_LOG_FILENAME:
            
            modified_time = item.stat().st_mtime
            date_folder_name = get_date_folder_name(modified_time)
            date_folder = root_path / date_folder_name
            date_folder.mkdir(exist_ok=True)
            
            
            ext = item.suffix.lower()
            category = get_category(ext)
            type_folder = date_folder / category
            type_folder.mkdir(exist_ok=True)
            
            
            target_path = type_folder / item.name
            shutil.move(str(item), str(target_path))
            moved_files.append((str(item), str(target_path)))
    
    
    for item in root_path.iterdir():
        if item.is_dir() and not any(item.name.startswith(month) for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
            
            modified_time = item.stat().st_mtime
            date_folder_name = get_date_folder_name(modified_time)
            date_folder = root_path / date_folder_name
            date_folder.mkdir(exist_ok=True)
            
            
            others_folder = date_folder / "Others"
            others_folder.mkdir(exist_ok=True)
            
            
            target_path = others_folder / item.name
            shutil.move(str(item), str(target_path))
            
            moved_files.append((f"{USER_FOLDERS_KEY}:{str(item)}", str(target_path)))
    
    write_to_log(root_path, moved_files)

def undo_sort(path):
    root_path = Path(path)
    moved_files = read_log(root_path)

    
    for original_path, new_path in reversed(moved_files):
        
        if not original_path.startswith(f"{USER_FOLDERS_KEY}:"):
            original = Path(original_path)
            new = Path(new_path)
            if new.exists():
                
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(new), str(original))
    
    
    for original_path, new_path in reversed(moved_files):
        
        if original_path.startswith(f"{USER_FOLDERS_KEY}:"):
            original_folder_path = original_path[len(f"{USER_FOLDERS_KEY}:"):]
            original_folder = Path(original_folder_path)
            new_folder = Path(new_path)
            
            if new_folder.exists():
                
                target_path = root_path / original_folder.name
                shutil.move(str(new_folder), str(target_path))
            
            try:
                for subdir in new_folder.iterdir():
                    if subdir.is_dir():
                        for file in subdir.glob("**/*"):
                            if file.is_file():
                                target = root_path / file.name
                                shutil.move(str(file), str(target))
                        
                #shutil.rmtree(str(item))
            except Exception as e:
                print(f"Could not fully remove {new_folder}: {e}")
  
    
    
    clean_empty_directories(root_path)
    
    delete_log(root_path)

def clean_empty_directories(root_path):
    for item in list(root_path.iterdir()):
        if item.is_dir():
            clean_empty_directories(item)  
            try:
                item.rmdir()  
            except OSError:
                pass  