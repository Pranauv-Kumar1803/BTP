https://react.dev/reference/react
just read thru this
const express = require('express');
const Bull = require('bull');
const Redis = require('ioredis');
const { resolve } = require('path');

const app = express();
const port = process.env.PORT || 5500;

// Redis client
const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: process.env.REDIS_PORT || 6379,
});

// Bull queue
const scanQueue = new Bull('scan-queue', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: process.env.REDIS_PORT || 6379,
  },
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  return res.send('Hi there! This is the home page');
});

app.post('/run_scan', async (req, res) => {
  const { url } = req.body;
  const requestId = new Date().getTime().toString();

  // Add job to queue
  await scanQueue.add({
    url,
    requestId,
  });

  // Immediately respond to the client
  return res.status(202).json({
    message: "Scan request accepted and queued",
    requestId,
  });
});

app.get('/scan_status/:requestId', async (req, res) => {
  const { requestId } = req.params;
  const status = await redis.get(scan:${requestId});

  if (!status) {
    return res.status(404).json({ message: "Scan not found" });
  }

  return res.json({ requestId, status });
});

// Start the server
app.listen(port, () => {
  console.log(Server running on port ${port});
});

// Worker process
scanQueue.process(async (job) => {
  const { url, requestId } = job.data;
  const savePath = output/${requestId};

  try {
    await redis.set(scan:${requestId}, 'in_progress');

    const tasks = ['wapiti', 'skipfish', 'nuclei'];
    for (const task of tasks) {
      await redis.set(scan:${requestId}, running_${task});
      await runTask(task, { url, savePath });
    }

    await redis.set(scan:${requestId}, 'completed');
  } catch (error) {
    console.error(Error processing job ${requestId}:, error);
    await redis.set(scan:${requestId}, 'failed');
  }
});

async function runTask(taskName, args) {
  const { default: worker } = await import('./worker.js');
  return worker({ functionName: taskName, args });
}