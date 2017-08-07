# Developer Guide

## In-depth Guides
- [Project Setup](project-setup.md)
- [Frontend](frontend.md)
- [Backend](backend.md)
- [Deployment](deployment.md)
- [Appendix](appendix.md)

## Overview
The app is built using a HTML/CSS/JS frontend and a Django backend, deployed on Heroku. These components are documented for developer purposes in the pages [Frontend](frontend.md), [Backend](backend.md), and [Deployment](deployment.md) respectively. If you plan to contribute to the project, check out our [Project Setup](project-setup.md) guide to set up your development environment, and make sure to read the [Appendix](appendix.md) for our policies, workflow, code conventions, etc.

Below we provide a brief overview of the project's directory structure:

```
- get_a_room_app/
  - static/
    - css/
      - styles.css
    - js/
      - mapbuilder.js
      - places.js
  - templates/
    - index.html
    - slide-panel.html
  - models.py
  - tests.py
  - urls.py
  - views.py
- get_a_room/
  - settings.py
```

`get_a_room_app/` contains the components of the app: the models, views, and controllers. This is where both frontend and backend developers will spend most of their time. `get_a_room/` contains the configuration settings that apply to the entire project. Generally, these configurations do not need to be changed, but they are documented in the [Django settings documentation](https://docs.djangoproject.com/en/1.11/ref/settings/) in case they need to be changed in the future.

See the dedicated pages on frontend and backend for more details.






