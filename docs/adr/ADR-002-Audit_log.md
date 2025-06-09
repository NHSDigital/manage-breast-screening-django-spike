# ADR-002: Audit log

> |              |                     |
> | ------------ | ------------------- |
> | Date         | `09/06/2025`        |
> | Status       | `RFC by 12/06/2025` |
> | Deciders     | `Manage team`       |
> | Significance | `Security`          |
> | Owners       | @matmoore           |

---

## Context

Our service will contain personal data that we need to protect the integrity of.

We need the capability to audit changes to data stored by the app, so that we can quickly understand what happened in the event that something went wrong due to an unathorised change or bug in the application.

## Decision

### Assumptions

- We will not build functionality off of the history tables. They will be solely used for audit purposes.

### Drivers

The solution should:

- capture the user who made the change
- be well maintained and tested, keeping pace with the Django release cycle
- be well documented
- make it easy to interrogate the audit log

### Options

- django-simple-history
- django-auditlog
- django-reversion
- pgAudit, or other SQL-level solutions

django-auditlog and django-simple-history look very similar and work in much the same way (hooking into the `post_delete`, `post_save` and `pre_save` signals emitted by Django models), however, django-simple-history seems like the better maintained library. django-auditlog has had less releases (11 vs 48) and is not tested against the most recent version of Django (5.1 vs 5.2).

Both of these two options provide middleware for capturing the user who made the change and storing that on the audit record.

django-reversion is similar but seems more focused on the use case of reverting specific models to a previous version, rather than auditing all the things. This package is also lighter on documentation, and does not test against the latest version of Django (5.0 vs 5.2).

There are particular kinds of updates that aren't captured by any of these libraries:

- [bulk creation/updates of records](https://django-simple-history.readthedocs.io/en/latest/common_issues.html#bulk-creating-and-queryset-updating)
- SQL level updates, e.g. in data migrations
- [cascading deletes](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)

These issues can be worked around by manually creating audit records, and django-simple-history provides some [helper functions to assist with bulk create/update operations](https://django-simple-history.readthedocs.io/en/latest/common_issues.html#bulk-creating-a-model-with-history).

In the case of cascading deletes, we should setup our `ForeignKey` fields to *not* cascade delete to avoid cases where records are deleted but we forget to audit the deletion.

One limitation of django-simple-history called out in the documentation is that it breaks [F expressions](https://docs.djangoproject.com/en/5.2/ref/models/expressions/#f-expressions) i.e. inserting/updating a field based on another field. We do not use these anywhere in the app so far.

SQL-level solutions can potentially capture more changes automatically, but at the cost of being harder to interpret, and requiring more infrastructure setup compared to installing a python library. We also lose the ability to trace each change back to an application user.

### Outcome

Use `django-simple-history` to implement an audit log. For each model in the app, there will be a corresponding "history" model that stores past versions of the changes.

During development of the service, we can use its Django admin functionality to inspect the audit log.

### Rationale

`django-simple-history` is a mature library that is still being actively maintained and tested against up-to-date Django versions. It is well documented, and the documentation clearly points out its limitations.

## Consequences

- calls to `model.save()` or `model.delete()` are automatically audited.
- bulk creation/updates/deletes must be rewritten to take into account the history tables. This will be less efficient in some cases, e.g. [QuerySet updates cannot be used](https://django-simple-history.readthedocs.io/en/latest/common_issues.html#queryset-updates-with-history-updated-in-django-2-2).
- any new model methods or model manager methods that create/update/delete data must be written to handle auditing.

## Compliance

This change will be successful if:

- auditibility becomes part of the definition of done for new tickets; in particular, the team need to be aware that bulk operations are not automatically audited.
- we don't find ourselves limited by the restriction on using `F` expressions.
- we actively use the audit log to answer data questions.

## Notes

- [Jira ticket](https://nhsd-jira.digital.nhs.uk/browse/DTOSS-9251)

## Tags

`#security` `#observability`
