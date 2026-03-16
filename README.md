# ZERODAY Widget

![ZERODAY Logo](https://img.shields.io/badge/Status-Beta-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**ZERODAY** is a minimalist, elegant desktop sticky note widget designed for productivity and quick capture. Built with Python and PyQt6, it provides a distraction-free way to manage your daily tasks directly from your desktop.

## 🚀 Features

- **Minimalist Aesthetics**: Sleek glassmorphic design with a dark theme, optimized for modern desktop environments like Wayland and Hyprland.
- **Markdown Integration**: All tasks are automatically synchronized with `~/Desktop/TODO.md`. Use the widget or edit the file directly—it stays in sync.
- **Multi-Monitor Awareness**: Automatically spawns an instance on every connected display, keeping your notes accessible wherever your cursor is.
- **File System Watcher**: Instant updates. If you edit your TODO file in another editor, the widget refreshes in real-time.
- **Lightweight & Fast**: Extremely low resource footprint, designed to sit quietly in the background.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/callmeATHUL/zeroday-widget.git
   cd zeroday-widget
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then install PyQt6:
   ```bash
   pip install PyQt6
   ```

3. **Run the widget**:
   ```bash
   python zeroday_widget.py
   ```

## 🎨 Customization

You can modify the look and feel by editing the `style.qss` file. The widget uses standard Qt Style Sheets, allowing for deep UI customization.

## 🔮 Future Improvements & Features

We're constantly looking to improve ZERODAY. Here's what's on our roadmap:

- [ ] **Cloud Sync**: Optional synchronization with GitHub Gists or cloud providers.
- [ ] **Categories & Tags**: Organize tasks with custom categories and color-coded tags.
- [ ] **Transparency Controls**: Adjustable background opacity sliders within the widget.
- [ ] **Interactive Reminders**: System notifications and reminders for high-priority tasks.
- [ ] **Drag-and-Drop**: Reorder tasks easily via the UI.
- [ ] **Custom Themes**: A collection of built-in themes (Amoled, Nord, Gruvbox, etc.).

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Created with ❤️ for the open-source community.*
