# Enterprise Archive Server

A menu-driven Linux System Administration micro project built with Bash and standard Linux commands. The program creates and searches compressed archives, extracts them into separate folders, backs up and restores project files, reports storage use, demonstrates file permissions, and records actions in a log.

## Team and responsibilities

- Avinash K — Linux System Administrator
- V Rishith — Storage and Backup Administrator
- Ragavendra Raju K S — Automation and Security Engineer
- N Nithish Kumar — Testing, Documentation and Presentation Lead

Please verify the spelling and student IDs with your team sheet before using them in your final submission. The screenshot renders some IDs in scientific notation, so they are not copied here.

## Problem this project addresses

Server files and project records can accumulate over time. Administrators need a simple way to create compressed archives, find files in an archive, recover data, check available storage, and review administrative actions. This project puts those common tasks behind a guided terminal menu and validates user input before acting.

## Requirements

- Ubuntu or another Linux distribution with Bash
- Standard commands: `tar`, `gzip`, `find`, `grep`, `df`, `du`, `chmod`, `ls`, `date`, and `tail`
- No third-party packages are required

The optional browser dashboard uses BusyBox `httpd` to run Bash CGI locally. The core terminal project does not need this package.

## Start the project

1. Open a Linux terminal.
2. Create the project folder and enter it:

   ```bash
   mkdir -p ~/enterprise-archive-server/scripts
   cd ~/enterprise-archive-server
   ```

3. Create the main script using Nano:

   ```bash
   nano scripts/archive_server.sh
   ```

4. Copy the contents of the delivered `archive_server.sh` into Nano. Save with **Ctrl+O**, press **Enter**, then exit with **Ctrl+X**.
5. Make the script executable and start the menu:

   ```bash
   chmod +x scripts/archive_server.sh
   ./scripts/archive_server.sh
   ```

The script makes its `archives`, `backups`, `restored`, `logs`, and `data` folders on its first run.

## Optional website frontend

The project also includes a browser dashboard. Its buttons submit forms to a Bash CGI script, which calls the same archive functions and uses the same project folders as the terminal menu. This is a local demonstration deployment, not a public website.

1. In Ubuntu, install BusyBox once if the `busybox` command is missing:

   ```bash
   sudo apt update
   sudo apt install busybox
   ```

2. From the project folder, start the local web server:

   ```bash
   cd ~/enterprise-archive-server
   bash scripts/start_web.sh
   ```

3. Open `http://127.0.0.1:8080` in Chrome while leaving that terminal window open. The server binds to `127.0.0.1`, so it is available only from this computer. Press **Ctrl+C** in the terminal to stop it.

4. Use the dashboard forms. For the archive demo, first create the sample files from the feature demonstration above; enter `/home/<your-ubuntu-username>/archive-demo/source` as the source path. A different port can be selected with `bash scripts/start_web.sh 8081`.

The website interface does not replace the required Bash terminal menu. Demonstrate both if the instructor wants a frontend. Do not expose this basic local demo server to the internet or another network.

## Feature-by-feature demonstration

Use a second terminal, or exit the program and run these setup commands before testing:

```bash
mkdir -p ~/archive-demo/source
printf 'Quarterly archive server demo\n' > ~/archive-demo/source/notes.txt
printf 'Linux administration practice\n' > ~/archive-demo/source/linux.txt
```

Then run `~/enterprise-archive-server/scripts/archive_server.sh` and try:

1. **Create archive:** choose `1`; enter `~/archive-demo/source`; enter `quarterly_demo`. A `.tar.gz` appears in `archives/`.
2. **List archives:** choose `2`; confirm `quarterly_demo.tar.gz` is listed.
3. **Search:** choose `3`; select `quarterly_demo.tar.gz`; search for `linux`. The matching archived path should appear.
4. **Extract:** choose `4`; select the archive; inspect the new folder under `restored/`.
5. **Backup:** choose `5`; confirm a dated `project_backup_*.tar.gz` under `backups/`.
6. **Restore:** choose `6`; enter a listed backup name; inspect the dated restore folder under `restored/`.
7. **Disk use:** choose `7`; review the `df` and `du` output.
8. **Permissions:** choose `8`; enter `640`; confirm the mode changes on `data/permission_demo.txt`. Try `999` to demonstrate validation.
9. **Activity log:** choose `9`; confirm actions and timestamps appear.
10. **Input validation:** enter `x` at the menu, an empty archive name, or a missing source path and show the clear error message.

Each menu action waits for Enter before showing the menu again. Menu option `0` exits.

## Optional scheduled backup

The included `crontab.example` runs a project backup daily at 6:00 PM. First replace `/home/your-user` with the output of `echo "$HOME"` on your Linux VM. Then install the line with `crontab -e`. Confirm it with `crontab -l`. Cron availability and service commands differ by distribution; scheduled backups are optional and the menu backup works without cron.

## Project folders created at runtime

- `archives/` — user-created compressed archives
- `backups/` — compressed project backups
- `restored/` — separate destination for extracted data and restored backups
- `logs/activity.log` — timestamped activity history
- `data/permission_demo.txt` — safe sample file for chmod demonstration
- `scripts/archive_server.sh` — main Bash menu and functions
- `web/index.html`, `web/style.css` — browser dashboard
- `web/cgi-bin/archive.cgi` — Bash CGI bridge to the project functions
- `scripts/start_web.sh` — starts the loopback-only local web demo

## Safety and limitations

Archive extraction checks for absolute paths and `..` path components and always extracts into a new project subfolder. Choose input files outside the project folder when creating an archive. Backup restore writes into a new folder; it does not overwrite the live project. The project logs menu actions locally and does not provide remote access, user accounts, or encryption.
