# Contributing to BytePSU's Discord Bot 

We're thrilled that you're interested in contributing to our project. Before you get started, please take a moment to read through this guide, as it will help you understand our development process and how you can make a meaningful contribution.

## Table of Contents

1. [Getting Started](#getting-started)
    - [Creating an account](#creating-an-account)
    - [Joining the organization](#joining-bytepsu)
    - [Cloning the repo](#cloning-the-repo)
2. [Making Changes](#making-changes)
    - [Branching](#branching)
    - [Commit Messages](#commit-messages)
    - [Push](#push)
3. [Merging Your Changes](#merging-your-changes)
4. [Tips](#tips)
5. [Code of Conduct](#code-of-conduct)
6. [Need Help?](#need-help)

## Getting Started

### Creating an account
In order to get started you need a GitHub account. If you don't already have one begin by [registering for an account.](https://github.com/join). 

### Joining BytePSU
Once you have an account, post a message in the club's Discord server to be added to the organization.   

### Cloning the repo
As a member of the organization you can clone the repo to your local machine machine. This will make a copy of the project you can work with. 

To use git, open a terminal, navigate to the folder of your choice, and run the following command to clone the repo.

```bash
git clone https://github.com/BytePSU/discord-bot.git
```

If you prefer to work in VS Code you can open a terminal by pressng <kbd>CTRL</kbd> + <kbd>`</kbd> and use the previous command. If you prefer to use the GUI you can [follow these instructions.](https://www.geeksforgeeks.org/how-to-clone-a-project-from-github-using-vscode/)

Now you're ready to make changes and contribute!

## Making Changes 

### Branching 
Before you start working on a new feature or bug fix, create a new branch. A branch is your personal work area where you can code without affecting other programmers: 
```bash
git checkout -b BranchNameHere
```
Make sure your branch name (BranchNameHere) is descriptive and unique.

In VS Code you can use the version control GUI on the left hand side to create a new branch. If you are new to VS Code this [YouTube Video will help you get started.](https://www.geeksforgeeks.org/how-to-clone-a-project-from-github-using-vscode/) 

### Commit Messages
Commit messages can be thought of as snapshots or saved states. Making a commit will save a copy fo the current state of your project folder.

```bash
git commit -m "commit message"
```
Where commit message is a description of your commit. Here are some tips when creating a message:

- Use present tense (e.g "Add Feature" not "Added Feature")
- Start with a capitalized verb (e.g., "Fix," "Add," "Update").
- Reference any related issues or pull requests.

### Push 
The commits you have made are local and on your machine. To send a copy of them to GitHub, you need to push them.

```bash
git push
```

In VS Code, the ... menu in the souce control panel (<kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>G</kbd>) will allow you to push commits to GitHub. 

## Merging your changes
1. Visit your branch on GitHub and click on "Compare & pull request" for the branch you just pushed.
2. Provide a descriptive title and summary for your pull request.
3. Mention any related issues or pull requests in your description.
4. Submit your pull request, and our project managers will review it as soon as possible.

## Tips
- Never work directly in the main branch.
- Use a new branch when you are working on a new feature.
- Don't wait too long before merging your branch into main.
- Your branch won't affect anyone else so don't be afraid to try things out. If you make a mistake you can return to a previous commit or delete the branch and start over.
- You don't have to work in VS Code. Any program that supports git will work. The steps will be the same but the location of the options will be different.

## Code of Conduct 
Please read and follow our Code of Conduct. We expect all contributors to be respectful and create a welcoming environment for everyone.

## Need Help? 
If you have questions or need assistance, feel free to reach out to us on our Discord server or create an issue on GitHub.

Thank you for your contribution! We appreciate your help in making BytePSU's Discord Bot even better.