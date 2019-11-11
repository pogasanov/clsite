// Make sidebar sticky
const Sticky = require('sticky-js');
const sticky_sidebar = new Sticky('.sidebar');

// Scrollspy on profile sections to select item in sidebar
const sections = document.querySelectorAll(".profile-block");
const links = document.querySelectorAll(".sidebar-item")

function get_sections_id_with_position() {
    const sections_id_with_position = {};
    Array.prototype.forEach.call(sections, function (e) {
        sections_id_with_position[e.id] = e.offsetTop;
    });
    return sections_id_with_position
}

export function profile_sidebar_update_active() {
    const sections_id_with_position = get_sections_id_with_position()
    for (let [section, position] of Object.entries(sections_id_with_position)) {
        if (position >= document.documentElement.scrollTop) {
            links.forEach(link => {
                delete link.dataset.active
            })
            document.querySelector(`.sidebar-item a[href*=${section}]`).closest('.sidebar-item').dataset.active = true
            break
        }
    }
}

window.onscroll = profile_sidebar_update_active