<Typography variant="body1" sx={{ wordBreak: 'break-word' }}>
  {isUser ? (
    message.content
  ) : (
    <ReactMarkdown>{message.content}</ReactMarkdown>
  )}
</Typography>
