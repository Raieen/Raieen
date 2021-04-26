/**
 * Application Constants.
 * This should correspond with push_button.py.
 */
let LAST_PRESSED_ENDPOINT = "https://raw.githubusercontent.com/Raieen/Raieen/main/button/last_pressed.txt"
let ORANGE_UPPER = 99
let ORANGE_LOWER = 50

let YELLOW_UPPER = 49
let YELLOW_LOWER = 30

/**
 * Return the color based on the score.
 * This should correspond with push_button.py.
 * @param {Number} score
 */
function getColor(score) {
  if (score > ORANGE_UPPER) {
    return "red"
  } else if (score >= ORANGE_LOWER && score <= ORANGE_UPPER) {
    return "orange"
  } else if (score >= YELLOW_LOWER && score <= YELLOW_UPPER) {
    return "yellow"
  }

  return "green"
}

/**
 * Return the score.
 * This should correspond with push_button.py.
 * @param {Number} current_seconds
 * @param {Number} last_seconds
 */
function get_score(current_seconds, last_seconds) {
    return Math.floor((current_seconds - last_seconds) / 60 / 60 * 1.5)
}

addEventListener('fetch', function(event) {
  const { request } = event
  const response = handleRequest(request).catch(handleError)
  event.respondWith(response)
})

/**
 * Receives a HTTP request and replies with a response.
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function handleRequest(request) {
  let lastPressedResponse = await fetch(LAST_PRESSED_ENDPOINT)
  let lastPressedSeconds = parseInt(await lastPressedResponse.text())
  let score = get_score(new Date().getTime() / 1000, lastPressedSeconds)

  let response = await fetch(
      "https://img.shields.io/badge/-" + score + "%20points-" + getColor(score))
  response = new Response(response.body, response)
  
  // Prevent GitHub from caching the response
  response.headers.set("Cache-Control", "max-age=0, no-cache, no-store, must-revalidate")
  return response
}

/**
 * Responds with an uncaught error.
 * @param {Error} error
 * @returns {Response}
 */
function handleError(error) {
  console.error('Uncaught error:', error)

  const { stack } = error
  return new Response(stack || error, {
    status: 500,
    headers: {
      'Content-Type': 'text/plain;charset=UTF-8'
    }
  })
}
