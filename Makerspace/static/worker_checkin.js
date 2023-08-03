/*
* userSpecificElements.js
*
* this function shows the appropriate links/buttons depending on the privilege level of the user
*
* REFERENCES
* https://css-tricks.com/when-a-click-is-not-just-a-click/
* https://www.w3schools.com/jsref/met_document_queryselector.asp
* ChatGPT, an AI language model developed by OpenAI, accessed on [30 April 2023]
*/

// prevent the worker check in / worker check out button from automatically submitting when the page is refreshed
const workerForm = document.querySelector('#worker-form');
const workerButton = document.querySelector('#workerPresent');

workerButton.addEventListener('click', function(event) {
    event.preventDefault();
    workerForm.submit();
    const is_checked_in = document.querySelector('#is-checked-in').value === 'True';
    workerButton.innerText = is_checked_in ? 'Worker Check Out' : 'Worker Check In';
    console.log("worker in/out change")
});
