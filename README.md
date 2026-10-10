# UInstaller

**A lightweight, configurable installer for downloading, updating, and deploying applications.**

UInstaller is a universal desktop installer built with Python and PyWebView. It provides a simple graphical interface for automating application installation and updates without requiring users to interact with the command line.

The installer downloads files from a configured source, removes outdated files or directories, and optionally extracts downloaded archives to a specified location. Its behavior is controlled through a configuration layer, making it adaptable to different applications and deployment workflows.

## ✨ Features

- **Universal Configuration** — Customize the product name, download source, target paths, filenames, and installation behavior.
- **Automatic Downloads** — Download files from a remote URL with streaming support.
- **Old Version Cleanup** — Remove existing files and directories before deploying the new version.
- **Archive Extraction** — Optionally extract downloaded ZIP archives into a configured destination.
- **Live Progress Updates** — Display installation progress, status messages, and version information.
- **Lightweight GUI** — A compact desktop interface powered by PyWebView, HTML, CSS, and JavaScript.
- **Background Installation** — Run installation tasks in a separate thread to keep the interface responsive.
- **Reusable UI Bundle** — Build and save the interface to `uinstaller.uinterface`, allowing the installer to load the bundled UI when the source `ui` directory is unavailable.

## ⚙️ How It Works

UInstaller follows a simple installation workflow:

1. **Initialize** — Load the configuration and display the product name, current version, and target version.
2. **Download** — Retrieve the configured file from the remote source.
3. **Clean Up** — Remove existing files and directories specified in the target configuration.
4. **Finalize** — Either finish without extracting anything or extract the downloaded ZIP archive.
5. **Complete** — Notify the interface that the installation process has finished.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Core application logic |
| PyWebView | Desktop window and JavaScript API integration |
| HTML5 | User interface structure |
| CSS3 | Interface styling |
| JavaScript | UI interaction and progress updates |
| Requests | HTTP downloads |
| Threading | Background installation tasks |
| ZipFile | ZIP archive extraction |
| Shutil and OS | File and directory management |

## 📋 Requirements

- Python 3.13
- pip
- A supported operating system and WebView runtime for PyWebView
- Internet access to download the configured installation package
- Appropriate filesystem permissions for the configured target paths

## 🔧 Configuration

UInstaller uses a `Config` class to define the product-specific installation parameters.

The configuration layer provides the following settings:

| Setting | Description |
|---|---|
| Product name | Name displayed in the installer window |
| Current version | Version currently installed |
| New version | Version being installed |
| Source URL | Remote URL of the installation package |
| File name | Local filename used for the downloaded file |
| Target paths | Existing files or directories to remove |
| Downloaded action | Determines whether to skip extraction or extract a ZIP archive |
| Extraction target | Destination directory for extracted archive contents |

### Downloaded actions

- `none` — Skip archive extraction and finish the installation workflow.
- `unzip` — Extract the downloaded ZIP archive into the configured destination.

Other action values do not trigger either of these finalization branches in the current implementation.

## 📊 Installation Progress

The graphical interface receives status and progress updates from the Python backend.

Typical status messages include:

- `Downloading...`
- `Removing <path>...`
- `Extracting...`
- `Finalizing...`

The progress indicator is updated during the download, cleanup, and finalization stages. The current implementation uses predefined progress milestones rather than measuring the exact percentage of downloaded bytes.

## 🔒 Security and Reliability

UInstaller performs file operations and downloads from configurable locations. Before using it in production, consider the following precautions:

- Only use trusted download URLs and verify downloaded packages before installing them.
- Restrict cleanup targets to explicitly approved paths.
- Validate ZIP archive contents before extraction to prevent path traversal and unintended file overwrites.
- Handle download, filesystem, and extraction errors gracefully.
- Use checksums or digital signatures to verify package integrity.
- Avoid running the installer with elevated privileges unless required.
- Test updates against a temporary directory before deploying them to production systems.

**Important:** The current implementation removes configured targets before completing finalization. If downloading succeeds but cleanup or extraction fails, the previous installation may already have been removed. A staging directory and rollback mechanism would make updates safer.

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a Pull Request with a clear description.

## 📄 License

No license has been specified yet. Add a `LICENSE` file to define the terms under which the project can be used, modified, and distributed.

## 💡 Philosophy

UInstaller is designed to separate reusable installation logic from product-specific configuration.

Instead of building a new installer for every application, configure the product details, download source, cleanup targets, and finalization behavior — and reuse the same installation workflow.

**One installer. Different products. Simple deployments.**

