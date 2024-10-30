const { errorRate } = require('./config');

function generateMeeting() {
  const title = generateRandomString(10);
  const location = generateRandomString(15);
  const dateTime = generateRandomDate();

  return {
    meeting_id: generateUUID(),
    title: injectError(title, 2000),
    location: injectError(location, 2000),
    date_time: dateTime,
    participants: generateParticipants(),
    attachments: generateAttachments()
  };
}

// Generate random participants
function generateParticipants() {
  const participants = [];
  const count = getRandomInt(50, 100);

  for (let i = 0; i < count; i++) {
    participants.push({
      participant_id: generateUUID(),
      name: injectError(generateRandomString(8), 600),
      email: injectEmailError(generateRandomEmail())
    });
  }

  return participants;
}

// Generate random attachments
function generateAttachments() {
  const attachments = [];
  const count = getRandomInt(5, 10);

  for (let i = 0; i < count; i++) {
    attachments.push({
      attachment_id: generateUUID(),
      url: injectUrlError(generateRandomURL())
    });
  }

  return attachments;
}

// Utility functions for random data generation

// Generate a random string of a given length
function generateRandomString(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Generate a random date in the format "YYYY-MM-DD HH:MM AM/PM"
function generateRandomDate() {
  const year = getRandomInt(2024, 2026);
  const month = String(getRandomInt(1, 12)).padStart(2, '0');
  const day = String(getRandomInt(1, 28)).padStart(2, '0');
  const hour = getRandomInt(1, 12);
  const minute = String(getRandomInt(0, 59)).padStart(2, '0');
  const ampm = Math.random() > 0.5 ? 'AM' : 'PM';
  return `${year}-${month}-${day} ${hour}:${minute} ${ampm}`;
}

// Generate a random email address
function generateRandomEmail() {
  const domains = ['example.com', 'email.com', 'test.org'];
  return `${generateRandomString(5)}@${domains[Math.floor(Math.random() * domains.length)]}`;
}

// Generate a random URL
function generateRandomURL() {
  const domains = ['example.com', 'mysite.org', 'testsite.net'];
  return `https://${generateRandomString(7)}.${domains[Math.floor(Math.random() * domains.length)]}/path`;
}

// Generate a random UUID (version 4)
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// Error injection functions
function injectError(value, maxLength) {
  return Math.random() < errorRate && value.length < maxLength ? 'A'.repeat(maxLength + 1) : value;
}

function injectEmailError(email) {
  return Math.random() < errorRate ? email.replace('@', '') : email;
}

function injectUrlError(url) {
  return Math.random() < errorRate ? 'invalid-url' : url;
}

// Get a random integer between min and max
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

module.exports = { generateMeeting };
