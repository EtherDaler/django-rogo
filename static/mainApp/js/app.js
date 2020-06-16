'use strict';

const docEl = document.querySelector('[data-id="myRides"]');
const joinerEl = docEl.querySelector('[data-id="joiner"]');
const driverEl = docEl.querySelector('[data-id="driver"]');
const drive1El = docEl.querySelector('[data-id="driver-bt"]');
const joiner1El = docEl.querySelector('[data-id="joiner-bt"]');

joiner1El.style.display = 'none';
driver1El.style.display = 'block';

drive1El.onclick = () => {
	joinerEl.style.display = 'none';
	driverEl.style.display = 'block';
};

joiner1El.onclick = () => {
	driverEl.style.display = 'none';
	joinerEl.style.display = 'block';
};