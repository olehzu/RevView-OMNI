# Client note:


Signed the NDA with the client and briefly discussed the project idea.
The goal is to simplify and automate parts of the current avionics code review process while keeping human review and traceability.


# Business logic:


The current review process is very manual: authors need to collect checklists, create diffs, fill review records, get SVN information, run Jenkins builds, and notify reviewers.
The new system should centralize Jira, SVN, Jenkins, diffs, checklists, and reviewer comments into one workflow.
AI can help with summaries, file-change descriptions, and simple compliance checks, but should not replace reviewer judgment.


# Technical requirements:


Programming language: Python.
Integrate with Jira, SVN, and Jenkins.
Use a sandbox/mock environment because students cannot access the client’s production systems directly.


# Project requirements:


Can be developed on GitHub.
MVP must be completed by the end of this semester.
MVP should cover review creation, SVN diff generation, unified review workspace, basic automation/AI, notifications, and review closure.
