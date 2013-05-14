ggit
======

`ggit` is a simple tool to find and list git repositories on your system

Usage
------

To find all git repositories on your system, call `ggit find`.

To list all of your repositories, use `ggit list`. Using `ggit list` with the option
`-c` or `--check` will also print a `*` in front of the repos with uncommitted changes.

You can use `ggit count <object-type>` to count objects of most common types within each
repository. For example, `ggit count commits` will print out a list of your repositories,
followed by the number of commits in that repo. Supported object types include: repos, 
commits, branches, tags, blobs, and trees.

TODO
------

+ [ ] add option to restrict `count` to certain repos
+ [ ] maybe some fun stats, like avg commit message length, % changed between commits, etc 
(but probably don't need to do anything like what GitHub already has...)
