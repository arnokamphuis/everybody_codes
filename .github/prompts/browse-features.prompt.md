# Browse and Select an Open Feature Request

You are an expert engineering assistant integrated with this GitHub repository. Your goal is to help me find and select an open feature request to begin working on.

Please follow these steps:

1.  **Find Open Feature Requests**:
    * Access the GitHub issues for this repository.
    * Filter the issues to find all that are currently **open** and have a title that starts with `[Feature]`.

2.  **Display the Features**:
    * Present the list of found feature requests to me as a numbered menu.
    * For each issue, please include the following details:
        * Issue Title
        * Issue Number
        * Issue URL
        * The first paragraph of the issue's description.

3.  **Await My Selection**:
    * Ask me to choose a feature from the list by typing its number or pasting its URL.

4.  **Load the Feature Context**:
    * Once I have made a selection, retrieve the full description and context of the chosen issue.
    * At the same time, locate and load the corresponding markdown file from the `/possible-features/` directory. The filename will match the slugified version of the feature title (e.g., a feature titled `[Feature] User Authentication` would have a file named `feat-user-authentication.md`).

After you have loaded the issue details and the associated markdown file, confirm that the context is ready for me to begin implementation.