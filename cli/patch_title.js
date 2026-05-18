// Patch Claude Code TUI title bar
// Injected via NODE_OPTIONS=--require
const brand = process.env._DCC_BRAND || "Claude Code";
const origLog = console.log;
const origError = console.error;
const origWrite = process.stdout.write;
const origStderrWrite = process.stderr.write;

// Hook process.stdout.write to replace "Claude Code" in TUI output
process.stdout.write = function(chunk, encoding, cb) {
  if (typeof chunk === 'string' && chunk.includes('Claude Code')) {
    chunk = chunk.replace(/Claude Code/g, brand);
  } else if (Buffer.isBuffer(chunk) && chunk.includes('Claude Code')) {
    chunk = Buffer.from(chunk.toString().replace(/Claude Code/g, brand));
  }
  return origWrite.call(process.stdout, chunk, encoding, cb);
};

process.stderr.write = function(chunk, encoding, cb) {
  if (typeof chunk === 'string' && chunk.includes('Claude Code')) {
    chunk = chunk.replace(/Claude Code/g, brand);
  } else if (Buffer.isBuffer(chunk) && chunk.includes('Claude Code')) {
    chunk = Buffer.from(chunk.toString().replace(/Claude Code/g, brand));
  }
  return origStderrWrite.call(process.stderr, chunk, encoding, cb);
};
