ggit
======

`ggit` is a simple Python tool to find and list git repositories on your system

Usage
------

To find all git repositories on your system, call `ggit find`. This does a system `find`
call, and caches the results in the text file `~/.ggit/repolist.txt`

To list all of your repositories, use `ggit list`. Using `ggit list` with the option
`-c` will also print a `*` in front of the repos with uncommitted changes. You can print
the locations in an abbreviated form by using the option `-a`, possibly followed by a 
digit. For example, `ggit list -c -a 3` will print the path of your git repos starting
from their third parent.

You can use `ggit count <object-type>` to count objects of most common types within each
repository. For example, `ggit count commit` will print out a list of your repositories,
followed by the number of commits in that repo. Supported object types include: repos, 
commits, branches, tags, blobs, and trees.

TODO
------

+ [ ] add option to restrict `count` to certain repos
+ [ ] maybe some fun stats, like avg commit message length, % changed between commits, etc 
(but probably don't need to do anything like what GitHub already has...)
