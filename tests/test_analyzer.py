import unittest
from unittest.mock import patch, MagicMock
import os
import stat
from analyzer import traverse_directory, categorize_files, calculate_total_size, categorize_permissions, find_large_files

class TestDirectoryAnalysisTool(unittest.TestCase):

    #Test traverse_directory function without errors
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.stat')
    def test_traverse_directory(self, mock_stat, mock_getsize, mock_walk):
        mock_walk.return_value = [
            ('/test', ('subdir',), ('file1', 'file2')),
            ('/test/subdir', (), ('file3',)),
        ]
        mock_getsize.side_effect = [100, 200, 300]
        mock_stat.side_effect = [
            MagicMock(st_mode=stat.S_IRUSR), 
            MagicMock(st_mode=stat.S_IWUSR), 
            MagicMock(st_mode=stat.S_IXUSR)
        ]

        expected = [
            ('/test/file1', 100, stat.S_IRUSR),
            ('/test/file2', 200, stat.S_IWUSR),
            ('/test/subdir/file3', 300, stat.S_IXUSR),
        ]

        result = traverse_directory('/test')

        result = sorted(result)
        expected = sorted(expected)

        self.assertEqual(result, expected)


    #Test traverse_directory function with OSError
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.stat')
    def test_traverse_directory_error(self, mock_stat, mock_getsize, mock_walk):
        mock_walk.return_value = [
            ('/test', ('subdir',), ('file1', 'file2')),
        ]
        mock_getsize.side_effect = [100, OSError('Permission denied')]
        mock_stat.side_effect = [MagicMock(st_mode=stat.S_IRUSR)]

        expected = [
            ('/test/file1', 100, stat.S_IRUSR),
        ]

        with patch('builtins.print') as mock_print:
            result = traverse_directory('/test')
            mock_print.assert_called_with("Error accessing /test/file2: Permission denied")
        self.assertEqual(result, expected)

    #Test the function categorize_files
    @patch('mimetypes.guess_type')
    def test_categorize_files(self, mock_guess_type):
        file_info = [
            ('/test/file1.txt', 100, stat.S_IRUSR),
            ('/test/file2.jpg', 200, stat.S_IWUSR),
            ('/test/file3', 300, stat.S_IXUSR),
        ]

        mock_guess_type.side_effect = [('text/plain', None), ('image/jpeg', None), (None, None)]

        expected = {
            'text': [('/test/file1.txt', 100, stat.S_IRUSR)],
            'image': [('/test/file2.jpg', 200, stat.S_IWUSR)],
            'unknown': [('/test/file3', 300, stat.S_IXUSR)]
        }

        result = categorize_files(file_info)
        self.assertEqual(result, expected)

    #Test the function calculate_total_size
    def test_calculate_total_size(self):
        categorized_files = {
            'text': [('/test/file1.txt', 100, stat.S_IRUSR)],
            'image': [('/test/file2.jpg', 200, stat.S_IWUSR)],
            'unknown': [('/test/file3', 300, stat.S_IXUSR)]
        }

        expected = {
            'text': 100,
            'image': 200,
            'unknown': 300
        }

        result = calculate_total_size(categorized_files)
        self.assertEqual(result, expected)

    #Test the function categorize_permissions with different permissions
    def test_categorize_permissions(self):
        file_info = [
            ('/test/file1', 100, stat.S_IWOTH),
            ('/test/file2', 200, stat.S_ISUID),
            ('/test/file3', 300, stat.S_ISGID),
            ('/test/file4', 400, stat.S_ISVTX),
            ('/test/file5', 500, stat.S_IRUSR)
        ]

        expected = {
            'world_writable': ['/test/file1'],
            'suid_files': ['/test/file2'],
            'sgid_files': ['/test/file3'],
            'sticky_files': ['/test/file4']
        }

        result = categorize_permissions(file_info)
        self.assertEqual(result, expected)

    #Test the function find_large_files with default threshold
    def test_find_large_files(self):
        file_info = [
            ('/test/file1', 100, stat.S_IRUSR),
            ('/test/file2', 20000000, stat.S_IWUSR),
            ('/test/file3', 300, stat.S_IXUSR),
        ]

        expected = ['/test/file2']

        result = find_large_files(file_info, 10485760)  #10MB
        self.assertEqual(result, expected)

    #Test find_large_files function with custom thresholds
    #There is one file with 15MB threshold
    #There is no files with 25MB threshold
    def test_find_large_files_different_threshold(self):
        file_info = [
            ('/test/file1', 100, stat.S_IRUSR),
            ('/test/file2', 20000000, stat.S_IWUSR),
            ('/test/file3', 300, stat.S_IXUSR),
        ]

        expected = ['/test/file2']
        result = find_large_files(file_info, 15000000)  #15MB
        self.assertEqual(result, expected)

        expected = []
        result = find_large_files(file_info, 25000000)  #25MB
        self.assertEqual(result, expected)

    #Test the function categorize_files with an unknown file type
    @patch('mimetypes.guess_type')
    def test_categorize_files_with_unknown_type(self, mock_guess_type):
        file_info = [
            ('/test/file1.txt', 100, stat.S_IRUSR),
            ('/test/file2.unknown', 200, stat.S_IWUSR),
        ]

        mock_guess_type.side_effect = [('text/plain', None), (None, None)]

        expected = {
            'text': [('/test/file1.txt', 100, stat.S_IRUSR)],
            'unknown': [('/test/file2.unknown', 200, stat.S_IWUSR)]
        }

        result = categorize_files(file_info)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
