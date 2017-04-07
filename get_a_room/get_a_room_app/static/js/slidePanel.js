/* slidePanel.js
 * Author: Michael Friedman
 *
 * Custom behavior that loads building stats into the slide panel on clicking
 * a building.
 */

// Defines what the side panel does on-click
$('.sample-button').on('click', function() {
    // Make AJAX request to get building stats
    $.ajax({
      url: 'http://localhost:8000/stats/building/frist-campus-center',
      success: function(result) {
        // Parse JSON response and populate view
        var buildingStats = JSON.parse(result);
        var content =  // this is a **horrible** way to populate the view, but I don't know how else to do it!
          `<h1>` + buildingStats.name + `</h1>
          <div class="my-wrapper">
          <table id="table">`;
        for (i = 0; i < buildingStats.rooms.length; i++) {
          var room = buildingStats.rooms[i];
          content +=
            `<tr class="tablerow">
              <td>` + room.number + `</td>
              <td>` + room.occupancy + ` / ` + room.capacity + `</td>
            </tr>`
        }
        content +=
         `</table>
          </div>
          <a href="#" class="close">Click to close</a>`;

        // Slide out the panel with the content
        $.slidePanel.show({
          content: content
        }, {
          direction: 'right',
          closeSelector: '.close',
          useCssTransforms3d: true,
          useCssTransforms: true,
          useCssTransitions: true,
          loading: {
              template: function(options) {
                  return '<div class="' + options.classes.loading + '"><div class="spinner"></div></div>';
              }
          }
        });
      }
    });
});
