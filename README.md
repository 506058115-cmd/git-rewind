# git-rewind

Your repository's tiny on-this-day time machine. It finds a commit from a previous year that was made on today's date, using only your local Git history.

## Use it

Requires Python 3.8+ and Git. No packages to install, and no network access.

```sh
python git_rewind.py /path/to/your/repository
```

On Windows, `py` works too:

```powershell
py .\git_rewind.py C:\path\to\your\repository
```

Leave out the repository path to use the current directory. Pick a date with `--date`:

```sh
python git_rewind.py . --date 2024-05-01
```

If no anniversary exists, git-rewind picks a random earlier commit instead. It scans at most the latest 5,000 commits across local refs.
It only prints a commit summary; it does not check out a commit or change the working tree.

## Privacy

Commit history is read from the local repository and stays on your computer. git-rewind makes no network requests.
Control characters in commit subjects are escaped before display so repository text cannot issue terminal control sequences.

## License

MIT. See [LICENSE](LICENSE).
## Linux x86_64 downloads

- [Single-file build](https://github.com/506058115-cmd/git-rewind/releases/download/v1.0.0/git-rewind-linux-x86_64-onefile.tar.gz)
- [Directory bundle](https://github.com/506058115-cmd/git-rewind/releases/download/v1.0.0/git-rewind-linux-x86_64-onedir.tar.gz)
- [v1.0.0 release page](https://github.com/506058115-cmd/git-rewind/releases/tag/v1.0.0)

The archives include build information and third-party license notices. The release also provides SHA-256 checksums. Built on WSL Ubuntu 24.04 with Python 3.12.3 and PyInstaller 6.22.2 for GNU/Linux x86_64. Older distributions may need a compatible glibc. Running this tool also requires system Git on PATH.
