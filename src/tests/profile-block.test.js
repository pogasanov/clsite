import {shallowMount} from '@vue/test-utils'
import profileBlock from '../js/components/commons/profile-block.vue'

describe('profile-block', () => {
    const EXPECTED_TITLE = 'Tested title';
    const EXPECTED_SECTION_ID = 'tested_id';
    const EXPECTED_SLOT_CONTENT = '<div>Tested slot</div>';

    it('is a Vue instance', () => {
        const wrapper = shallowMount(profileBlock);
        expect(wrapper.isVueInstance()).toBeTruthy()
    });

    it('renders correctly', () => {
        const wrapper = shallowMount(profileBlock, {
            propsData: {
                title: EXPECTED_TITLE,
                section_id: EXPECTED_SECTION_ID
            },
            slots: {
                default: EXPECTED_SLOT_CONTENT
            }
        });
        expect(wrapper.element).toMatchSnapshot()
    });

    it('set title', () => {
        const wrapper = shallowMount(profileBlock, {
            propsData: {
                title: EXPECTED_TITLE
            }
        });
        expect(wrapper.props().title).toBe(EXPECTED_TITLE);
        expect(wrapper.find('h2').text()).toBe(EXPECTED_TITLE)
    });

    it('set section id', () => {
        const wrapper = shallowMount(profileBlock, {
            propsData: {
                section_id: EXPECTED_SECTION_ID
            }
        });
        expect(wrapper.props().section_id).toBe(EXPECTED_SECTION_ID);
        expect(wrapper.find('section').attributes().id).toBe(EXPECTED_SECTION_ID)
    });

    it('detect if it has content', () => {
        let wrapper = shallowMount(profileBlock, {
            slots: {
                default: EXPECTED_SLOT_CONTENT
            }
        });
        expect(wrapper.find('.js-edit').exists()).toBe(true);

        wrapper = shallowMount(profileBlock);
        expect(wrapper.text()).toContain('information is hidden')
    });

    it('trigger edit and save', () => {
        const wrapper = shallowMount(profileBlock, {
            slots: {
                default: EXPECTED_SLOT_CONTENT
            }
        });
        wrapper.find('.js-edit').trigger('click');
        expect(wrapper.emitted().edit).toBeTruthy();

        wrapper.find('.js-save').trigger('click');
        expect(wrapper.emitted().edit.length).toBe(2)
    });

    it('trigger edit and cancel', () => {
        const wrapper = shallowMount(profileBlock, {
            slots: {
                default: EXPECTED_SLOT_CONTENT
            }
        });
        wrapper.find('.js-edit').trigger('click');
        expect(wrapper.emitted().edit).toBeTruthy();

        wrapper.find('.js-cancel').trigger('click');
        expect(wrapper.emitted().cancel).toBeTruthy()
    })
});
