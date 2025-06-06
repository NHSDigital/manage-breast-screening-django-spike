import setSubmit from './set-submit.js'

/**
 * Enhance an HTML form to intercept submit events and instead fetch the form action URL.
 * If successful, show child elements with data-show-on-submit, and hide those with data-hide-on-submit.
 * If unsuccessful, or the fetch times out, force a page refresh.
 */
class CheckIn {
  /**
   * @param {Element | null} [$root] - HTML element to use for component
   */
  constructor($root) {
    if (!$root || !($root instanceof HTMLElement)) {
      throw new Error('CheckIn initialised without a root element')
    }

    const $form = $root.querySelector('form')
    if (!$form) {
      throw new Error('CheckIn initialised without a form element')
    }

    this.$root = $root
    this.$form = $form
    this.$showOnSubmit = $root.querySelectorAll('[data-show-on-submit]')
    this.$hideOnSubmit = $root.querySelectorAll('[data-hide-on-submit]')

    const showResult = this.showResult.bind(this)

    setSubmit(this.$form, {
      onBeforeSubmit() {
        console.log('Submitting form...')
      },
      onSuccess() {
        showResult()
      },
      onError(error) {
        console.error(error)
      }
    })
  }

  showResult() {
    this.$form.setAttribute('hidden', '')
    this.$hideOnSubmit.forEach(($elem) => $elem.setAttribute('hidden', ''))
    this.$showOnSubmit.forEach(($elem) => $elem.removeAttribute('hidden'))
  }
}

/**
 * Initialise check in component
 *
 * @param {object} [options]
 * @param {Element | Document | null} [options.scope] - Scope of the document to search within
 */
export function initCheckIn(options = {}) {
  const $scope = options.scope || document
  const $elements = $scope.querySelectorAll('[data-module="app-check-in"]')

  $elements.forEach(($root) => {
    new CheckIn($root) // eslint-disable-line no-new
  })
}
