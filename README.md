# AUTOPULL
A script by BromTeque

The release binary is only compatible with Linux as of now. Windows binaries are on the TODO list. Use WSL if you wish to run the binary on Windows. Alternatively create your own Windows binary with PyInstaller or run the python script "raw".

# USAGE AND OPTIONS

Download the autopull release binary.

First run

```chmod +x autopull```

then

```./autopull -u <GitHub username>```

,alternatively (for debug)

```./autopull -du <GitHub username>```

## General options:
    --version,                          Prints version number
## Required options:
    -u, --username <GitHub Username>    GitHub username to get repositories from
## Optional options:
    -d, --debug                         Changes logging to debug mode


    
# TODO

 - Add license
 - Windows release binary
 - Add LFS support
 - Add submodules support
 - Platform-agnostic autopulling ([Like this](https://github.com/BromTeque/bromchive/blob/master/pull.py))
 - Reconsider approach. Should it be "CLI-like" or cron-friendly? Both? Recocnsider logging method.
