# Frontend (UI)

Below is the directory structure that frontend developers will work with.

```
- get_a_room_app/
  - static/
    - css/
      - styles.css
    - js/
      - mapbuilder.js
      - places.js
      - slidePanel.js
  - templates/
    - index.html
    - slide-panel.html
  - tests.py
```

## Frontend code
The frontend is written in HTML, CSS, and JavaScript. `templates/` contains the HTML files, while `static/` contains the CSS and JavaScript code. The files listed above are the ones we write our code in, and the other files we have not listed are CSS/JS libraries.

HTML:
- `index.html` defines our main page - the map page. It loads the map interface code from `mapbuilder.js` (see below).
- `slide-panel.html` defines the layout for the side panel that appears when users click a building on the map.

CSS:
- `styles.css` contains our custom defined styles for the entire app. We use the Bootstrap framework for styling.

JS:
- `mapbuilder.js` defines our map interface. This was built with the Leaflet JS library. See the [Leaflet documentation](http://leafletjs.com/reference-1.0.0.html) for a reference on how to use it.
  
  To populate the map, we make requests to the backend database through our web API for study space occupancy stats, geographic coordinates of the campus' buildings, and other data. See the [Backend](backend.md) section for the API specification (i.e. requests and the format of data returned by them) and other details.
- `places.js` contains static data about campus buildings: GPS coordinates, names, etc. It is a once-generated file, and it was once used to populate the database with this data- it does not need to be modified.
- `slidePanel.js` defines the behavior of the side panel that appears when a user clicks a building on the map.


## Testing
Write any frontend tests in `tests.py`. Use the [Django’s testing documentation](https://docs.djangoproject.com/en/1.11/topics/testing/) as a reference for this.

## Dependencies
Below we list the dependencies (libraries, frameworks, etc.) used in the frontend, and what we use them for. Update this list as more dependencies are added.

- Bootstrap CSS/JS: Standard CSS/JS framework.
- jQuery Slide Panel: JavaScript library and CSS styles for our side panel.
- Leaflet 1.0.0-beta.2 CSS/JS: JavaScript map library and corresponding CSS styles. Used to create our map interface.
- [Leaflet Locate Control](https://github.com/domoritz/leaflet-locatecontrol): Leaflet CSS/JS plugin for finding a user's geolocation.