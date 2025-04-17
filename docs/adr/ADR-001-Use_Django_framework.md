# ADR-nnn: Use Django framework

>|              |                                                                                                                                                                                    |
>| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
>| Date         | `17/04/2025` _when the decision was last updated_                                                                                                                                  |
>| Status       | `Proposed`                        |
>| Deciders     | `Team` |
>| Significance | `Structure` |
>| Owners       | @matmoore @malcolmbaig @gpeng |
---

- [ADR-nnn: Any Decision Record Template](#adr-nnn-any-decision-record-template)
  - [Context](#context)
  - [Decision](#decision)
    - [Assumptions](#assumptions)
    - [Drivers](#drivers)
    - [Options](#options)
    - [Outcome](#outcome)
    - [Rationale](#rationale)
  - [Consequences](#consequences)
  - [Compliance](#compliance)
  - [Notes](#notes)
  - [Actions](#actions)
  - [Tags](#tags)

## Context

We're deciding initial technologies for the service. We're working under the assumption we will be working in Python but need to decide on a framework.

[Reasons for adopting a framework are outlined in the quality framework.](https://github.com/NHSDigital/software-engineering-quality-framework/blob/6d5453d3ee0f9c7af1a4b48d2ec8cb72d9826460/practices/structured-code.md?plain=1#L24) Our app is not trivial enough to build without a framework, and we are assuming it will be fairly typical for a web application running
in the cloud: a stateless service that renders HTML from tempalates, an ORM that connects to a Postgres database, etc.

We're initially intending to productionise the [manage screening events prototype](https://github.com/NHSDigital/manage-screening-events-prototype). We're anticipating that we may build an additional gateway service that would be deployed inside trusts' networks, which this app would communicate with via a queue or API, but this is to be decided later.


## Decision



### Drivers

- We're building a web application with an accessible frontend, not a microservice
- Convention over configuration: the framework should provide reasonable, secure defaults, and be familiar enough for new team members joining the team
- Easy to get started with
- Easy to extend while maintaining separation of concerns
- Limited boilerplate

### Options

We considered the two most common frameworks in Python: Django and Flask. Both are stable, established frameworks, with large open source communities. Flask is on the Technology Radar, and is being used for several APIs. Django is not on the radar but is used by the [Transformation directorate website](https://github.com/nhsx/nhsx-website).

In addition to this repo, we created a [technical spike for Flask](https://github.com/NHSDigital/manage-breast-screening-flask-spike).

#### ORM

Django has a built in ORM and migrations framework. The Django ORM uses the simpler [ActiveRecord pattern](https://www.thoughtfulcode.com/orm-active-record-vs-data-mapper/), whereas a Flask app would use SQLAlchemy, which implements the Data mapper pattern.

Django's ORM is well documented and easy to get started with:
- [Models documentation](https://docs.djangoproject.com/en/5.2/topics/db/queries/)
- [Queries documentation](https://docs.djangoproject.com/en/5.2/topics/db/queries/)

Django ORM is less flexible and fully featured than SQLAlchemy. However, this is probably a case of YAGNI (you aint gonna need it) as we are not anticipating a lot of complex database queries.

Django also provides a [model form](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/) abstraction, that makes it very easy to generate form pages based on an ORM model, with minimal boilerplate.

In general, Django encourages a tightly coupled model layer, but this comes with the benefit that
the view / form / model abstractions work well together. It is possible to abstract away the ORM behind a service layer, but then you lose a lot of these helpful abstractions (e.g. model forms, pagination helpers etc).

#### Templating

Django has its own templating language, but it also supports Jinja.
With a few minor adjustments, we can reuse the NHS.UK frontend templates.

Flask uses Jinja by default.

#### Routing

Flask has a fairly robust routing system, using "blueprints" to organise and group routes in different parts of the app. Django has a comparable system which is also flexible and easy to keep organised.

#### View logic

Django includes [Generic class-based views](https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/), which can be used to reduce boilerplate in the view layer. The trade-off is they are a bit more unintuitive to work with compared to function based views. We have the option of using either or both.

Django has a [form abstraction](https://docs.djangoproject.com/en/5.2/topics/forms/) that simplifies the rendering and processing of form pages. The form layer is completely decoupled from the model layer, but you would typically use model forms as described above.

If we decide to build APIs, we can use [Django Rest Framework](https://www.django-rest-framework.org/) - a framework built on top of Django that handles serialisation/deserialisation, API authentication, and OpenAPI specifications.

#### Authentication system

Django comes bundled with an [authentication system](https://docs.djangoproject.com/en/5.1/ref/contrib/auth/) which handles accounts, permissions, and user sessions.

We would be using this in combination with an OIDC library such as [Django-AllAuth](https://docs.allauth.org/en/latest/) or [Authlib](https://docs.authlib.org/en/latest/client/django.html).

Flask would need auth built out manually using a library like flask-OAuth.

#### Learning curve

Django is a larger framework, so there is more to learn, but less moving parts.

Since the framework has more conventions for doing things than flask, it is easier to move between Django
projects, and if you get stuck it's a bit easier to find people who've solved the same problem before.

We have some Django knowledge on the team already, and Django is conceptually very similar to other major web frameworks such as Rails, which the team is already familiar with.

#### Code structure

Flask is completely flexible and unopinionated, meaning that every decision about where to put things will be up to this team. This could lead to a project structure that has more of a learning overhead for new developers.

Django has a more prescriptive structure, which potentially means a project structure that is more familiar to new developers.

Django encourages you to factor your Django project into modular [apps](https://docs.djangoproject.com/en/5.2/ref/applications/), rather than a single monolithic package. An app may correspond to a [bounded context in domain-driven design](https://martinfowler.com/bliki/BoundedContext.html) or a cross-cutting capability.

[It is possible to write apps in such a way that can be reused and configured in other projects.](https://docs.djangoproject.com/en/5.2/intro/reusable-apps/).

There is a large ecosystem of 3rd party apps available.

#### Security

Django has built in protections for common web app vulnerabilities, such as XSS, SQL injections, CSRF.

There is guidance and checklists in the [Django security guide](https://docs.djangoproject.com/en/5.2/topics/security/) and [How to deploy Django](https://docs.djangoproject.com/en/5.2/howto/deployment/).

Flask has basic session management and XSS protection via its use of jinja2 templates. Other protections would need to come from external libraries, which we'd need to select manually based on a list of common vulnerabilities.

#### Testing

Django comes with very good [testing tools](https://docs.djangoproject.com/en/5.2/topics/testing/tools/). Out of the box you can test database interactions (rolling back to a fresh state between tests), and emulated HTTP requests.

By default Django uses unittest as the test framework, but you can easily swap this out for [pytest](https://pypi.org/project/pytest-django/).

Flask also comes with a [test client](https://flask.palletsprojects.com/en/stable/testing/).

#### CLI

Flask has a basic CLI tool that allows for running a dev server, displaying app routes, and running a shell in the app context. All other convenience commands would need to be implemented manually.

Django has the manage utility for running administrative tasks, including running a server, migrations, an application shell, inspecting the database schema, etc. One notable absence is printing out app routes.

#### Summary of differences

The following is the minimum set of concerns that would require us to hand-roll our own setup under Flask (and for which Django already provides a solution):

- Project structure
- ORM / database setup
- Form rendering
- Security protections comparable to the built-in Django protections
- Helper scripts for common tasks

### Outcome

We decided to use Django on the basis that:

- The above represents a sizable amount of time and effort recreating things that are already available in Django
- It would involve the use of various Flask extensions in varying states of maintenance, as opposed to a single, well-maintained framework
- The security protections in particular are an area where it would be preferable not to roll our own, given the potential for leaving attack vectors open

## Consequences

Engineers on the team will need to learn Django. Some suggested learning resources:
- [Django documentation and first steps guide](https://docs.djangoproject.com/en/5.1/)
- Two scoops of Django 3.x by Daniel and Audrey Greenfield
- [Django Girls Tutorial](http://tutorial.djangogirls.org/en/index.html)
- [Django for Beginners](https://learndjango.com/courses/django-for-beginners/) / [Django for Professionals](https://learndjango.com/courses/django-for-professionals/)

[We should expect a new feature release of django roughly every eight months, and regular patch releases](https://docs.djangoproject.com/en/dev/internals/release-process/).

If we decide to build an API in the same service, we should look at [Django Rest Framework](https://www.django-rest-framework.org/)

## Compliance

N/A. We do not need measure anything specifically for this decision.

## Actions

- Run through [Django deployment checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)

## Tags

`#frameworks` `#libraries`
