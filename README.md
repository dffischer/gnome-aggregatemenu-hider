# Gnome Shell Aggregate Menu Hider

This is a generator for Gnome Shell extensions that hide items from the aggregate menu. Use it to clean up removing unwanted items.

## Installation

Archlinux users have [packages in the AUR for all generated extensions](https://aur.archlinux.org/pkgbase/gnome-shell-extension-aggregatemenu-hider/).

### Manual Compilation

This project uses [waf](https://code.google.com/p/waf/) to compile and install.

```bash
waf configure install
```

### Selective Installation

Which extensions to generate can be selected with waf's `--targets` option.

```bash
waf --targets=Volume,User configure install
```

Use `waf list` to show all available variants.

## Extension

To create a new variant, add a line to [the table in `extensions.csv`](extensions.csv). It then shows up as a target for waf. The columns have the following meaning.

column      | explanation
------------|-------------
name        | Extension Name as it is displayed to the user.<br/>The first word should be unique as it will be used to identify the extension.
author      | Author name, also without spaces, as it will be part of the extension identifier.
item        | object path locating the entry to hide inside the menu.
description | Description of the extension as it is displayed to the user.

To find the object path, _looking glass_ is recommended. While in Gnome Shell, press <kbd>Alt</kbd> + <kbd>F2</kbd>, enter `lg` and hit return. Starting with `Main.panel.statusArea.aggregateMenu.` tab completion can be used to inspect the hierarchy. The entries already present in the table may serve as some starting points.
