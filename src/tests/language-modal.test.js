import {shallowMount} from '@vue/test-utils'
import languageModal from '../js/components/modals/language-modal.vue'

describe('languageModal', () => {
    test('is a Vue instance', () => {
        const wrapper = shallowMount(languageModal, {
            propsData: {
                languages: [],
                index: undefined
            }
        });
        expect(wrapper.isVueInstance()).toBeTruthy()
    })
});
