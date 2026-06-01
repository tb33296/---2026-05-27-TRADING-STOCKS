from pathlib import Path

def count_file_lines(file_path):
    """Safely counts the lines in a file, skipping binary or unreadable files."""
    try:
        with open(file_path, "rb") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def get_dir_stats(directory, ignore_set):
    """Recursively counts total subfolders and files inside a directory, ignoring specific names."""
    folder_count = 0
    file_count = 0
    
    try:
        for item in directory.iterdir():
            if item.name in ignore_set:
                continue
            if item.is_dir():
                folder_count += 1
                # Recursively add stats from subdirectories
                sub_folders, sub_files = get_dir_stats(item, ignore_set)
                folder_count += sub_folders
                file_count += sub_files
            else:
                file_count += 1
    except PermissionError:
        pass # Skip folders without read permissions
        
    return folder_count, file_count

def generate_tree_lines(directory, prefix="", ignore_set=None):
    """Recursively generates tree lines with stats as a list of strings."""
    if ignore_set is None:
        ignore_set = {".venv", "__pycache__", ".git", ".pytest_cache", ".egg-info", "build", "dist"}

    lines = []
    paths = [p for p in directory.iterdir() if p.name not in ignore_set]
    paths = sorted(paths, key=lambda p: (not p.is_dir(), p.name.lower()))
    count = len(paths)
    
    for i, path in enumerate(paths):
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        
        if path.is_dir():
            # Get total items inside this folder recursively
            sub_folders, sub_files = get_dir_stats(path, ignore_set)
            display_name = f"{path.name} ({sub_folders} folders, {sub_files} files)/"
        else:
            line_count = count_file_lines(path)
            display_name = f"{path.name} ({line_count} lines)"
        
        lines.append(f"{prefix}{connector}{display_name}")
        
        if path.is_dir():
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree_lines(path, prefix + extension, ignore_set))
            
    return lines

def save_tree_to_markdown(root_dir, output_filename="_folderTree.md"):
    path = Path(root_dir)
    ignore_set = {".venv", "__pycache__", ".git", ".pytest_cache", ".egg-info", "build", "dist"}
    
    # Root folder stats
    root_folders, root_files = get_dir_stats(path, ignore_set)
    root_name = f"{path.resolve().name} ({root_folders} folders, {root_files} files)/"
    
    tree_lines = generate_tree_lines(path, ignore_set=ignore_set)
    
    markdown_content = f"# Folder Tree\n\n```text\n{root_name}\n"
    markdown_content += "\n".join(tree_lines)
    markdown_content += "\n```\n"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Success: '{output_filename}' generated with folder metrics.")

# Run the generator for the current folder
save_tree_to_markdown(".")
