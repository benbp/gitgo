This is a tool to help manage batches of git repositories, such as viewing
and changing of branches of all repos within a directory. It is intended to aid
with the use of git within a Golang workspace, in order to make development that
involves dependencies and branches across repositories easier.

***Installation***

Move gitgo to somewhere in your path, and make it executable.

***Examples:***

**Switch to different branches across multiple repos as defined in a template**

```
gitgo -p my_project
```

**Git pull and checkout new branch on all subdirectories of repo1 and repo2**

```
gitgo pull 'checkout -b new_branch' -r repo1 repo2 
```

**Get status of all repositories owned by <owner>**

```
gitgo status -o benbp
```

**Enter relative paths instead**

```
gitgo 'remote show' ./dir1 ../dir2
```

**Show branches and remotes of selected repositories**

```
gitgo 'branch -a' 'remote show' -r packer gophercloud perigee
```

