<Paper
  elevation={isUser ? 3 : 1}
  sx={{
    maxWidth: '95%',
    width: 'fit-content',
    p: 2,
    borderRadius: 3,
    bgcolor: isUser ? 'primary.main' : 'grey.100',
    color: isUser ? 'primary.contrastText' : 'text.primary',
    overflowX: 'auto',
    whiteSpace: 'pre-wrap',
  }}
>
