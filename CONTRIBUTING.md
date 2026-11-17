
# Contributing Guidelines

Thank you for contributing to the Employee Management System project.

These guidelines describe the development workflow followed by the project team.

## 1. Project Collaboration

The project is developed by two team members using Git and GitHub.

Each member works on a separate feature branch to keep development organized.

## 2. Branch Naming Convention

The following branches are used:

- `main` - Main stable project branch.
- `feature-member1` - Member 1 development branch.
- `feature-member2` - Member 2 development branch.

New features should be developed on their respective feature branches.

## 3. Development Workflow

Follow these steps when contributing:

1. Clone the project repository.
2. Switch to the assigned feature branch.
3. Implement the required changes.
4. Test the application locally.
5. Stage the modified files.
6. Create meaningful Git commits.
7. Push the feature branch to GitHub.
8. Create a Pull Request targeting `main`.
9. Review the proposed changes.
10. Resolve feedback and merge approved changes.

## 4. Commit Message Convention

Use clear and descriptive commit messages.

Examples:

- `feat: add employee management functionality`
- `fix: correct employee form validation`
- `docs: update project documentation`
- `style: improve navigation layout`
- `test: add database operation tests`
- `security: implement CSRF protection`

Each commit should represent a meaningful unit of work.

## 5. Code Quality Guidelines

- Use meaningful variable and function names.
- Follow consistent Python indentation.
- Keep functions focused on individual responsibilities.
- Avoid committing unnecessary files.
- Test changes before pushing them.
- Do not commit passwords, secret keys, or sensitive employee information.

## 6. Testing

Before submitting a Pull Request, check Python syntax:

```bash
python -m py_compile app.py models.py database.py
```

Check whitespace errors:

```bash
git diff --check
```

Also test the affected application pages in a browser.

## 7. Pull Request Guidelines

Every feature branch should be submitted through a Pull Request.

A Pull Request should include:

- A clear title.
- A description of the implemented changes.
- Relevant screenshots when appropriate.
- Testing information.
- Review and approval before merging.

## 8. Merge Conflict Resolution

If two branches modify the same lines of a file, Git may report a merge conflict.

Contributors should:

1. Identify the conflicting file.
2. Inspect the conflicting sections.
3. Discuss which changes should be retained.
4. Resolve the conflict carefully.
5. Test the updated application.
6. Commit the resolution.

## 9. Team Responsibilities

| Member | Responsibilities |
|---|---|
| Member 1 | Backend, database, CRUD operations, dashboard analytics and security |
| Member 2 | Error pages, error handling, navigation, footer and documentation |

## 10. General Guidelines

Contributors should communicate changes clearly, preserve existing functionality, and maintain accurate project documentation.

Thank you for contributing!

