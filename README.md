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

## Privacy

Commit history is read from the local repository and stays on your computer. git-rewind makes no network requests.

## License

MIT. See [LICENSE](LICENSE).
