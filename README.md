# GitLabManager - Discord Style

**Version 0.2** - A modern GUI client for GitLab operations with Discord-inspired styling

![Screenshot](![image](https://github.com/user-attachments/assets/a286e66e-0b40-42e9-b0d1-9287bf9446c0)
)

## Features ✨

- **Discord-Style Interface** 🎨  
  - Dark theme with accent colors inspired by Discord's UI design


- **Core Git Operations** 🔄  
  - Clone repositories
  - Commit changes
  - Push to remote
  - Pull updates


- **Enhanced Functionality** 🚀
  - Config persistence (auto-saves user inputs)
  - Multi-file selection dialog
  - Real-time console output
  - Interactive tooltips
  - Branch selection support
  - Secure token masking


- **Advanced Features** 💡
  - Threaded operations (prevents UI freezing)
  - Input validation
  - Git repository detection
  - Status notifications
  - Cross-platform support (releases are only available as .exe)

## Installation 📦

1. **Prerequisites**
   - Python 3.6+
   - Tkinter (usually included with Python)

2. **Run the application**
   ```bash
   python GitLabManager.py
   ```

## Usage Guide 🖥️

1. **Configure Connection**
   - Enter GitLab repository URL
   - Provide username and personal access token
   - Select local directory

2. **File Management** 📂
   - Use "Select Files" button to choose files for commit
   - View selected files in the listbox

3. **Git Operations** 
   - **Clone**: Initialize repository copy
   - **Commit**: Stage selected files with message
   - **Push**: Upload changes to remote
   - **Pull**: Fetch latest updates

4. **Console Output** 📋  
   View real-time command execution results in the integrated console

## Configuration ⚙️

- Automatic saving to `config.json`:
  ```json
  {
    "repo_url": "https://gitlab.com/your/repo.git",
    "username": "your_username",
    "token": "your_token",
    "local_dir": "/path/to/directory",
    "commit_message": "Default commit message",
    "branch": "main"
  }
  ```
- Config file is automatically created/updated on exit

## Project Structure 🗂️

```
GitLabManager/
├── main.py
├── config.json
├── README.md
├── LICENSE 
├── logo.ico
├── logo.png
└── requirements.txt
```

## License 📜

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Acknowledgments 🙏

- Built with Python's Tkinter framework
- Inspired by Discord's modern UI design
- Git integration powered by Git command-line tools

---

**Version 0.2.1 Changelog**
- icon added
- fixed some bugs
- added some improvements

**Version 0.2 Changelog**  
- Added Discord-style theme implementation
- Implemented real-time console output
- Added file selection dialog and listbox
- Introduced configuration persistence
- Added threaded command execution
- Improved error handling and validation
- Added interactive tooltips
- Implemented token visibility toggle

## 💰 You can help me by Donating
  [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/zyberphil) 
