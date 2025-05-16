const TIMEOUT = 2000

/*
Enhance an HTML form to intercept submit events and instead fetch the form action URL.
If successful, show child elements with data-show-on-submit, and hide those with data-hide-on-submit.
If unsuccessful, or the fetch times out, force a page refresh.
*/
class AjaxSubmit {
  constructor($root) {
    if (!$root) {
      throw Error('AjaxSubmit initialised without a root element')
    }

    this.$root = $root
    this.$form = $root.querySelector('form')
    this.$showOnSubmit = $root.querySelectorAll('[data-show-on-submit]')
    this.$hideOnSubmit = $root.querySelectorAll('[data-hide-on-submit]')

    if (!this.$form || !(this.$form instanceof HTMLFormElement)) {
      throw Error('Must contain a form element')
    }

    this.method = this.$form.method
    this.action = this.$form.action

    if (!this.method || !this.action) {
      throw Error('Form method and action must be defined')
    }

    this.$form.addEventListener('submit', (event) => {
      event.preventDefault()
      this.submitForm()
      return false
    })
  }

  async submitForm() {
    const options = { method: this.method, body: new FormData(this.$form) }
    if (AbortSignal.timeout !== undefined) {
      options.signal = AbortSignal.timeout(TIMEOUT)
    }

    try {
      const response = await fetch(this.action, options)

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      }
    } catch (e) {
      console.error(e)
      location.reload()
      return
    }

    this.showResult()
  }

  showResult() {
    this.$form.setAttribute('hidden', '')
    this.$hideOnSubmit.forEach(($elem) => $elem.setAttribute('hidden', ''))
    this.$showOnSubmit.forEach(($elem) => $elem.removeAttribute('hidden'))
  }
}

export const init = ($scope = document) => {
  const $elements = $scope.querySelectorAll(`[data-module="app-ajax-submit"]`)

  return Array.from($elements).map(($element) => new AjaxSubmit($element))
}
