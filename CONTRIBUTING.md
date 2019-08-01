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

Issues should not take longer than 4-5 days from start to being
merged. If you think it will take longer, break down the issue into
smaller pieces that can be done on this timescale. If an MR is
taking this long, please ask for help to finish.

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

### Creating an MR

* Please try to create minimal slim MRs that are easy to review.
* Keep orthogonal changes in separate MRs.
* If they depend upon each other then create sequential MRs that
branch off each other.
* You are welcome to submit work-in-progress MRs, but put "[WIP]"
in the title and don't ask for review until the MR is ready for
review (see below). However, if you do have architectural or
implementation questions, you are free to ask for feedback.
* If your MR changes the UX, please include screenshots of the new
UX in the description of the MR.

### MR Code review

It is not other dev's responsibility to Q+A your work.

Before making your MR, make sure you verify: 
1) Make sure your code is tested both on local and Heroku.
2) Run `python app/manage.py test` on local, all tests should pass.
3) Running `faker.py` if you have changed it.

The instructions on how to do above is mentioned in `README.md`. 

When your code is ready for review, submit a merge request (MR) for
the team to review.

When you submit a MR, you should still continue working! Create a
new branch, off your old branch, and push code to your new branch
while we reviewing your old MR. Better yet, branch of master if the
MRs are parallel and not sequential.

### Code review

Please review other people's MRs.

If you make comments on the MR, the person can fix it immediately.
However, if it is a larger change, the reviewer or the MR submitter
can comment that it could be separate MR (and maybe needs a new
issues). Either the reviewer or the submitter can create the new
issue. Only after the issue is created can the comment be resolved.

When someone makes a comment, please don't say: "Yes" or "Great"
or "Okay" or "I'm working on it", it just makes the gitlab notifications
too chatty. Instead, just resolve the comment when it is done.

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
* `npm install`
* `npm build`
* etc.

If your MR closes an issue, write `Closes #XX` (issue number) in
the description.

## Coding conventions

1) If you want to change a code convention that other developers
have been using, you propose that on channel and get buy in from
other devs.
2) You don't just change the convention in one single line, you do
it project-wide.
3) You don't mix refactoring or style changes with feature MRs. Do
it one separate MR because it breaks a lot of things, has a huge
diff, and it's hard to see what's a style change and what's a feature
change.

Ideally, we would move to PEP8 and have coding standard enforced
through a Pycharm config file:
[!134](https://gitlab.com/ftwlegal/clsite/issues/134)
