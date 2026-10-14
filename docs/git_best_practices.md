# Git Best Practices

## Branches

### Switching Branches

To switch from one branch to another

```sh
git branch
```

```txt
On branch main
Your branch is up to date with 'origin/main'
```

You are on branch main, now enter...

```sh
git checkout existing-branch
```

You should get an output...

```txt
Switched to branch 'existing-branch'
Your branch is up to date with 'origin/existing-branch'
```

You have now successfully switched from branch `main` to `existing-branch`.

### Creating a New Branch

Before creating a branch, ensure you are on the branch you want to branch of off.

```txt
git branch
```

```txt
On branch main
Your branch is up to date with 'origin/main'
```

Here I am on the main branch, this ideal unless you want to branch off a feature branch.

```txt
git checkout...
```

```txt
```

#### Naming Convention

When naming a branch you want to follow our naming convention. 

```txt
initials-feature-futher_detail...
```

For example, if I were named John Doe and working on the docker container, I might name my feature branch as the following...

```txt
jd-docker-mac
```

This communicates to my teammates that me, **John Doe**, is working on the **docker** setup for **mac**.

```txt
jd-jd-docker-linux
```

Another example may be when you are collaborating, in this case, **John Doe and Jane Doe** are working on the **docker** setup for **Linux**.

#### Work Scope

Another major focus is to properly scope your work to your branch, this helps with pull requests when merging feature branches into the main code.

With this in mind, do your best to keep the work you are doing on your branch within the scope described in the naming of your branch.

### Merging Branches

## Pushing / Pulling

## Commiting
