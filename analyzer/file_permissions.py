import stat


def categorize_permissions(file_info):
    permissions_categories = {
        'world_writable': [],
        'suid_files': [],
        'sgid_files': [],
        'sticky_files': [],
    }

    for file_path, _, mode in file_info:
        if mode & stat.S_IWOTH:
            permissions_categories['world_writable'].append(file_path)
        if mode & stat.S_ISUID:
            permissions_categories['suid_files'].append(file_path)
        if mode & stat.S_ISGID:
            permissions_categories['sgid_files'].append(file_path)
        if mode & stat.S_ISVTX:
            permissions_categories['sticky_files'].append(file_path)

    return permissions_categories
