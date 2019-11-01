import {shallowMount} from '@vue/test-utils'
import profileBlock from '../js/components/commons/profile-block.vue'

describe('profile-block', () => {
    test('is a Vue instance', () => {
        const wrapper = shallowMount(profileBlock, {
            propsData: {
                languages: [],
                index: undefined
            }
        });
        expect(wrapper.isVueInstance()).toBeTruthy()
    })
});
