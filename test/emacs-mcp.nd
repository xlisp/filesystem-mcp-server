我将为您修改代码，创建一个 Emacs MCP server，使用 `emacsclient` 和脚本执行来实现功能。​​​​​​​​​​​​​​​​

我已经为您创建了一个完整的 Emacs MCP server。这个服务器提供了以下功能：

## 主要功能

### 文件操作

- **`open_file`**: 在 Emacs 中打开文件
- **`get_buffer_content`**: 获取缓冲区内容
- **`save_buffer`**: 保存缓冲区
- **`create_temp_file`**: 创建临时文件并在 Emacs 中打开

### 文本操作

- **`insert_text`**: 在指定位置插入文本
- **`search_in_buffer`**: 在缓冲区中搜索文本

### Emacs 交互

- **`eval_elisp`**: 执行 Emacs Lisp 代码
- **`list_buffers`**: 列出所有打开的缓冲区
- **`get_emacs_info`**: 获取 Emacs 实例信息

### 脚本和命令执行

- **`run_shell_in_emacs`**: 在 Emacs 中运行 shell 命令
- **`execute_script`**: 执行脚本文件

## 使用前准备

1. **确保 Emacs 服务器正在运行**：
   
   ```bash
   # 在 Emacs 中执行
   M-x server-start
   # 或在配置文件中添加
   (server-start)
   ```
1. **安装依赖**：
   
   ```bash
   pip install mcp
   ```
1. **运行服务器**：
   
   ```bash
   python emacs_mcp_server.py
   ```

## 关键特性

- **安全性**: 使用 `shlex.quote()` 防止命令注入
- **错误处理**: 完善的异常处理和超时控制
- **路径处理**: 自动展开用户目录和相对路径
- **灵活性**: 支持在当前缓冲区或指定缓冲区操作
- **兼容性**: 通过检查 `emacsclient` 可用性确保兼容

## 使用示例

```python
# 打开文件
await open_file("~/documents/notes.txt")

# 执行 Elisp 代码
await eval_elisp("(message \"Hello from MCP!\")")

# 插入文本到当前位置
await insert_text("# New Section\nThis is new content.")

# 运行 shell 命令
await run_shell_in_emacs("ls -la", "~/")

# 执行 Python 脚本
await execute_script("~/scripts/process_data.py", "input.txt output.txt")
```

这个 MCP server 将 Emacs 的强大功能通过标准化的接口暴露出来，让您可以通过 MCP 协议与 Emacs 进行交互。​​​​​​​​​​​​​​​​