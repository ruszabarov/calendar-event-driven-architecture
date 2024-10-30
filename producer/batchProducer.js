// IN THE TERMINAL run: npm install
// IN THE TERMINAL run: node batchProducer.js
const { generateMeeting } = require('./utils');
const { batchSizeMin, batchSizeMax, queueUrl } = require('./config');
const axios = require('axios');

// Create a batch of meetings
function createBatchOfMeetings() {
  const batchSize = getRandomInt(batchSizeMin, batchSizeMax);  // Generate random batch size --> will be between 500 to 1000
  const meetingsBatch = [];

  for (let i = 0; i < batchSize; i++) {
    meetingsBatch.push(generateMeeting());
  }

  return { meetings: meetingsBatch };  // Return the batch of meetings as JSON
}

// HTTP post send
async function sendBatchToEndpoint() {
  const batchData = createBatchOfMeetings();

  try {
    // POST req.
    const response = await axios.post(queueUrl, batchData);
    console.log(`Batch sent successfully: ${response.status}`);
  } catch (error) {
    console.error(`Error sending batch: ${error.message}`);
  }
}

// Get a random integer between min and max
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Run the batch producer to generate and send batch
sendBatchToEndpoint();
