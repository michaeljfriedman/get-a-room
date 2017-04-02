/* slidePanel.js
 * Author: Michael Friedman
 *
 * Custom behavior that loads building stats into the slide panel on clicking
 * a building.
 */

// Defines what the side panel does on-click
$('.sample-button').on('click', function() {
    $.slidePanel.show({
        url: 'http://localhost:8000/slide-panel/frist-campus-center',
        settings: {
            method: 'GET'
        }
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
});
