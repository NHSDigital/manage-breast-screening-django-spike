import { init } from './ajax-submit.js'

const html = `<div class="app-ajax-submit" data-module="app-ajax-submit">
  <div id="old-message" data-hide-on-submit>Not submitted</div>
  <div id="message" hidden data-show-on-submit>Submitted</div>
  <form id="form" data-success="container" method="post" action="/example">
    <button>Submit</button>
  </form>
</div>`

let form
let oldMessage
let message

beforeEach(() => {
  document.body.innerHTML = html
  form = document.getElementById('form')
  oldMessage = document.getElementById('old-message')
  message = document.getElementById('message')
})

afterEach(() => {})

it('swaps the form for a success message', async () => {
  mockFetch({ ok: true, status: 200 })
  init()

  form.dispatchEvent(new Event('submit'))
  await new Promise(process.nextTick)

  expect(form).toHaveAttribute('hidden')
  expect(oldMessage).toHaveAttribute('hidden')
  expect(message).not.toHaveAttribute('hidden')
})

it('refreshes the page if the request fails', async () => {
  mockFetch({ ok: false, status: 500 })
  init()

  form.dispatchEvent(new Event('submit'))
  await new Promise(process.nextTick)

  expect(location.reload).toHaveBeenCalled()
  expect(message).toHaveAttribute('hidden')
  expect(oldMessage).not.toHaveAttribute('hidden')
})

it('refreshes the page if there is an error, such as a timeout', async () => {
  mockFetchRejected(new Error('something went wrong'))
  init()

  form.dispatchEvent(new Event('submit'))
  await new Promise(process.nextTick)

  expect(location.reload).toHaveBeenCalled()
  expect(message).toHaveAttribute('hidden')
  expect(oldMessage).not.toHaveAttribute('hidden')
})
