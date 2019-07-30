# Contribution Guidelines

The most important thing is that your code is well-documented and
easy-to-understand.

## Overall guidelines

Be a self-starter. Please make progress and move forward, don't ask
for permission unless your work will interfere with and negatively
impact other dev.

If you don't know something, that's okay. Just ask.

But conversely, don't waste our time asking us stuff you know the
answer to or can make a reasonable guess yourself. Just make your
decision and ask in MR comments if people want a different choice.

If I ask you for your opinion on something, and you don't know
enough to give me a good answer, just tell me. That's okay. I don’t
want you to copy-and-paste someone else's opinion, that is bad.


## README.md

The [`README.md`](README.md) file should be self-explanatory.

A new junior developer should be able to follow the `README.md` to get
your code running, and not have to look at any code.

As much as possible, you should be able to copy and paste the
`README.md` into the shell.  Minimize the number of times the user
must copy and paste. Comments should use `#` so that code blocks
can be pasted into the shell without the comments affecting the
runtime.

## Git workflow

Each time you are creating a new feature, create a git branch called
`feature/blahblahblah`.

Please try to create minimal slim MRs that are easy to review. Keep
orthogonal changes in separate MRs. If they depend upon each othen
then create sequential MRs that branch off each other.

When your code is ready for review, submit a merge request (MR) for
the team to review. Please make sure your code is tested both on
local and Heroku. It is not other dev's responsibility to Q+A your
work.

When you submit a MR, you should still continue working! Create a
new branch, off your old branch, and push code to your new branch
while we reviewing your old MR. Better yet, branch of master if the
MRs are parallel and not sequential.

### Code review

Please review other people's MRs.

If you make comments on the MR, indicate whether it should be separe1======

### Large files in Git

Please avoid checking large files (over 100KB) into a repo, they
clog up the history, they make it much more time consuming to pull
on a new machine, and they are hard to remove from the history.

If you need files over 100KB to get the code to run, use
[`git-lfs`](https://git-lfs.github.com/). It is easier for us to
take a `git-lfs` file and make it a proper `git` file than vice-versa.

### MR descriptions

If an MR requires a special command, put that in the description
of the MR, e.g.:

* `python app/migrate.py migrate`
* `npm build`
* etc.

If your MR closes an issue, write `Closes #XX` (issue number) in
the description.
