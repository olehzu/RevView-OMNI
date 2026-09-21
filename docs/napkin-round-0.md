# Napkin Round 0: RevView-OMNI

## 1. Shape

RevView-OMNI is a web-based workflow and integration application that helps coordinate and automate the company’s code review process across Jira, Subversion, and Jenkins.

```text
[Review workflow]
	|
[Web interface] -- [Jira integration]
	|
[Subversion integration]
	|
[Jenkins build and test results]
```

## 2. The hard part

The hardest part is learning the client’s real code review process and translating it into reliable automation while working with systems that the team may not be able to access directly.

## 3. Bottleneck

The project is most likely to break under the constraints of a five-person team, especially when requirements, system access, integration details, and client preferences are still uncertain. The primary bottleneck is not expected user load; it is implementing and testing integrations without complete access to the company’s systems.

## 4. Stack

We would build the application with HTML and CSS for the interface and Python for the backend because the team already knows these technologies, while using documented interfaces or approved integration methods for Jira, Subversion, and Jenkins.

## 5. Kill risks

1. If the team cannot obtain usable access, credentials, documentation, or test environments for Jira, Subversion, or Jenkins, the integrations cannot be implemented or validated against real workflows.

2. If the client’s code review process differs between teams or is not documented clearly, the application may automate the wrong process and require major rework.

3. If company security policies prohibit the application from connecting to or storing information from these systems, the planned integration-based design may not be deployable.

## 6. Verdict

Yes, the project appears feasible for this team and timeframe, but only if the core workflow and integration access are confirmed early. The first things to cut would be full automation of every review step and any nonessential integration. The MVP should prioritize displaying review status and coordinating the workflow, with deeper Jenkins or Subversion automation added only when access and requirements are confirmed.