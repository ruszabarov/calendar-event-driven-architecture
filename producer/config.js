module.exports = {
  // Endpoint
  queueUrl: 'https://httpbin.org/post',
  batchSizeMin: 500,
  batchSizeMax: 1000,
  participantMin: 50,
  participantMax: 100,
  attachmentMin: 5,
  attachmentMax: 10,
  errorRate: 0.2  // 20% errors
};