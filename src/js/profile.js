// Make sidebar sticky
const Sticky = require('sticky-js');
const sticky_sidebar = new Sticky('.sidebar');

// Scrollspy on profile sections to select item in sidebar
class ScrollSpy {
    constructor() {
        this.update_sections_id_with_position()
        document.addEventListener('scroll', this.profile_sidebar_set_active.bind(this), false)
    }

    update_sections_id_with_position() {
        let sections = document.querySelectorAll(".profile-block");
        this.links = document.querySelectorAll(".sidebar-item");
        let sections_id_with_position = {}
        Array.prototype.forEach.call(sections, function (e) {
            sections_id_with_position[e.id] = e.offsetTop;
        });
        this.sections_id_with_position = sections_id_with_position
    }

    profile_sidebar_set_active() {
        for (let [section, position] of Object.entries(this.sections_id_with_position)) {
            if (position >= document.documentElement.scrollTop) {
                this.links.forEach(link => {
                    delete link.dataset.active
                })
                document.querySelector(`.sidebar-item a[href*=${section}]`).closest('.sidebar-item').dataset.active = true
                break
            }
        }
    }
}

export const scrollspy = new ScrollSpy()