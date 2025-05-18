const cleanedContent = message.content
  ?.split('\n')
  .map(line => line.trimEnd())
  .filter((line, i, arr) => {
    const trimmed = line.trim();
    // remove all leading blank lines and collapse multiple empty lines
    if (trimmed === '' && (i === 0 || arr[i - 1].trim() === '')) {
      return false;
    }
    return true;
  })
  .join('\n')
  .trim();
