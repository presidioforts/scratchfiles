const timestamp: string = new Date(message.timestamp).toLocaleTimeString();

const cleanedContent = message.content
  ?.split('\n')
  .map(line => line.trimEnd())
  .filter((line, i, arr) => line.trim() !== '' || (i > 0 && arr[i - 1].trim() !== ''))
  .join('\n');
