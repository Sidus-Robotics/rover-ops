# Git Setup

Git is a version control software that is considered the industry standard and used by Sidus Robotics. Gaining experience with Git is extremely relevant to anyone interested in the tech industry.

Git allows Sidus Robotics to collaboratively work across the software team/subteams while tracking changes. Our software repository is stored in the cloud through GitHub which uses Git.

## Installation

Before using Git ensure it is installed on your device. To do this enter this command in the shell...

```sh
git --version
```

If you get some output such as...

```txt
git version x.xx.x
```

If you have Git installed and can proceed with this guide. Otherwise, you need to install Git. You can follow [Git's documentation](https://git-scm.com/install/) to do so.

## Configuration

Git needs to know who you are to attach your credentials to your commits. To let Git know you need to configure it...

```sh
git config --global user.name "John Doe"
git config --global user.email "jdoe@email.com"
```

>**Note**: Use the same email you use for your GitHub account.

These commands will tell Git your name and email.

Something to take note of is the use of `--global`, this will set your entire machines configuration to use the defined name and email.

If you want to use more than one name and email you need to use `--local` while cd'ed in root of your repository. This will keep your configuration repository specific.

To check that you have correctly specified your configuration, enter...

```sh
git config user.name
git config user.email
```

The terminal will output your configured name and email.

### VSCode Extensions

Here is a list of VSCode extensions that interface with Git to make it easier to use.

- **[Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)**: View a Git Graph of your repository, and perform Git actions from the graph.

- **[GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)**: Supercharge Git within VS Code — Visualize code authorship at a glance via Git blame annotations and CodeLens, seamlessly navigate and explore Git repositories, gain valuable insights via rich visualizations and powerful comparison commands, and so much more

Furthermore the Source Control tab in activity bar of VSCode makes tracking your changes, commiting, and pushing/pulling much easier. This is a great alternative to using the terminal for Git.
