import {shallowMount} from '@vue/test-utils'
import profileBlock from '../js/components/commons/profile-block.vue'

describe('profile-block', () => {
    it('is a Vue instance', () => {
        const wrapper = shallowMount(profileBlock);
        expect(wrapper.isVueInstance()).toBeTruthy()
    });

    it('renders correctly', () => {
        const wrapper = shallowMount(profileBlock, {
            propsData: {
                title: 'Tested title',
                section_id: 'tested_id'
            },
            slots: {
                default: '<div>Tested slot</div>'
            }
        });
        expect(wrapper.element).toMatchSnapshot()
    });

    it('set title', () => {
        const EXPECTED_TITLE = 'Tested title';

        const wrapper = shallowMount(profileBlock, {
            propsData: {
                title: EXPECTED_TITLE
            }
        });
        expect(wrapper.props().title).toBe(EXPECTED_TITLE);
        expect(wrapper.find('h2').text()).toBe(EXPECTED_TITLE)
    });

    it('set section id', () => {
        const EXPECTED_ID = 'tested_id';

        const wrapper = shallowMount(profileBlock, {
            propsData: {
                section_id: EXPECTED_ID
            }
        });
        expect(wrapper.props().section_id).toBe(EXPECTED_ID);
        expect(wrapper.find('section').attributes().id).toBe(EXPECTED_ID)
    })
});
