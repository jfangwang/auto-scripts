# What is git-lazypush?
Tired of typing git add, git commit, and git push? Git-lazypush does all that for you

* Git lazy is a bash script that automates git add, commit, and push with custom commit messages
# How to install
1. Clone, cd, and pull the repo into your bash terminal
1. Once your in the directory, run `./install_git_lazy.sh`
	* install_git_lazy.sh literally makes the bash script executable and stores it in your bin directory
	* It is also a sudo command since it is entering to your /bin dir so provide your admin password when it prompts you to
1. You're all set!
# Usage of git-lazypush
* It is a command stored in bin so to use it, type `git lazypush yourCommitMessage`
* Quotes are not necessary when typing your message :)
* This command will not know if your head is untracked or not so use it when you know everything is stable

