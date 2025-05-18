{isUser ? (
  <Paper
    elevation={3}
    sx={{
      maxWidth: '95%',
      width: 'fit-content',
      p: 2,
      borderRadius: 3,
      bgcolor: 'primary.main',
      color: 'primary.contrastText',
      overflowX: 'auto',
      whiteSpace: 'pre-wrap',
    }}
  >
    <Typography variant="body1" sx={{ wordBreak: 'break-word' }}>
      {message.content}
    </Typography>
    <Typography variant="caption" sx={{ display: 'block', mt: 1, textAlign: 'right' }}>
      {timestamp}
    </Typography>
  </Paper>
) : (
  <Box
    sx={{
      maxWidth: '95%',
      width: 'fit-content',
      p: 2,
      borderRadius: 3,
      bgcolor: 'grey.100',
      color: 'text.primary',
      overflowX: 'auto',
      whiteSpace: 'pre-wrap',
    }}
  >
    <ReactMarkdown>{cleanedContent}</ReactMarkdown>
    <Typography variant="caption" sx={{ display: 'block', mt: 1, textAlign: 'right' }}>
      {timestamp}
    </Typography>
  </Box>
)}
