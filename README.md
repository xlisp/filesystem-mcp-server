# Filesystem MCP Server

A secure and feature-rich Model Context Protocol (MCP) server that provides safe filesystem operations and command execution capabilities for AI assistants.

## Overview

This MCP server enables AI assistants to interact with the local filesystem in a controlled and secure manner. It provides tools for reading, writing, listing files and directories, executing system commands, and searching file contents using The Silver Searcher (ag).

* 🚀 quickly for vscode mcp setting: mcp.json
```
{
  "servers": {
  "filesystem": {
      "type": "stdio",
      "command": "/opt/anaconda3/bin/python",
      "args": ["/Users/xlisp/PyPro/filesystem-mcp-server/filesystem.py"]
    },
...
 }
}
```

## Features

### 🔒 Security Features

- **Path Safety Validation**: Prevents directory traversal attacks
- **File Type Restrictions**: Only allows specific file extensions
- **File Size Limits**: Maximum 10MB file size to prevent memory issues
- **Command Blocking**: Blocks dangerous system commands (rm, del, format, etc.)
- **Encoding Support**: Multiple encoding fallback for international character support

### 📁 File Operations

- **Read Files**: Read text file contents with automatic encoding detection
- **Write Files**: Create or overwrite files with specified encoding
- **Append Files**: Append content to existing files
- **File Information**: Get detailed metadata about files and directories

### 📂 Directory Operations

- **List Directory**: View directory contents with file sizes
- **Create Directory**: Create directories with parent directory support
- **Get Current Directory**: Retrieve the current working directory

### 🔍 Search Capabilities

- **Pattern Search**: Search files using regex patterns with ag (The Silver Searcher)
- **File Type Filtering**: Filter search results by file extension
- **Context Lines**: Show surrounding lines for search matches
- **Case Sensitivity**: Optional case-sensitive or case-insensitive search

### ⚙️ Command Execution

- **Safe Command Execution**: Execute system commands with timeout protection
- **Working Directory Support**: Run commands in specific directories
- **Output Capture**: Capture both stdout and stderr

## Installation

### Prerequisites

- Python 3.8 or higher
- FastMCP library
- (Optional) The Silver Searcher (ag) for advanced file searching

### Install Dependencies

```bash
pip install mcp
```

### Install The Silver Searcher (Optional)

For advanced file searching capabilities:

**macOS:**
```bash
brew install the_silver_searcher
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install silversearcher-ag
```

**Linux (RedHat/CentOS):**
```bash
sudo yum install the_silver_searcher
```

**Windows:**
```bash
choco install ag
```

## Configuration

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

**macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["/path/to/filesystem.py"]
    }
  }
}
```

### Cursor/Windsurf Configuration

Add to your MCP settings:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["/absolute/path/to/filesystem.py"]
    }
  }
}
```

## Available Tools

### 1. read_file

Read the contents of a text file with automatic encoding detection.

**Parameters:**
- `file_path` (string): Path to the file to read

**Example:**
```
Read the file at /Users/username/documents/notes.txt
```

**Returns:**
- File path, size, and complete content
- Error message if file is inaccessible, too large, or has unsupported type

**Supported Encodings:**
- UTF-8
- GBK (Chinese)
- GB2312 (Simplified Chinese)
- Latin-1
- CP1252 (Windows)

---

### 2. write_file

Create a new file or overwrite an existing file with content.

**Parameters:**
- `file_path` (string): Path to the file to write
- `content` (string): Content to write to the file
- `encoding` (string, optional): File encoding (default: utf-8)

**Example:**
```
Write "Hello, World!" to /Users/username/test.txt
```

**Returns:**
- Success message with character count
- Error message if path is unsafe or content is too large

**Features:**
- Automatically creates parent directories if they don't exist
- Supports custom encoding

---

### 3. append_file

Append content to an existing file or create a new file.

**Parameters:**
- `file_path` (string): Path to the file to append to
- `content` (string): Content to append
- `encoding` (string, optional): File encoding (default: utf-8)

**Example:**
```
Append "\nNew line" to /Users/username/log.txt
```

**Returns:**
- Success message with appended character count
- Error message if final file size would exceed limit

---

### 4. list_directory

List the contents of a directory with file information.

**Parameters:**
- `directory_path` (string, optional): Path to directory (default: current directory)
- `show_hidden` (boolean, optional): Show hidden files (default: false)

**Example:**
```
List all files in /Users/username/projects
```

**Returns:**
- Formatted list with file/directory type, name, and size
- Error message if directory doesn't exist or is inaccessible

**Output Format:**
```
Type Name                                    Size
------------------------------------------------------------
DIR  subfolder                                    0 bytes
FILE document.txt                            1,234 bytes
FILE script.py                               5,678 bytes
```

---

### 5. get_file_info

Get detailed metadata about a file or directory.

**Parameters:**
- `file_path` (string): Path to the file or directory

**Example:**
```
Get information about /Users/username/document.pdf
```

**Returns:**
- Path, name, type, size
- Creation, modification, and access timestamps
- File extension (for files)
- Read/write/execute permissions

**Sample Output:**
```
Path: /Users/username/document.pdf
Name: document.pdf
Type: File
Size: 1,234,567 bytes
Created: Mon Dec 28 10:30:45 2025
Modified: Mon Dec 28 14:22:10 2025
Accessed: Mon Dec 28 15:45:30 2025
Extension: .pdf
Readable: True
Writable: True
Executable: False
```

---

### 6. execute_command

Execute a system command safely with timeout protection.

**Parameters:**
- `command` (string): Command to execute
- `working_directory` (string, optional): Working directory (default: current directory)
- `timeout` (integer, optional): Timeout in seconds (default: 30)

**Example:**
```
Execute "ls -la" in /Users/username/projects
```

**Returns:**
- Command, working directory, return code
- Standard output and error output
- Error message if command is blocked or times out

**Blocked Commands (for security):**
- rm, del, format, mkfs, dd
- shutdown, reboot, halt, poweroff

---

### 7. get_current_directory

Get the current working directory.

**Parameters:** None

**Example:**
```
What is the current directory?
```

**Returns:**
- Absolute path of current working directory

---

### 8. create_directory

Create a new directory, including parent directories if needed.

**Parameters:**
- `directory_path` (string): Path of the directory to create

**Example:**
```
Create directory /Users/username/projects/new-project/src
```

**Returns:**
- Success message with absolute path
- Error message if path is unsafe

**Features:**
- Creates all parent directories automatically
- Succeeds silently if directory already exists

---

### 9. search_files_ag

Search for text patterns in files using The Silver Searcher (ag).

**Parameters:**
- `pattern` (string): Text pattern to search for (supports regex)
- `search_path` (string, optional): Directory to search in (default: current directory)
- `file_type` (string, optional): File type filter (e.g., 'py', 'js', 'clj')
- `case_sensitive` (boolean, optional): Case-sensitive search (default: false)
- `max_results` (integer, optional): Maximum results (default: 100)
- `context_lines` (integer, optional): Context lines before/after match (default: 0)

**Example:**
```
Search for "TODO" in all Python files in /Users/username/projects with 2 lines of context
```

**Returns:**
- Search results with file paths, line numbers, and matched content
- Total match count
- Error message if ag is not installed or search fails

**Features:**
- Regex pattern support
- File type filtering
- Context lines for better understanding
- Color-coded output
- Line numbers for easy navigation

---

## Allowed File Extensions

The server restricts file operations to the following extensions for security:

- **Text:** .txt, .md, .log
- **Programming:** .py, .java, .js, .clj, .edn, .cljs, .cljc
- **Data:** .json, .csv, .xml, .yaml, .yml
- **Web:** .html, .css
- **Scripts:** .sh, .bat
- **Other:** .dump

## Security Considerations

### Path Safety
- All paths are validated to prevent directory traversal attacks
- Paths containing `..` components are rejected

### File Size Limits
- Maximum file size: 10MB
- Prevents memory exhaustion and performance issues

### Command Execution
- Dangerous commands are blocked
- All commands run with 30-second timeout (configurable)
- Commands execute in specified working directory only

### Encoding Safety
- Multiple encoding fallback prevents crashes
- Handles international characters gracefully

## Error Handling

The server provides detailed error messages for:

- **Invalid paths:** "Error: Unsafe file path: ..."
- **Unsupported file types:** "Error: File type not allowed: ..."
- **Missing files:** "Error: File does not exist: ..."
- **Size violations:** "Error: File too large (>10485760 bytes): ..."
- **Encoding issues:** "Error: Unable to read file with supported encodings: ..."
- **Command timeouts:** "Error: Command timed out after 30 seconds"
- **Blocked commands:** "Error: Command not allowed for security reasons: ..."

## Usage Examples

### Example 1: Read and Analyze a File

**User:** "Read the file /Users/username/projects/app.py and tell me what it does"

**Assistant:** Uses `read_file` tool to read the content, then analyzes the code and explains its functionality.

---

### Example 2: Create a New Project Structure

**User:** "Create a new Python project structure in /Users/username/projects/myapp with src, tests, and docs folders"

**Assistant:** 
1. Uses `create_directory` to create `/Users/username/projects/myapp/src`
2. Uses `create_directory` to create `/Users/username/projects/myapp/tests`
3. Uses `create_directory` to create `/Users/username/projects/myapp/docs`
4. Uses `write_file` to create `README.md`, `setup.py`, etc.

---

### Example 3: Search for TODOs in a Project

**User:** "Find all TODO comments in my Python project at /Users/username/projects/webapp"

**Assistant:** Uses `search_files_ag` with:
- pattern: "TODO"
- search_path: "/Users/username/projects/webapp"
- file_type: "py"
- context_lines: 2

Returns all TODO comments with surrounding context.

---

### Example 4: Batch File Processing

**User:** "List all Python files in /Users/username/scripts and show me the first one"

**Assistant:**
1. Uses `list_directory` to get all files in the directory
2. Filters for .py files
3. Uses `read_file` to read the first Python file
4. Displays the content

---

### Example 5: Execute Build Command

**User:** "Run 'npm install' in /Users/username/projects/webapp"

**Assistant:** Uses `execute_command` with:
- command: "npm install"
- working_directory: "/Users/username/projects/webapp"
- timeout: 30

Returns the installation output and any errors.

---

## Troubleshooting

### Issue: "ag is not installed" error

**Solution:** Install The Silver Searcher:
```bash
# macOS
brew install the_silver_searcher

# Linux (Debian/Ubuntu)
sudo apt-get install silversearcher-ag

# Linux (RedHat/CentOS)
sudo yum install the_silver_searcher

# Windows
choco install ag
```

---

### Issue: "File type not allowed" error

**Solution:** The file extension is not in the allowed list. Supported extensions are:
- .txt, .py, .java, .js, .json, .md, .csv, .log, .yaml, .yml, .xml, .html, .css, .sh, .bat, .clj, .edn, .cljs, .cljc, .dump

If you need to support additional file types, modify the `ALLOWED_EXTENSIONS` set in the code.

---

### Issue: "File too large" error

**Solution:** The file exceeds the 10MB limit. You can:
1. Split the file into smaller chunks
2. Modify the `MAX_FILE_SIZE` constant in the code (not recommended for security)
3. Use command-line tools via `execute_command` for large files

---

### Issue: "Command not allowed" error

**Solution:** The command is blocked for security reasons. Blocked commands include:
- rm, del, format, mkfs, dd, shutdown, reboot, halt, poweroff

Use alternative safe commands or modify the `BLOCKED_COMMANDS` set if you trust the environment.

---

### Issue: "Unable to read file with supported encodings"

**Solution:** The file encoding is not supported. The server tries:
- UTF-8, GBK, GB2312, Latin-1, CP1252

For other encodings, you may need to convert the file first or add the encoding to the `read_file_content` function.

---

## Advanced Configuration

### Customizing Allowed Extensions

Edit the `ALLOWED_EXTENSIONS` set in `filesystem.py`:

```python
ALLOWED_EXTENSIONS = {
    '.txt', '.py', '.java', '.js', '.json', '.md', 
    '.csv', '.log', '.yaml', '.yml', '.xml', '.html', 
    '.css', '.sh', '.bat', '.clj', '.edn', '.cljs', 
    '.cljc', '.dump',
    # Add your custom extensions here
    '.rs', '.go', '.cpp', '.h'
}
```

---

### Adjusting File Size Limit

Modify the `MAX_FILE_SIZE` constant:

```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB instead of 10MB
```

**Warning:** Larger file sizes may impact performance and memory usage.

---

### Adding Custom Encodings

Add encodings to the `read_file_content` function:

```python
async def read_file_content(file_path: str) -> str | None:
    encodings = [
        'utf-8', 'gbk', 'gb2312', 'latin-1', 'cp1252',
        # Add your custom encodings here
        'shift-jis', 'euc-kr', 'big5'
    ]
    # ... rest of the function
```

---

### Modifying Command Timeout

Change the default timeout in `execute_command`:

```python
@mcp.tool()
async def execute_command(
    command: str, 
    working_directory: str = ".", 
    timeout: int = 60  # Changed from 30 to 60 seconds
) -> str:
    # ... rest of the function
```

---

## Best Practices

### 1. Always Use Absolute Paths
Use absolute paths instead of relative paths for clarity and reliability:
```
✅ /Users/username/projects/app.py
❌ ../projects/app.py
```

### 2. Check File Existence First
Before reading or writing, use `get_file_info` or `list_directory` to verify:
```
1. List directory to see available files
2. Read the specific file you need
```

### 3. Use Appropriate Search Tools
- For simple file listing: Use `list_directory`
- For content search: Use `search_files_ag` with appropriate filters
- For file metadata: Use `get_file_info`

### 4. Handle Large Directories Carefully
When listing large directories, consider:
- Using `search_files_ag` with file type filters
- Listing subdirectories one at a time
- Using command-line tools via `execute_command` for very large directories

### 5. Validate Paths in Prompts
When asking the AI to work with files, provide complete, valid paths:
```
✅ "Read /Users/username/documents/report.txt"
❌ "Read that file we talked about earlier"
```

---

## Performance Considerations

### File Reading
- Files are read entirely into memory
- Maximum file size is 10MB by default
- Multiple encoding attempts may slow down reading of large files

### Directory Listing
- Sorted alphabetically for consistency
- Hidden files excluded by default (can be enabled)
- Large directories (1000+ files) may take a few seconds

### Search Operations
- `search_files_ag` is very fast for large codebases
- Regex patterns may be slower than literal strings
- Context lines increase output size

### Command Execution
- All commands have a 30-second timeout by default
- Long-running commands should increase timeout parameter
- Output is captured in memory (very large outputs may cause issues)

---

## Security Best Practices

### 1. Restrict File Access
Only allow the MCP server to access specific directories by running it in a controlled environment.

### 2. Review Commands Before Execution
Always review commands before asking the AI to execute them, especially:
- Commands that modify system state
- Commands with sudo/admin privileges
- Commands that access sensitive data

### 3. Monitor File Operations
Keep track of what files the AI is reading and writing to ensure it stays within expected boundaries.

### 4. Use Read-Only Mode When Possible
If you only need to read files, consider creating a read-only variant that disables `write_file`, `append_file`, and `execute_command`.

### 5. Regular Security Audits
Periodically review:
- Allowed file extensions
- Blocked commands list
- File size limits
- Timeout settings

---

## API Reference

### Tool Signatures

```python
async def read_file(file_path: str) -> str

async def write_file(
    file_path: str, 
    content: str, 
    encoding: str = "utf-8"
) -> str

async def append_file(
    file_path: str, 
    content: str, 
    encoding: str = "utf-8"
) -> str

async def list_directory(
    directory_path: str = ".", 
    show_hidden: bool = False
) -> str

async def get_file_info(file_path: str) -> str

async def execute_command(
    command: str, 
    working_directory: str = ".", 
    timeout: int = 30
) -> str

async def get_current_directory() -> str

async def create_directory(directory_path: str) -> str

async def search_files_ag(
    pattern: str,
    search_path: str = ".",
    file_type: Optional[str] = None,
    case_sensitive: bool = False,
    max_results: int = 100,
    context_lines: int = 0
) -> str
```

---

## Contributing

To extend this MCP server:

1. **Add New Tools:** Define new functions with the `@mcp.tool()` decorator
2. **Enhance Security:** Add more validation and safety checks
3. **Support More File Types:** Extend `ALLOWED_EXTENSIONS`
4. **Improve Error Handling:** Add more specific error messages
5. **Add Logging:** Implement comprehensive logging for debugging

---

## License

This MCP server is provided as-is for educational and development purposes. Please review and modify security settings according to your specific needs and environment.

---

## Support

For issues, questions, or contributions:
- Review the troubleshooting section
- Check the security considerations
- Ensure all prerequisites are installed
- Verify file paths and permissions

---

## Version History

### Version 1.0
- Initial release
- Core file operations (read, write, append)
- Directory operations (list, create, info)
- Command execution with safety checks
- The Silver Searcher (ag) integration
- Multi-encoding support
- Security features (path validation, file type restrictions, command blocking)

---

## Acknowledgments

Built with:
- **FastMCP**: Model Context Protocol implementation
- **The Silver Searcher (ag)**: Fast code searching tool
- **Python**: Core programming language

---

**Happy Coding! 🚀**
